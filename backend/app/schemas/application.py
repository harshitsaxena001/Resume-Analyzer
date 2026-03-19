from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: Optional[int] = None

class ApplicationStatusUpdate(BaseModel):
    status: str

class ApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    job_id: int
    resume_id: Optional[int]
    status: str
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
