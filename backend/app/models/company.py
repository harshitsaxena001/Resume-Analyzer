from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    name = Column(String(150), nullable=False)
    industry = Column(String(100))
    location = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, server_default=text("NOW()"))

    # Relationships
    recruiter = relationship("User", back_populates="companies", foreign_keys=[recruiter_id])
    job_postings = relationship("JobPosting", back_populates="company", cascade="all, delete-orphan")
