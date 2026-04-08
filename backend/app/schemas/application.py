from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: Optional[int] = None
    cover_letter: Optional[str] = None

class ApplicationStatusUpdate(BaseModel):
    status: str

class ApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    job_id: int
    resume_id: Optional[int]
    cover_letter: Optional[str]
    status: str
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
