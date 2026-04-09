from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkExperience(BaseModel):
    company: str
    role: str
    duration: str

class ResumeParsedData(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    current_role: str
    experience_years: float
    education_level: str
    skills: List[str]
    work_experience: List[WorkExperience]
    certifications: List[str]
    overall_score: float
    resume_upgrade_suggestions: List[str] = []

class ResumeResponse(BaseModel):
    resume_id: int
    user_id: int
    file_name: str
    parsed_json: ResumeParsedData
    experience_yrs: Optional[float]
    education_level: Optional[str]
    current_role: Optional[str]
    overall_score: Optional[float]
    uploaded_at: datetime

    class Config:
        from_attributes = True
