from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "SkillSync AI Resume Analyzer API"
    VERSION: str = "1.0.0"

    # Database Settings
    DATABASE_URL: str

    # JWT Authentication Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Gemini API Integration
    GEMINI_API_KEY: str

    # Storage
    UPLOAD_DIR: str = "./uploads"

    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "https://resume-analyzer-iota-murex.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]               
    CORS_ORIGIN_REGEX: str = r"^https?://((?:[a-zA-Z0-9-]+\.)*vercel\.app|localhost|127\.0\.0\.1|10(?:\.\d{1,3}){3}|172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){2})(?::\d+)?$"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
