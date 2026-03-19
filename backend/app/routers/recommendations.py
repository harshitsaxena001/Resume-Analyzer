from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.match import MatchScoreResponse
from app.services import match_service

router = APIRouter()

@router.get("/{resume_id}", response_model=List[MatchScoreResponse])
async def get_recommendations(
    resume_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Add auth check for proper resume ownership
    matches = await match_service.get_top_matches(db, resume_id)
    return matches

@router.post("/compute/{resume_id}")
async def compute_recommendations(
    resume_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await match_service.compute_all_matches_for_resume(db, resume_id)
    return {"message": "Match scores computed successfully"}

@router.get("/skill-gap/{resume_id}/{job_id}", response_model=MatchScoreResponse)
async def get_gap_analysis(
    resume_id: int, 
    job_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = await match_service.get_skill_gap(db, resume_id, job_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match score not found. Please compute matches first.")
    return match
