from pydantic import BaseModel
from typing import List, Optional


class JobRecommendationResponse(BaseModel):
    resume_id: int
    job_id: int
    title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    match_reasons: List[str]
