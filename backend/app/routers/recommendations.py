from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.match import JobRecommendationResponse
from app.services import match_service

router = APIRouter()


@router.get("/user/me", response_model=List[JobRecommendationResponse])
async def get_recommendations_for_current_user(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    capped_limit = min(max(limit, 1), 50)
    return await match_service.recommend_jobs_for_user(db, current_user.user_id, capped_limit)
