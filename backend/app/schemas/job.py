from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class CompanyMatch(BaseModel):
    company_id: int
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    skill_id: int
    name: str
    class Config:
        from_attributes = True

class JobSkillBase(BaseModel):
    id: int
    is_required: bool
    skill: SkillBase
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    job_type: Optional[str] = "full-time"
    experience_min: Optional[float] = 0.0
    experience_max: Optional[float] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    is_active: bool = True

class JobCreate(JobBase):
    company_id: Optional[int] = None
    required_skills: List[str] = []

class JobResponse(JobBase):
    job_id: int
    company_id: Optional[int]
    posted_at: datetime
    expires_at: Optional[datetime]
    company: Optional[CompanyMatch] = None
    job_skills: List[JobSkillBase] = []
    
    
    class Config:
        from_attributes = True
