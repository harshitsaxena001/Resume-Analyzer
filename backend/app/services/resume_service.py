import os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.models.resume import Resume, ResumeSkill
from app.models.skill import Skill
from app.utils.pdf_parser import extract_text_from_pdf
from app.services.ai_service import parse_resume

async def process_resume_upload(user_id: int, file: UploadFile, db: AsyncSession):
    # 1. Save file locally
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    file_bytes = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_bytes)
        
    # 2. Extract text from PDF
    raw_text = extract_text_from_pdf(file_bytes)
    
    # 3. Parse with Claude
    parsed_data = await parse_resume(raw_text)
    
    # 4. Save Resume in DB
    db_resume = Resume(
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path,
        raw_text=raw_text,
        parsed_json=parsed_data.model_dump(),
        experience_yrs=parsed_data.experience_years,
        education_level=parsed_data.education_level,
        current_role=parsed_data.current_role,
        overall_score=parsed_data.overall_score
    )
    db.add(db_resume)
    await db.commit()
    await db.refresh(db_resume)
    
    # 5. Handle Skills Normalization
    for skill_name in parsed_data.skills:
        # Check if skill exists
        result = await db.execute(select(Skill).where(Skill.name == skill_name))
        db_skill = result.scalars().first()
        
        # If not, create it
        if not db_skill:
            db_skill = Skill(name=skill_name, category="General")
            db.add(db_skill)
            await db.commit()
            await db.refresh(db_skill)
            
        # Link to resume
        db_resume_skill = ResumeSkill(
            resume_id=db_resume.resume_id,
            skill_id=db_skill.skill_id,
            proficiency="intermediate", # Defaulting
            years_exp=0 # Could be inferred from AI if added
        )
        db.add(db_resume_skill)
        
    await db.commit()
    return db_resume

async def get_resume_by_id(db: AsyncSession, resume_id: int):
    result = await db.execute(select(Resume).where(Resume.resume_id == resume_id))
    return result.scalars().first()

async def get_user_resumes(db: AsyncSession, user_id: int):
    result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    return result.scalars().all()

async def delete_resume(db: AsyncSession, resume_id: int):
    resume = await get_resume_by_id(db, resume_id)
    if resume:
        db.delete(resume)
        await db.commit()
        return True
    return False
