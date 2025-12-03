from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from models import get_db, RFP, Vendor
from schemas.rfp import RFPCreate, RFPResponse, RFPUpdate, RFPVendorLink
from schemas.vendor import VendorResponse
from services.ai_service import parse_rfp_description


router = APIRouter(prefix="/api/rfps", tags=["RFPs"])


# CREATE
@router.post("/", response_model=RFPResponse, status_code=status.HTTP_201_CREATED)
async def create_rfp(rfp: RFPCreate, db: AsyncSession = Depends(get_db)):
    
    parsed_data = await parse_rfp_description(rfp.description)
    
    try:
        new_rfp = RFP(
            title=parsed_data.get("title", "Untitled RFP"),
            description=rfp.description,
            budget=parsed_data.get("budget"),
            deadline=parsed_data.get("deadline"),
            requirements=parsed_data.get("requirements", []),
            payment_terms=parsed_data.get("payment_terms"),
            warranty_terms=parsed_data.get("warranty_terms"),
            status="NEW"
        )
        
        db.add(new_rfp)
        await db.commit()
        await db.refresh(new_rfp)
        
        return new_rfp
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create RFP: {str(e)}"
        )

#get all rfps
@router.get("/", response_model=List[RFPResponse])
async def get_rfps(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip cannot be negative"
        )
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 1000"
        )
    
    try:

        result = await db.execute(
            select(RFP)
            .offset(skip)
            .limit(limit)
            .order_by(RFP.created_at.desc())
        )

        rfps = result.scalars().all()
        return rfps
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch RFPs: {str(e)}"
        )


#get single rfp
@router.get("/{rfp_id}", response_model=RFPResponse)
async def get_rfp(rfp_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific RFP by ID"""
    
    if not rfp_id or not rfp_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RFP ID cannot be empty"
        )
    
    try:
        result = await db.execute(select(RFP).where(RFP.id == rfp_id))
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {rfp_id} not found"
            )
        
        return rfp
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch RFP: {str(e)}"
        )

#Modify RFP
@router.put("/{rfp_id}", response_model=RFPResponse)
async def update_rfp(rfp_id: str, rfp_update: RFPUpdate, db: AsyncSession = Depends(get_db)):
    
    if not rfp_id or not rfp_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RFP ID cannot be empty"
        )
    
    update_data = rfp_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    try:
        result = await db.execute(select(RFP).where(RFP.id == rfp_id))
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {rfp_id} not found"
            )
        
        for field, value in update_data.items():
            setattr(rfp, field, value)
        
        await db.commit()
        await db.refresh(rfp)
        
        return rfp
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update RFP: {str(e)}"
        )


#Remove RFP
@router.delete("/{rfp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rfp(rfp_id: str, db: AsyncSession = Depends(get_db)):
    
    if not rfp_id or not rfp_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RFP ID cannot be empty"
        )
    
    try:
        result = await db.execute(select(RFP).where(RFP.id == rfp_id))
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {rfp_id} not found"
            )
        
        await db.delete(rfp)
        await db.commit()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete RFP: {str(e)}"
        )


#Assign vendors to RFP
@router.post("/{rfp_id}/vendors", response_model=RFPResponse)
async def link_vendors_to_rfp(
    rfp_id: str,
    vendor_link: RFPVendorLink,
    db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await db.execute(select(RFP).where(RFP.id == rfp_id))
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {rfp_id} not found"
            )
        
        # Verify all vendors exist
        for vendor_id in vendor_link.vendor_ids:
            result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
            vendor = result.scalar_one_or_none()
            
            if not vendor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vendor with id {vendor_id} not found"
                )
        
        rfp.sent_to_vendors = vendor_link.vendor_ids
        
        await db.commit()
        await db.refresh(rfp)
        
        return rfp
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to link vendors: {str(e)}"
        )


#get vendors fron rfp
@router.get("/{rfp_id}/vendors", response_model=List[VendorResponse])
async def get_rfp_vendors(
    rfp_id: str,
    db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await db.execute(select(RFP).where(RFP.id == rfp_id))
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {rfp_id} not found"
            )
        
        # Get vendors by IDs
        vendors = []
        for vendor_id in rfp.sent_to_vendors:
            result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
            vendor = result.scalar_one_or_none()
            if vendor:
                vendors.append(vendor)
        
        return vendors
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch vendors: {str(e)}"
        )

