from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.resume import ResumeResponse
from app.services import resume_service

router = APIRouter()

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        resume = await resume_service.process_resume_upload(user_id=current_user.user_id, file=file, db=db)
        return resume
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    resume = await resume_service.get_resume_by_id(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.user_id != current_user.user_id and current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Not authorized to view this resume")
    return resume

@router.get("/user/{user_id}", response_model=List[ResumeResponse])
async def get_all_resumes_for_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.user_id and current_user.role != "recruiter":
         raise HTTPException(status_code=403, detail="Not authorized")
    resumes = await resume_service.get_user_resumes(db, user_id)
    return resumes

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    resume = await resume_service.get_resume_by_id(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this resume")
    
    await resume_service.delete_resume(db, resume_id)
    return None
