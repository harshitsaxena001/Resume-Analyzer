from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MatchScoreResponse(BaseModel):
    match_id: int
    resume_id: int
    job_id: int
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    computed_at: datetime

    class Config:
        from_attributes = True
