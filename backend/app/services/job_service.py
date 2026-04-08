from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload, joinedload
from app.models.job_posting import JobPosting, JobSkill
from app.models.company import Company
from app.models.skill import Skill
from app.schemas.job import JobCreate
from typing import List


def _normalize_skill_names(skills: List[str]) -> List[str]:
    seen = set()
    normalized = []
    for skill in skills:
        clean = (skill or "").strip()
        if not clean:
            continue
        key = clean.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(clean)
    return normalized

async def create_job(db: AsyncSession, job: JobCreate):
    required_skills = _normalize_skill_names(job.required_skills or [])

    description = job.description
    if required_skills:
        description_lower = (description or "").lower()
        if "skills" not in description_lower and "required" not in description_lower:
            description = (
                f"{description}\n\nKey skills demanded: {', '.join(required_skills)}"
            )

    db_job = JobPosting(
        title=job.title,
        description=description,
        location=job.location,
        job_type=job.job_type,
        experience_min=job.experience_min,
        experience_max=job.experience_max,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        company_id=job.company_id,
        is_active=job.is_active
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    
    # Process required skills
    if required_skills:
        for skill_name in required_skills:
            result = await db.execute(select(Skill).where(Skill.name == skill_name))
            db_skill = result.scalars().first()
            if not db_skill:
                db_skill = Skill(name=skill_name, category="General")
                db.add(db_skill)
                await db.commit()
                await db.refresh(db_skill)
            
            job_skill = JobSkill(
                job_id=db_job.job_id,
                skill_id=db_skill.skill_id,
                is_required=True
            )
            db.add(job_skill)
        await db.commit()

        if db_job.company_id:
            company_result = await db.execute(
                select(Company).where(Company.company_id == db_job.company_id)
            )
            company = company_result.scalars().first()
            if company:
                existing_desc = (company.description or "").strip()
                focus_line = f"Commonly hiring for skills: {', '.join(required_skills)}"
                if focus_line.lower() not in existing_desc.lower():
                    company.description = (
                        f"{existing_desc}\n\n{focus_line}".strip()
                        if existing_desc
                        else focus_line
                    )
                    await db.commit()
        
    return db_job

async def get_job_by_id(db: AsyncSession, job_id: int):
    stmt = (
        select(JobPosting)
        .options(
            joinedload(JobPosting.company),
            selectinload(JobPosting.job_skills).joinedload(JobSkill.skill)
        )
        .where(JobPosting.job_id == job_id)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = (
        select(JobPosting)
        .options(
            joinedload(JobPosting.company),
            selectinload(JobPosting.job_skills).joinedload(JobSkill.skill)
        )
        .where(JobPosting.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def search_jobs(db: AsyncSession, query: str):
    # Full-text search using PostgreSQL tsvector
    # 'english' dictionary is used in PRD
    # Using plainto_tsquery or to_tsquery
    search_query = func.plainto_tsquery('english', query)
    result = await db.execute(
        select(JobPosting)
        .options(
            joinedload(JobPosting.company),
            selectinload(JobPosting.job_skills).joinedload(JobSkill.skill)
        )
        .where(
            JobPosting.is_active == True,
            JobPosting.search_vector.op("@@")(search_query)
        )
    )
    return result.scalars().all()

async def delete_job(db: AsyncSession, job_id: int):
    job = await get_job_by_id(db, job_id)
    if job:
        db.delete(job)
        await db.commit()
        return True
    return False

# update_job function can be added later as needed
