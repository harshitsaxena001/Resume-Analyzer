from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import relationship
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255))
    file_path = Column(Text)
    raw_text = Column(Text)
    parsed_json = Column(JSONB)
    experience_yrs = Column(Numeric(4, 1))
    education_level = Column(String(50))
    current_role = Column(String(100))
    location = Column(String(100))
    overall_score = Column(Numeric(4, 1))
    search_vector = Column(TSVECTOR)
    uploaded_at = Column(DateTime, server_default=text("NOW()"))
    updated_at = Column(DateTime, server_default=text("NOW()"), onupdate=text("NOW()"))

    # Relationships
    user = relationship("User", back_populates="resumes")
    resume_skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="resume", cascade="all, delete-orphan")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False, index=True)
    proficiency = Column(String(20), server_default="intermediate") # 'beginner', 'intermediate', 'expert'
    years_exp = Column(Numeric(3, 1))

    # Relationships
    resume = relationship("Resume", back_populates="resume_skills")
    skill = relationship("Skill")
