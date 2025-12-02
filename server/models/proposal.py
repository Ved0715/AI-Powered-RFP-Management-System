from sqlalchemy import Column, String, DateTime, Text, JSON, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .base import Base, ProposalStatus


class Proposal(Base):
    __tablename__ = 'proposals'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Relationships
    rfp_id = Column(String, ForeignKey("rfps.id"), nullable=False)
    rfp = relationship("RFP", back_populates="proposals")
    
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    vendor = relationship("Vendor", back_populates="proposals")
    
    email_raw = Column(Text)  
    email_subject = Column(String)
    
    total_price = Column(Numeric(10, 2))
    line_items = Column(JSON, default=list)  # Individual items with prices
    terms = Column(Text)
    delivery_time = Column(String)
    warranty = Column(String)
    
   
    ai_score = Column(Numeric(3, 2))  
    ai_summary = Column(Text) 
    ai_pros = Column(JSON, default=list)
    ai_cons = Column(JSON, default=list)
    
    status = Column(String, default=ProposalStatus.DRAFT.value)
    
    received_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)