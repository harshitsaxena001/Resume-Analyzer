from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, resume, jobs, recommendations, applications

app = FastAPI(
    title="SkillSync AI Resume Analyzer API",
    description="Backend API for SkillSync AI Resume Analyzer & Job Recommendation System",
    version="1.0.0"
)

# Configure CORS
origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])

@app.get("/")
async def root():
    return {"message": "Welcome to SkillSync API"}

