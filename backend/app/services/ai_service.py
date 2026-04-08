from google import genai
import json
import re
from app.config import settings
from app.schemas.resume import ResumeParsedData


def _extract_first_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else "unknown@example.com"


def _extract_phone(text: str) -> str | None:
    match = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}", text)
    return match.group(0) if match else None


def _extract_experience_years(text: str) -> float:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)", text, flags=re.IGNORECASE)
    if not matches:
        return 0.0
    try:
        return max(float(m) for m in matches)
    except ValueError:
        return 0.0


def _extract_education(text: str) -> str:
    lowered = text.lower()
    if "phd" in lowered:
        return "PhD"
    if "m.tech" in lowered or "mtech" in lowered or "master" in lowered or "mba" in lowered:
        return "Masters"
    if "b.tech" in lowered or "btech" in lowered or "bachelor" in lowered or "b.e" in lowered:
        return "Bachelors"
    if "diploma" in lowered:
        return "Diploma"
    return "Not specified"


def _extract_skills(text: str) -> list[str]:
    known_skills = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C", "SQL", "FastAPI", "Django", "Flask",
        "React", "Node.js", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "HTML", "CSS",
        "MongoDB", "PostgreSQL", "MySQL", "Pandas", "NumPy", "Machine Learning", "TensorFlow", "PyTorch",
    ]
    lowered = text.lower()
    found: list[str] = []
    for skill in known_skills:
        token = skill.lower()
        if token in {"c", "sql", "aws", "gcp", "git", "css", "html"}:
            pattern = rf"\b{re.escape(token)}\b"
            if re.search(pattern, lowered):
                found.append(skill)
            continue
        if token == "c++":
            if "c++" in lowered:
                found.append(skill)
            continue
        if token in lowered:
            found.append(skill)
    return found[:20]


def _extract_full_name(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if "@" in cleaned or len(cleaned) > 80:
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,60}", cleaned):
            return cleaned
    return "Unknown Candidate"


def _extract_current_role(text: str) -> str:
    lowered = text.lower()
    role_markers = [
        "software engineer", "frontend developer", "backend developer", "full stack developer",
        "data analyst", "data scientist", "devops engineer", "machine learning engineer", "intern",
    ]
    for marker in role_markers:
        if marker in lowered:
            return marker.title()
    return "Not specified"


def _fallback_parse_resume(raw_text: str) -> ResumeParsedData:
    full_name = _extract_full_name(raw_text)
    email = _extract_first_email(raw_text)
    phone = _extract_phone(raw_text)
    skills = _extract_skills(raw_text)
    experience_years = _extract_experience_years(raw_text)
    education_level = _extract_education(raw_text)
    current_role = _extract_current_role(raw_text)

    # Heuristic score so downstream UI can still display a meaningful value.
    score = min(95.0, 45.0 + len(skills) * 4.0 + min(experience_years, 8.0) * 2.0)

    return ResumeParsedData(
        full_name=full_name,
        email=email,
        phone=phone,
        current_role=current_role,
        experience_years=experience_years,
        education_level=education_level,
        skills=skills,
        work_experience=[],
        certifications=[],
        overall_score=round(score, 1),
    )

async def parse_resume(raw_text: str) -> ResumeParsedData:
    """Parse resume with Gemini - single API call."""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""You are a resume parser. Extract the following from the resume text below and return ONLY valid JSON:
{{
  "full_name": "",
  "email": "",
  "phone": "",
  "current_role": "",
  "experience_years": 0.0,
  "education_level": "",
  "skills": [],
  "work_experience": [{{"company": "", "role": "", "duration": ""}}],
  "certifications": [],
  "overall_score": 0.0
}}
Resume Text: {raw_text}
"""

    model_candidates = ["gemini-2.5-flash", "gemini-2.0-flash"]
    errors: list[str] = []

    for model_name in model_candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            content = (response.text or "").strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()

            parsed_dict = json.loads(content)
            return ResumeParsedData(**parsed_dict)
        except Exception as e:
            errors.append(f"{model_name}: {e}")
            continue

    # Fallback: Use heuristic parsing when Gemini unavailable
    if raw_text and raw_text.strip():
        return _fallback_parse_resume(raw_text)

    raise ValueError(
        "Could not extract text from the PDF. Please upload a text-based PDF file."
    )

