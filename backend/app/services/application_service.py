from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.application import Application
from app.schemas.application import ApplicationCreate

async def create_application(db: AsyncSession, user_id: int, app_data: ApplicationCreate):
    db_app = Application(
        user_id=user_id,
        job_id=app_data.job_id,
        resume_id=app_data.resume_id,
        status="applied"
    )
    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)
    return db_app

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
