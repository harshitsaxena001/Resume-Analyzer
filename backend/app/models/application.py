from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_applications_user_job"),
    )

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.job_id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="SET NULL"), nullable=True)
    cover_letter = Column(Text, nullable=True)
    status = Column(String(30), server_default="applied") # applied, under_review, shortlisted, rejected, offered
    applied_at = Column(DateTime, server_default=text("NOW()"))
    updated_at = Column(DateTime, server_default=text("NOW()"), onupdate=text("NOW()"))

    # Relationships
    user = relationship("User", back_populates="applications")
    job_posting = relationship("JobPosting", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
