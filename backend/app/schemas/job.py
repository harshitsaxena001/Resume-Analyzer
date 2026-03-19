from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    
    class Config:
        from_attributes = True
