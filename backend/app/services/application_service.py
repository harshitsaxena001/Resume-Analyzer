from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.application import Application
from app.models.job_posting import JobPosting
from app.models.resume import Resume
from app.schemas.application import ApplicationCreate

async def create_application(db: AsyncSession, user_id: int, app_data: ApplicationCreate):
    job_result = await db.execute(select(JobPosting).where(JobPosting.job_id == app_data.job_id))
    job = job_result.scalars().first()
    if not job:
        return None, "job_not_found"

    existing_result = await db.execute(
        select(Application).where(
            Application.user_id == user_id,
            Application.job_id == app_data.job_id,
        )
    )
    existing_app = existing_result.scalars().first()
    if existing_app:
        return existing_app, "already_applied"

    if app_data.resume_id is not None:
        resume_result = await db.execute(select(Resume).where(Resume.resume_id == app_data.resume_id))
        resume = resume_result.scalars().first()
        if not resume or resume.user_id != user_id:
            return None, "invalid_resume"

    db_app = Application(
        user_id=user_id,
        job_id=app_data.job_id,
        resume_id=app_data.resume_id,
        cover_letter=app_data.cover_letter,
        status="applied"
    )
    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)
    return db_app, None

async def get_user_applications(db: AsyncSession, user_id: int):
    result = await db.execute(select(Application).where(Application.user_id == user_id))
    return result.scalars().all()

async def get_job_applications(db: AsyncSession, job_id: int):
    result = await db.execute(select(Application).where(Application.job_id == job_id))
    return result.scalars().all()

async def update_application_status(db: AsyncSession, application_id: int, status: str):
    result = await db.execute(select(Application).where(Application.application_id == application_id))
    db_app = result.scalars().first()
    if db_app:
        db_app.status = status
        await db.commit()
        await db.refresh(db_app)
    return db_app
