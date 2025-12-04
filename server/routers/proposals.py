
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from models import get_db, Proposal, RFP, Vendor
from schemas.proposal import ProposalCreate, ProposalResponse, ProposalUpdate
from services.email_service import get_unread_emails, mark_email_as_read
from services.ai_service import parse_vendor_proposal


router = APIRouter(prefix="/api/proposals", tags=["Proposals"])


#cehck for venders responce with ai.
@router.post("/rfps/{rfp_id}/check-responses", response_model=dict)
async def check_vendor_responses(
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
        
        if not rfp.sent_to_vendors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No vendors linked to this RFP"
            )
        
        vendor_emails = []
        vendor_map = {} 
        
        for vendor_id in rfp.sent_to_vendors:
            result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
            vendor = result.scalar_one_or_none()
            if vendor:
                vendor_emails.append(vendor.email)
                vendor_map[vendor.email.lower()] = vendor.id
        
        unread_emails = get_unread_emails(vendor_emails=vendor_emails, max_results=20)
        
        created_proposals = []
        
        for email_data in unread_emails:
            sender = email_data['from']
            
            if '<' in sender:
                email_address = sender.split('<')[1].split('>')[0].strip().lower()
            else:
                email_address = sender.strip().lower()
            
            # Check if this vendor already has a proposal
            vendor_id = vendor_map.get(email_address)
            if not vendor_id:
                continue
            
            result = await db.execute(
                select(Proposal).where(
                    Proposal.rfp_id == rfp_id,
                    Proposal.vendor_id == vendor_id
                )
            )
            existing_proposal = result.scalar_one_or_none()
            
            if existing_proposal:
                continue  

            # Parse email with AI
            parsed_data = await parse_vendor_proposal(
                email_body=email_data['body'],
                email_subject=email_data['subject']
            )
            
            # Create proposal
            new_proposal = Proposal(
                rfp_id=rfp_id,
                vendor_id=vendor_id,
                email_raw=email_data['body'],
                email_subject=email_data['subject'],
                total_price=parsed_data.get('total_price'),
                line_items=parsed_data.get('line_items', []),
                terms=parsed_data.get('terms'),
                delivery_time=parsed_data.get('delivery_time'),
                warranty=parsed_data.get('warranty'),
                status="PENDING",
                received_at=datetime.utcnow()
            )
            
            db.add(new_proposal)
            created_proposals.append({
                "vendor_id": vendor_id,
                "email_subject": email_data['subject']
            })
            
            # Mark email as read
            mark_email_as_read(email_data['id'])
        
        await db.commit()
        
        return {
            "rfp_id": rfp_id,
            "checked": len(unread_emails),
            "created": len(created_proposals),
            "proposals": created_proposals
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check responses: {str(e)}"
        )


# GET ALL PROPOSALS FOR AN RFP
@router.get("/rfps/{rfp_id}", response_model=List[ProposalResponse])
async def get_rfp_proposals(
    rfp_id: str,
    db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await db.execute(
            select(Proposal)
            .where(Proposal.rfp_id == rfp_id)
            .order_by(Proposal.created_at.desc())
        )
        proposals = result.scalars().all()
        return proposals
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch proposals: {str(e)}"
        )


# GET SINGLE PROPOSAL
@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get specific proposal by ID"""
    
    try:
        result = await db.execute(select(Proposal).where(Proposal.id == proposal_id))
        proposal = result.scalar_one_or_none()
        
        if not proposal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proposal with id {proposal_id} not found"
            )
        
        return proposal
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch proposal: {str(e)}"
        )


# CREATE PROPOSAL MANUALLY (for testing)
@router.post("/", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
async def create_proposal(
    proposal: ProposalCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a proposal manually (for testing/demo purposes)"""
    
    try:
        # Verify RFP exists
        result = await db.execute(select(RFP).where(RFP.id == proposal.rfp_id))
        rfp = result.scalar_one_or_none()
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RFP with id {proposal.rfp_id} not found"
            )
        
        # Verify vendor exists
        result = await db.execute(select(Vendor).where(Vendor.id == proposal.vendor_id))
        vendor = result.scalar_one_or_none()
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {proposal.vendor_id} not found"
            )
        
        new_proposal = Proposal(
            rfp_id=proposal.rfp_id,
            vendor_id=proposal.vendor_id,
            email_raw=proposal.email_raw,
            email_subject=proposal.email_subject,
            total_price=proposal.total_price,
            line_items=proposal.line_items,
            terms=proposal.terms,
            delivery_time=proposal.delivery_time,
            warranty=proposal.warranty,
            status="PENDING",
            received_at=datetime.utcnow()
        )
        
        db.add(new_proposal)
        await db.commit()
        await db.refresh(new_proposal)
        
        return new_proposal
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create proposal: {str(e)}"
        )


# UPDATE PROPOSAL
@router.put("/{proposal_id}", response_model=ProposalResponse)
async def update_proposal(
    proposal_id: str,
    proposal_update: ProposalUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update proposal information"""
    
    update_data = proposal_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    try:
        result = await db.execute(select(Proposal).where(Proposal.id == proposal_id))
        proposal = result.scalar_one_or_none()
        
        if not proposal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proposal with id {proposal_id} not found"
            )
        
        for field, value in update_data.items():
            setattr(proposal, field, value)
        
        await db.commit()
        await db.refresh(proposal)
        
        return proposal
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update proposal: {str(e)}"
        )


# DELETE PROPOSAL
@router.delete("/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proposal(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    
    try:
        result = await db.execute(select(Proposal).where(Proposal.id == proposal_id))
        proposal = result.scalar_one_or_none()
        
        if not proposal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proposal with id {proposal_id} not found"
            )
        
        await db.delete(proposal)
        await db.commit()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete proposal: {str(e)}"
        )
