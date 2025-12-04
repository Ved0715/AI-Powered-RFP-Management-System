from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List

from models import get_db, Vendor
from schemas.vendor import VendorCreate, VendorUpdate, VendorResponse

router = APIRouter(prefix="/api/vendors", tags=["Vendors"])

#create
@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor( vendor: VendorCreate, db: AsyncSession = Depends(get_db)):
    # Check if vendor with email already exists
    result = await db.execute(
        select(Vendor).where(Vendor.email == vendor.email.lower().strip())
    )
    existing_vendor = result.scalar_one_or_none()
    
    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendor with email {vendor.email} already exists"
        )
    
    try:
        new_vendor = Vendor(
            name=vendor.name,
            email=vendor.email.lower().strip(),  
            contact_person=vendor.contact_person,
            phone=vendor.phone.strip() if vendor.phone else None,
            notes=vendor.notes if vendor.notes else None
        )
        
        db.add(new_vendor)
        await db.commit()
        await db.refresh(new_vendor)
        
        return new_vendor
        
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create vendor due to database constraint"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

#Get all vendors
@router.get("/", response_model=List[VendorResponse])
async def get_vendors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):

    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip parameter cannot be negative"
        )
    
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 1000"
        )
    
    try:
        result = await db.execute(
            select(Vendor)
            .offset(skip)
            .limit(limit)
        )
        vendors = result.scalars().all()
        return vendors
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch vendors: {str(e)}"
        )

#Get single vendor by ID
@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: str, db: AsyncSession = Depends(get_db)):
  
    if not vendor_id or not vendor_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor ID cannot be empty"
        )
    
    try:
        result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()
        
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {vendor_id} not found"
            )
        
        return vendor
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch vendor: {str(e)}"
        )

#Modify vendor
@router.put("/{vendor_id}", response_model=VendorResponse)
async def update_vendor( vendor_id: str, vendor_update: VendorUpdate, db: AsyncSession = Depends(get_db) ):
    
    if not vendor_id or not vendor_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor ID cannot be empty"
        )

    update_data = vendor_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )


    try:
        result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()
        
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {vendor_id} not found"
            )
        
        if "email" in update_data and update_data["email"] != vendor.email:
            result = await db.execute(
                select(Vendor).where(Vendor.email == update_data["email"])
            )
            existing_vendor = result.scalar_one_or_none()
            
            if existing_vendor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Another vendor with email {update_data['email']} already exists"
                )
            
            update_data["email"] = update_data["email"].lower().strip()
        
        
        update_data["phone"] = update_data["phone"].strip()
        
        for field, value in update_data.items():
            setattr(vendor, field, value)
        
        await db.commit()
        await db.refresh(vendor)
        
        return vendor
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vendor: {str(e)}"
        )



#Remove vendor
@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor( vendor_id: str,db: AsyncSession = Depends(get_db) ):

    if not vendor_id or not vendor_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor ID cannot be empty"
        )

    try:
        result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()
        
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {vendor_id} not found"
            )
        
        await db.delete(vendor)
        await db.commit()
        
        return None 
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete vendor: {str(e)}"
        )