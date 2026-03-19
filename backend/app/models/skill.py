from sqlalchemy import Column, Integer, String, DateTime, text
from app.database import Base

class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50)) # e.g., 'Programming', 'Framework', 'Soft Skill'
    created_at = Column(DateTime, server_default=text("NOW()"))
