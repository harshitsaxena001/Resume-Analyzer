from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.models.resume import Resume, ResumeSkill
from app.models.job_posting import JobPosting, JobSkill
from app.models.skill import Skill


MIN_MATCH_SCORE = 50.0


def _normalize_skill_set(skills: set[str]) -> set[str]:
    return {skill.strip().lower() for skill in skills if skill and skill.strip()}


def _safe_float(value, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _partial_skill_match(candidate_skills: set[str], required_skill: str) -> bool:
    """Check if any candidate skill partially matches required skill (e.g., 'react' matches 'react native')."""
    req_lower = required_skill.lower()
    
    for cand_skill in candidate_skills:
        cand_lower = cand_skill.lower()
        # Exact match
        if cand_lower == req_lower:
            return True
        # Partial match: one contains the other or common prefix
        if cand_lower in req_lower or req_lower in cand_lower:
            return True
        # Common framework matching (e.g., "react" matches "react native", "typescript")
        if any(cand_lower.startswith(part) or req_lower.startswith(part) 
               for part in ['react', 'node', 'python', 'java', 'c++']):
            if cand_lower.startswith(req_lower[:3]) or req_lower.startswith(cand_lower[:3]):
                return True
    
    return False


def _role_seniority_score(current_role: str | None, job_title: str | None) -> tuple[float, bool]:
    """
    Calculate role progression score and check for seniority match.
    Returns: (score 0.0-15.0, is_progression_fit)
    """
    if not current_role or not job_title:
        return 0.0, False
    
    current_lower = current_role.lower()
    job_lower = job_title.lower()
    
    # Exact or close role match
    if current_lower in job_lower or job_lower in current_lower:
        return 15.0, True
    
    # Senior progression
    senior_keywords = {'senior', 'lead', 'principal', 'staff', 'architect', 'manager'}
    junior_keywords = {'junior', 'intern', 'entry', 'associate'}
    
    job_has_senior = any(kw in job_lower for kw in senior_keywords)
    current_has_senior = any(kw in current_lower for kw in senior_keywords)
    current_has_junior = any(kw in current_lower for kw in junior_keywords)
    
    # Progression from junior to regular
    if current_has_junior and not job_has_senior:
        return 12.0, True
    
    # Natural progression from regular to senior
    if not current_has_senior and job_has_senior:
        return 10.0, True
    
    # Same level seniority
    if (current_has_senior and job_has_senior) or (not current_has_senior and not job_has_senior):
        return 8.0, True
    
    return 0.0, False


def _education_match_score(resume_education: str | None, job_type: str | None) -> float:
    """Calculate education level appropriateness score (0.0-5.0)."""
    if not resume_education:
        return 2.0  # Neutral if not specified
    
    resume_edu_lower = (resume_education or "").lower()
    job_type_lower = (job_type or "").lower()
    
    education_levels = {
        "phd": 4,
        "masters": 3,
        "bachelors": 2,
        "diploma": 1,
        "not specified": 0,
    }
    
    resume_level = education_levels.get(resume_edu_lower, 0)
    
    # Junior roles prefer bachelor+ 
    if "junior" in job_type_lower or "intern" in job_type_lower:
        return min(5.0, 3.0 + (resume_level * 0.4))
    
    # Senior roles prefer master+
    if any(kw in job_type_lower for kw in ["senior", "lead", "principal", "manager"]):
        return min(5.0, 2.0 + (resume_level * 0.6))
    
    # Regular roles
    return min(5.0, 2.5 + (resume_level * 0.5))


def _keyword_overlap(current_role: str | None, title: str | None) -> bool:
    if not current_role or not title:
        return False
    role_words = {w for w in current_role.lower().split() if len(w) > 2}
    title_words = {w for w in title.lower().split() if len(w) > 2}
    return len(role_words.intersection(title_words)) > 0


def _extract_known_skills_from_text(text: str, known_skills: set[str]) -> set[str]:
    if not text:
        return set()
    lowered = text.lower()
    return {skill for skill in known_skills if skill in lowered}


def _get_role_category(role: str | None) -> str:
    """Extract role category from job title or role."""
    if not role:
        return "unknown"
    
    role_lower = role.lower()
    
    # Define role categories
    categories = {
        "data": ["data scientist", "data analyst", "data engineer"],
        "backend": ["backend", "server", "api"],
        "frontend": ["frontend", "ui", "ux", "web development"],
        "fullstack": ["full stack", "fullstack"],
        "devops": ["devops", "infrastructure", "cloud"],
        "ml": ["machine learning", "ml engineer", "deep learning"],
        "pm": ["product manager", "product owner", "pm"],
        "qa": ["qa", "qe", "quality assurance", "test"],
        "intern": ["intern"],
        "design": ["designer", "design"],
    }
    
    for category, keywords in categories.items():
        if any(kw in role_lower for kw in keywords):
            return category
    
    return "general"


def _role_category_match_score(resume_role: str | None, job_title: str | None) -> float:
    """
    Score based on role category match. 
    Penalizes significant mismatches (e.g., Data Scientist applying for PM).
    Returns 0-20 points.
    """
    if not resume_role or not job_title:
        return 10.0  # Neutral if roles not specified
    
    resume_category = _get_role_category(resume_role)
    job_category = _get_role_category(job_title)
    
    # Exact category match
    if resume_category == job_category and resume_category != "unknown":
        return 20.0
    
    # Allow some transitions
    # Data realm can transition: data scientist <-> data engineer <-> ml engineer <-> analyst
    data_realm = {"data", "ml"}
    if resume_category in data_realm and job_category in data_realm:
        return 15.0
    
    # Development realm: backend <-> fullstack <-> frontend (less ideal)
    dev_realm = {"backend", "frontend", "fullstack"}
    if resume_category in dev_realm and job_category in dev_realm:
        return 12.0
    
    # Different specialization (e.g., Data Scientist -> PM or Backend)
    # This should be penalized significantly
    return 2.0


async def recommend_jobs_for_user(db: AsyncSession, user_id: int, limit: int = 10):
    resume_result = await db.execute(
        select(Resume)
        .where(Resume.user_id == user_id)
        .order_by(Resume.uploaded_at.desc())
        .limit(1)
    )
    latest_resume = resume_result.scalars().first()

    if not latest_resume:
        return []

    # Get resume data
    db_resume_skills_query = await db.execute(
        select(Skill.name)
        .join(ResumeSkill, ResumeSkill.skill_id == Skill.skill_id)
        .where(ResumeSkill.resume_id == latest_resume.resume_id)
    )
    db_resume_skills = set(db_resume_skills_query.scalars().all())

    parsed_skills = set()
    parsed_role = None
    parsed_exp = None
    parsed_education = None
    if latest_resume.parsed_json:
        parsed_skills = set(latest_resume.parsed_json.get("skills", []))
        parsed_role = latest_resume.parsed_json.get("current_role")
        parsed_exp = latest_resume.parsed_json.get("experience_years")
        parsed_education = latest_resume.parsed_json.get("education_level")

    resume_skills = _normalize_skill_set(db_resume_skills.union(parsed_skills))
    resume_exp = _safe_float(latest_resume.experience_yrs, _safe_float(parsed_exp, 0.0))

    known_skills_result = await db.execute(select(Skill.name))
    known_skills = {
        (name or "").strip().lower()
        for name in known_skills_result.scalars().all()
        if (name or "").strip()
    }

    jobs_result = await db.execute(
        select(JobPosting)
        .options(
            joinedload(JobPosting.company),
            selectinload(JobPosting.job_skills).joinedload(JobSkill.skill),
        )
        .where(JobPosting.is_active == True)
    )
    active_jobs = jobs_result.scalars().all()

    recommendations = []

    for job in active_jobs:
        # Separate required and preferred skills
        required_skill_names = set()
        preferred_skill_names = set()
        
        for job_skill in job.job_skills:
            if job_skill.skill and job_skill.skill.name:
                skill_name = (job_skill.skill.name or "").strip().lower()
                if job_skill.is_required:
                    required_skill_names.add(skill_name)
                else:
                    preferred_skill_names.add(skill_name)
        
        # Extract from description if no required skills defined
        description_skill_names = set()
        if not required_skill_names:
            company_description = (job.company.description or "") if job.company else ""
            description_skill_names = _extract_known_skills_from_text(
                f"{job.description or ''}\n{company_description}", known_skills
            )
            required_skill_names = description_skill_names

        # Calculate skill matches (exact + partial)
        exact_matched_required = resume_skills.intersection(required_skill_names)
        partial_matched_required = {
            skill for skill in required_skill_names 
            if skill not in exact_matched_required and _partial_skill_match(resume_skills, skill)
        }
        matched_required = sorted(exact_matched_required.union(partial_matched_required))
        missing_required = sorted(required_skill_names.difference(exact_matched_required).difference(partial_matched_required))
        
        # Preferred skills (bonus points)
        matched_preferred = sorted(resume_skills.intersection(preferred_skill_names))
        
        # IMPROVED SKILL SCORING (0-40 points)
        # Core required skills: heavier weight
        if required_skill_names:
            exact_ratio = len(exact_matched_required) / len(required_skill_names)
            partial_ratio = len(partial_matched_required) / len(required_skill_names)
            skill_component = (exact_ratio * 35.0) + (partial_ratio * 5.0)  # Partial skills worth less
        else:
            # When no required skills defined, use lower base score (force role category matching to be primary)
            skill_component = 8.0
        
        # Bonus for matched preferred skills
        if preferred_skill_names:
            preferred_bonus = min(5.0, (len(matched_preferred) / len(preferred_skill_names)) * 5.0)
            skill_component += preferred_bonus

        # Fine-grained evidence bonus helps break ties when many jobs are close.
        skill_evidence_bonus = min(4.0, (len(matched_required) * 0.8) + (len(matched_preferred) * 0.4))
        
        # IMPROVED EXPERIENCE SCORING (0-30 points)
        exp_min = _safe_float(job.experience_min, 0.0)
        exp_max = _safe_float(job.experience_max, 20.0) if hasattr(job, 'experience_max') else 20.0
        
        if resume_exp >= exp_min:
            if resume_exp > exp_max:
                # Over-qualified: slight penalty to encourage right-fit roles
                experience_component = 28.0 - ((resume_exp - exp_max) * 0.5)
            else:
                # Perfect fit: full points
                experience_component = 30.0
        elif exp_min > 0:
            # Under-qualified: graduated penalty
            gap = exp_min - resume_exp
            experience_component = max(10.0, 30.0 - (gap * 8.0))
        else:
            experience_component = 25.0
        
        experience_component = max(0.0, min(30.0, experience_component))
        
        # ROLE CATEGORY MATCHING (0-20 points) - PRIMARY CHECK FOR ROLE FIT
        role_category_score = _role_category_match_score(parsed_role, job.title)
        _, is_progression_fit = _role_seniority_score(parsed_role, job.title)  # For progression fit info only
        role_keyword_bonus = 3.0 if _keyword_overlap(parsed_role, job.title) else 0.0
        
        # EDUCATION MATCHING (0-5 points)
        education_score = _education_match_score(parsed_education, job.job_type)
        
        # DESCRIPTION SIGNAL BONUS (0-5 points)
        if description_skill_names:
            description_overlap = len(resume_skills.intersection(description_skill_names))
            description_bonus = min(5.0, (description_overlap / max(1, len(description_skill_names))) * 5.0)
        else:
            description_bonus = 0.0
        
        # FINAL SCORE CALCULATION (0-100 points)
        # Breakdown: Skills(40) + Experience(30) + Role_Category(20) + Education(5) + Description(5) = 100
        final_score = round(min(100.0, 
            skill_component + 
            experience_component + 
            role_category_score + 
            role_keyword_bonus +
            education_score + 
            description_bonus +
            skill_evidence_bonus
        ), 2)
        
        # Build detailed reasons
        reasons = []
        
        # Skill breakdown
        if required_skill_names:
            if exact_matched_required:
                reasons.append(f"Exact match: {len(exact_matched_required)}/{len(required_skill_names)} core skills")
            if partial_matched_required:
                reasons.append(f"Partial match: {len(partial_matched_required)} additional skill overlap")
            if missing_required:
                reasons.append(f"Missing: {', '.join(list(missing_required)[:2])}{'...' if len(missing_required) > 2 else ''}")
        else:
            reasons.append("No specific skills required for this role")
        
        # Experience fit
        if resume_exp >= exp_min:
            if resume_exp > (exp_max or 20.0):
                reasons.append(f"Over-qualified: You have {resume_exp:.1f} years vs {exp_min:.1f} required")
            else:
                reasons.append(f"Experience match: {resume_exp:.1f} years (required: {exp_min:.1f})")
        else:
            reasons.append(f"Experience gap: You have {resume_exp:.1f} years, role needs {exp_min:.1f}")
        
        # Role fit
        if is_progression_fit:
            reasons.append("Role progression: Natural career advancement opportunity")
        else:
            reasons.append("Role change: Different specialization")
        
        # Education
        if parsed_education and parsed_education.lower() != "not specified":
            reasons.append(f"Education level: {parsed_education}")

        recommendations.append(
            {
                "resume_id": latest_resume.resume_id,
                "job_id": job.job_id,
                "title": job.title,
                "company_name": job.company.name if job.company else None,
                "location": job.location,
                "job_type": job.job_type,
                "score": final_score,
                "matched_skills": matched_required,
                "missing_skills": missing_required,
                "match_reasons": reasons,
            }
        )

    filtered_recommendations = [
        item for item in recommendations if item["score"] >= MIN_MATCH_SCORE
    ]
    filtered_recommendations.sort(key=lambda item: item["score"], reverse=True)
    return filtered_recommendations[:limit]

