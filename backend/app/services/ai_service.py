from google import genai
import json
from app.config import settings
from app.schemas.resume import ResumeParsedData

async def parse_resume(raw_text: str) -> ResumeParsedData:
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
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        parsed_dict = json.loads(content)
        return ResumeParsedData(**parsed_dict)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        raise ValueError(f"Failed to parse resume using AI: {e}")
