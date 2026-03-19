from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.job import JobCreate, JobResponse
from app.services import job_service

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "recruiter" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only recruiters can post jobs")
    return await job_service.create_job(db=db, job=job)

@router.get("/", response_model=List[JobResponse])
async def get_jobs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    jobs = await job_service.get_jobs(db, skip=skip, limit=limit)
    return jobs

@router.get("/search", response_model=List[JobResponse])
async def search_jobs(q: str = Query(...), db: AsyncSession = Depends(get_db)):
    jobs = await job_service.search_jobs(db, q)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await job_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "recruiter" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only recruiters can delete jobs")
    job = await job_service.get_job_by_id(db, job_id)
    if not job:
         raise HTTPException(status_code=404, detail="Job not found")
    # Needs logic to ensure recruiter owns company associated with job
    await job_service.delete_job(db, job_id)
    return None
