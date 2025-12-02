from sqlalchemy import Column, String, DateTime, Text, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .base import Base, RFPStatus


class RFP(Base):
    __tablename__ = 'rfps'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)  
    
    budget = Column(Numeric(10, 2))
    deadline = Column(DateTime)
    requirements = Column(JSON, default=list) 
    payment_terms = Column(String)
    warranty_terms = Column(String)
    status = Column(String, default=RFPStatus.NEW.value)
    sent_to_vendors = Column(JSON, default=list)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    proposals = relationship("Proposal", back_populates="rfp", cascade="all, delete-orphan")
