from pydantic import BaseModel
from datatime import datetime
from typing import Optional, List


class RFPCreate(BaseModel):
    description: str

class RFPResponse(BaseModel):
    id: str
    title: str
    description: str
    budget: Optional[float] = None
    deadline: Optional[datetime] = None
    requirements: List[str] = []
    payment_terms: Optional[str] = None
    warranty_terms: Optional[str] = None
    status: str
    sent_to_vendors: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RFPUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    deadline: Optional[datetime] = None
    requirements: Optional[List[str]] = None
    payment_terms: Optional[str] = None
    warranty_terms: Optional[str] = None
    status: Optional[str] = None


# Schema for linking vendors to RFP
class RFPVendorLink(BaseModel):
    vendor_ids: List[str]  




