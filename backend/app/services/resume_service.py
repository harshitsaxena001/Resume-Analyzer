import os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

from app.config import settings
from app.models.resume import Resume, ResumeSkill
from app.models.skill import Skill
from app.utils.pdf_parser import extract_text_from_pdf
from app.services.ai_service import parse_resume


def _trim(value: str | None, max_len: int) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    if not cleaned:
        return None
    return cleaned[:max_len]


def _normalize_skills(skills: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        cleaned = _trim(skill, 100)
        if not cleaned:
            continue

        # Collapse repeated whitespace and dedupe case-insensitively.
        cleaned = " ".join(cleaned.split())
        key = cleaned.lower()
        if key in seen:
            continue

        seen.add(key)
        normalized.append(cleaned)

    return normalized

async def process_resume_upload(user_id: int, file: UploadFile, db: AsyncSession):
    # 1. Save file locally
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    file_bytes = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_bytes)
        
    # 2. Extract text from PDF
    raw_text = extract_text_from_pdf(file_bytes)
    
    # 3. Parse with Gemini (single API call)
    parsed_data = await parse_resume(raw_text)

    # Keep values within DB varchar limits to avoid truncation exceptions.
    db_file_name = _trim(file.filename, 255)
    db_education_level = _trim(parsed_data.education_level, 50)
    db_current_role = _trim(parsed_data.current_role, 100)
    db_location = _trim(getattr(parsed_data, "location", None), 100)
    
    # 4. Save Resume in DB
    db_resume = Resume(
        user_id=user_id,
        file_name=db_file_name,
        file_path=file_path,
        raw_text=raw_text,
        parsed_json=parsed_data.model_dump(),
        experience_yrs=parsed_data.experience_years,
        education_level=db_education_level,
        current_role=db_current_role,
        location=db_location,
        overall_score=parsed_data.overall_score
    )
    db.add(db_resume)
    await db.commit()
    await db.refresh(db_resume)
    
    # 5. Handle skills normalization safely.
    normalized_skills = _normalize_skills(parsed_data.skills)

    try:
        for skill_name in normalized_skills:
            result = await db.execute(
                select(Skill).where(func.lower(Skill.name) == skill_name.lower())
            )
            db_skill = result.scalars().first()

            if not db_skill:
                db_skill = Skill(name=skill_name, category="General")
                db.add(db_skill)
                try:
                    await db.flush()
                except IntegrityError:
                    # Handle race/duplicate creation by reloading existing row.
                    await db.rollback()
                    result = await db.execute(
                        select(Skill).where(func.lower(Skill.name) == skill_name.lower())
                    )
                    db_skill = result.scalars().first()
                    if not db_skill:
                        raise

            db_resume_skill = ResumeSkill(
                resume_id=db_resume.resume_id,
                skill_id=db_skill.skill_id,
                proficiency="intermediate",
                years_exp=0,
            )
            db.add(db_resume_skill)

        await db.commit()
    except (DataError, IntegrityError, SQLAlchemyError) as exc:
        await db.rollback()
        raise ValueError(f"Could not save parsed resume data: {exc}")

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
