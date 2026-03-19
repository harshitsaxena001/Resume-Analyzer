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

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
