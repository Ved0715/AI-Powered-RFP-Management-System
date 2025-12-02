from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class VendorCreate(BaseModel):
    name: str
    email: EmailStr  # Validates email format
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class VendorResponse(BaseModel):
    id: str
    name: str
    email: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
