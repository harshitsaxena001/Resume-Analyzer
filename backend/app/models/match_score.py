from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class MatchScore(Base):
    __tablename__ = "match_scores"

    match_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.job_id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Numeric(5, 2), index=True) # 0.00 to 100.00
    matched_skills = Column(JSONB) # list of matched skill names
    missing_skills = Column(JSONB) # list of missing required skills
    computed_at = Column(DateTime, server_default=text("NOW()"))

    # Relationships
    resume = relationship("Resume", back_populates="match_scores")
    job_posting = relationship("JobPosting", back_populates="match_scores")
