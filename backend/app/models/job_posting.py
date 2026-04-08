from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship
from app.database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    job_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="SET NULL"), nullable=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100))
    job_type = Column(String(30), server_default="full-time") # full-time, part-time, internship, contract, remote
    experience_min = Column(Numeric(3, 1), server_default="0")
    experience_max = Column(Numeric(3, 1))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    is_active = Column(Boolean, server_default="true", index=True)
    search_vector = Column(TSVECTOR)
    posted_at = Column(DateTime, server_default=text("NOW()"))
    expires_at = Column(DateTime)

    # Relationships
    company = relationship("Company", back_populates="job_postings")
    job_skills = relationship("JobSkill", back_populates="job_posting", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job_posting", cascade="all, delete-orphan")

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.job_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    is_required = Column(Boolean, server_default="true")

    # Relationships
    job_posting = relationship("JobPosting", back_populates="job_skills")
    skill = relationship("Skill")
