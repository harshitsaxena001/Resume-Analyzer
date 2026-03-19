from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.resume import Resume, ResumeSkill
from app.models.job_posting import JobPosting, JobSkill
from app.models.match_score import MatchScore
from app.models.skill import Skill

async def compute_match_score(db: AsyncSession, resume_id: int, job_id: int):
    # Fetch Resume Skills
    res_skills_query = await db.execute(
        select(Skill.name)
        .join(ResumeSkill, ResumeSkill.skill_id == Skill.skill_id)
        .where(ResumeSkill.resume_id == resume_id)
    )
    resume_skills = set(res_skills_query.scalars().all())

    # Fetch Job Required Skills
    job_skills_query = await db.execute(
        select(Skill.name)
        .join(JobSkill, JobSkill.skill_id == Skill.skill_id)
        .where(JobSkill.job_id == job_id, JobSkill.is_required == True)
    )
    required_skills = set(job_skills_query.scalars().all())

    # Calculate gap
    matched_skills = list(resume_skills.intersection(required_skills))
    missing_skills = list(required_skills.difference(resume_skills))

    # Basic scoring logic as per PRD
    total_required = len(required_skills)
    if total_required > 0:
        skill_score = (len(matched_skills) / total_required) * 70
    else:
        skill_score = 70.0 # If no required skills, assume 100% skill match

    # Mock experience and education check (Adding arbitrary logic based on PRD multipliers block)
    # real logic would require fetching full job & resume objects and comparing values
    experience_match_bonus = 20.0
    education_match_bonus = 10.0
    
    final_score = skill_score + experience_match_bonus + education_match_bonus

    # Upsert match score
    result = await db.execute(
        select(MatchScore).where(MatchScore.resume_id == resume_id, MatchScore.job_id == job_id)
    )
    match = result.scalars().first()

    if match:
        match.score = final_score
        match.matched_skills = matched_skills
        match.missing_skills = missing_skills
    else:
        match = MatchScore(
            resume_id=resume_id,
            job_id=job_id,
            score=final_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
        db.add(match)

    await db.commit()
    await db.refresh(match)
    return match

async def get_top_matches(db: AsyncSession, resume_id: int, limit: int = 5):
    result = await db.execute(
        select(MatchScore)
        .where(MatchScore.resume_id == resume_id)
        .order_by(MatchScore.score.desc())
        .limit(limit)
    )
    return result.scalars().all()

async def get_skill_gap(db: AsyncSession, resume_id: int, job_id: int):
    result = await db.execute(
        select(MatchScore)
        .where(MatchScore.resume_id == resume_id, MatchScore.job_id == job_id)
    )
    return result.scalars().first()

async def compute_all_matches_for_resume(db: AsyncSession, resume_id: int):
    jobs_query = await db.execute(select(JobPosting.job_id).where(JobPosting.is_active == True))
    active_job_ids = jobs_query.scalars().all()
    
    for job_id in active_job_ids:
        await compute_match_score(db, resume_id, job_id)
    return True
