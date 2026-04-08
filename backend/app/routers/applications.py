from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate
from app.services import application_service

router = APIRouter()

@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    app_data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_app, error_code = await application_service.create_application(db, current_user.user_id, app_data)

    if error_code == "job_not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    if error_code == "already_applied":
        raise HTTPException(status_code=409, detail="You have already applied to this job")
    if error_code == "invalid_resume":
        raise HTTPException(status_code=400, detail="Selected resume is invalid")

    return db_app

@router.get("/user/{user_id}", response_model=List[ApplicationResponse])
async def get_user_applications(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await application_service.get_user_applications(db, user_id)

@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
async def get_job_applications(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "recruiter" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await application_service.get_job_applications(db, job_id)

@router.patch("/{app_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    app_id: int,
    status_update: ApplicationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "recruiter" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    app = await application_service.update_application_status(db, app_id, status_update.status)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app
