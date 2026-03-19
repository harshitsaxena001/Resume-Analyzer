from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.job_posting import JobPosting, JobSkill
from app.models.skill import Skill
from app.schemas.job import JobCreate
from typing import List

async def create_job(db: AsyncSession, job: JobCreate):
    db_job = JobPosting(
        title=job.title,
        description=job.description,
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
    if job.required_skills:
        for skill_name in job.required_skills:
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
        
    return db_job

async def get_job_by_id(db: AsyncSession, job_id: int):
    result = await db.execute(select(JobPosting).where(JobPosting.job_id == job_id))
    return result.scalars().first()

async def get_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(JobPosting).where(JobPosting.is_active == True).offset(skip).limit(limit))
    return result.scalars().all()

async def search_jobs(db: AsyncSession, query: str):
    # Full-text search using PostgreSQL tsvector
    # 'english' dictionary is used in PRD
    # Using plainto_tsquery or to_tsquery
    search_query = func.plainto_tsquery('english', query)
    result = await db.execute(
        select(JobPosting)
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
