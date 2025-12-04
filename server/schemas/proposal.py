from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class ProposalCreate(BaseModel):
    rfp_id: str
    vendor_id: str
    email_raw: Optional[str] = None
    email_subject: Optional[str] = None
    total_price: Optional[float] = None
    line_items: Optional[List[Dict]] = []
    terms: Optional[str] = None
    delivery_time: Optional[str] = None
    warranty: Optional[str] = None

class ProposalResponse(BaseModel):
    id: str
    rfp_id: str
    vendor_id: str
    email_raw: Optional[str] = None
    email_subject: Optional[str] = None
    total_price: Optional[float] = None
    line_items: List[Dict] = []
    terms: Optional[str] = None
    delivery_time: Optional[str] = None
    warranty: Optional[str] = None
    ai_score: Optional[float] = None
    ai_summary: Optional[str] = None
    ai_pros: Optional[List[str]] = []
    ai_cons: Optional[List[str]] = []
    status: str
    received_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProposalUpdate(BaseModel):
    total_price: Optional[float] = None
    line_items: Optional[List[Dict]] = None
    terms: Optional[str] = None
    delivery_time: Optional[str] = None
    warranty: Optional[str] = None
    status: Optional[str] = None
