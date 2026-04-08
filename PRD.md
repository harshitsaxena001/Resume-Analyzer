# Product Requirements Document (PRD)

## AI Resume Analyser & Job Recommendation System

**Version:** 1.0  
**Stack:** FastAPI · NeonDB (PostgreSQL) · Python · React (Frontend TypeScript)  
**Project Type:** DBMS Academic Project  
**Date:** March 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Objectives](#2-goals--objectives)
3. [Tech Stack](#3-tech-stack)
4. [System Architecture](#4-system-architecture)
5. [Database Schema (NeonDB)](#5-database-schema-neondb)
6. [Project Folder Structure](#6-project-folder-structure)
7. [API Endpoints](#7-api-endpoints)
8. [Core Features & Modules](#8-core-features--modules)
9. [AI/ML Pipeline](#9-aiml-pipeline)
10. [Frontend Pages](#10-frontend-pages)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [Environment & Configuration](#12-environment--configuration)
13. [Non-Functional Requirements](#13-non-functional-requirements)

---

## 1. Project Overview

The **AI Resume Analyser & Job Recommendation System** is a full-stack web application that allows job seekers to upload their resumes, receive AI-powered analysis and skill-gap feedback, and get personalised job recommendations matched to their profile. Recruiters can post jobs and view matched candidate profiles.

This project demonstrates advanced DBMS concepts including relational schema design, complex SQL queries, indexing strategies, stored procedures/views, and full-text search — all hosted on NeonDB (serverless PostgreSQL).

---

## 2. Goals & Objectives

### Primary Goals

- Parse and analyse resumes using AI (Google Gemini API)
- Match job seekers to relevant job postings using a dynamic scoring algorithm
- Provide skill-gap analysis and improvement suggestions
- Showcase DBMS concepts: normalisation, joins, indexing, views, triggers

### Academic DBMS Concepts Demonstrated

- Entity-Relationship (ER) modelling with 8 tables
- 3NF-normalised schema design
- Complex multi-table JOINs in recommendation queries
- Full-text search using PostgreSQL `tsvector` / `tsquery`
- Database views for resume skill summaries
- Indexes on high-query columns (skills, job_title, user_id)
- Transactions for atomic resume upload + parsing operations

---

## 3. Tech Stack

| Layer             | Technology                                                       |
| ----------------- | ---------------------------------------------------------------- |
| Backend Framework | FastAPI (Python 3.11+)                                           |
| Database          | NeonDB (Serverless PostgreSQL)                                   |
| ORM               | SQLAlchemy 2.0 (async) + asyncpg driver                          |
| AI / NLP          | Google Gemini API (`google-genai`) for resume parsing & analysis |
| Resume Parsing    | PyMuPDF / pdfplumber (PDF extraction)                            |
| Auth              | JWT (python-jose) + bcrypt password hashing                      |
| File Storage      | Local `/uploads` dir                                             |
| Frontend          | React 19 + Vite + TypeScript + Custom CSS                        |
| HTTP Client       | Axios                                                            |
| Deployment        | Render / Railway (backend) + Vercel (frontend)                   |

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        FRONTEND                          │
│         React + Vite + TypeScript + Custom CSS           │
│   (Auth, Resume Upload, Dashboard, Job Listings)         │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP / REST (Axios)
                  ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                    │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │ Auth Router│  │Resume Router│  │  Jobs Router       │ │
│  └────────────┘  └─────┬──────┘  └────────────────────┘ │
│                        │                                 │
│              ┌─────────▼──────────┐                      │
│              │   AI Service       │                      │
│              │  (Gemini API)      │                      │
│              │  Resume Parsing    │                      │
│              │  Skill Extraction  │                      │
│              └─────────┬──────────┘                      │
│                        │                                 │
│              ┌─────────▼─────────┐                       │
│              │  Match Service    │                       │
│              │  Dynamic Scoring  │                       │
│              └─────────┬─────────┘                       │
│                        │                                 │
│              ┌─────────▼──────────┐                      │
│              │  SQLAlchemy ORM    │                      │
│              └─────────┬──────────┘                      │
└────────────────────────┼────────────────────────────────┘
```

oldString: ```text

### Primary Goals

- Parse and analyse resumes using AI (Claude API or similar)
- Match job seekers to relevant job postings using a scoring algorithm
- Provide skill-gap analysis and improvement suggestions
- Showcase DBMS concepts: normalisation, joins, indexing, views, triggers

### Academic DBMS Concepts Demonstrated

- Entity-Relationship (ER) modelling with 8+ tables
- 3NF-normalised schema design
- Complex multi-table JOINs in recommendation queries
- Full-text search using PostgreSQL `tsvector` / `tsquery`
- Database views for resume scoring summaries
- Triggers for auto-updating match scores
- Indexes on high-query columns (skills, job_title, user_id)
- Transactions for atomic resume upload + parsing operations

---

## 3. Tech Stack

| Layer             | Technology                                           |
| ----------------- | ---------------------------------------------------- |
| Backend Framework | FastAPI (Python 3.11+)                               |
| Database          | NeonDB (Serverless PostgreSQL)                       |
| ORM               | SQLAlchemy 2.0 (async) + asyncpg driver              |
| AI / NLP          | Claude API (Anthropic) for resume parsing & analysis |
| Resume Parsing    | PyMuPDF / pdfplumber (PDF extraction)                |
| Auth              | JWT (python-jose) + bcrypt password hashing          |
| File Storage      | Local `/uploads` dir (or Cloudinary for production)  |
| Frontend          | React + Vite + TailwindCSS                           |
| HTTP Client       | Axios                                                |
| Deployment        | Render / Railway (backend) + Vercel (frontend)       |

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        FRONTEND                          │
│              React + Vite + TailwindCSS                  │
│   (Auth, Resume Upload, Dashboard, Job Listings)         │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP / REST (Axios)
                  ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                    │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │ Auth Router│  │Resume Router│  │  Jobs Router       │ │
│  └────────────┘  └─────┬──────┘  └────────────────────┘ │
│                        │                                 │
│              ┌─────────▼──────────┐                      │
│              │   AI Service       │                      │
│              │  (Claude API)      │                      │
│              │  Resume Parsing    │                      │
│              │  Skill Extraction  │                      │
│              │  Match Scoring     │                      │
│              └─────────┬──────────┘                      │
│                        │                                 │
│              ┌─────────▼──────────┐                      │
│              │  SQLAlchemy ORM    │                      │
│              └─────────┬──────────┘                      │
└────────────────────────┼────────────────────────────────┘
```

                         │ asyncpg
                         ▼

┌─────────────────────────────────────────────────────────┐
│ NeonDB (PostgreSQL) │
│ │
│ users · resumes · skills · job_postings │
│ applications · companies · resume_skills · job_skills │
└─────────────────────────────────────────────────────────┘

```

---

## 5. Database Schema (NeonDB)

### 5.1 Entity-Relationship Overview

The database has **8 core tables** in 3NF:

```

users ──< resumes ──< resume_skills >── skills
│ │
└──< applications >── job_postings ──<─┘
│ job_skills
companies

````

---

### 5.2 Table Definitions (SQL)

```sql
-- 1. USERS
CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          VARCHAR(20) DEFAULT 'jobseeker' CHECK (role IN ('jobseeker', 'recruiter', 'admin')),
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP DEFAULT NOW()
);

-- 2. COMPANIES (for recruiters)
CREATE TABLE companies (
    company_id   SERIAL PRIMARY KEY,
    recruiter_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    name         VARCHAR(150) NOT NULL,
    industry     VARCHAR(100),
    location     VARCHAR(100),
    website      VARCHAR(255),
    description  TEXT,
    created_at   TIMESTAMP DEFAULT NOW()
);

-- 3. SKILLS (master list)
CREATE TABLE skills (
    skill_id   SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    category   VARCHAR(50),    -- e.g. 'Programming', 'Framework', 'Soft Skill'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. RESUMES
CREATE TABLE resumes (
    resume_id       SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    file_name       VARCHAR(255),
    file_path       TEXT,
    raw_text        TEXT,                  -- extracted plain text from PDF
    parsed_json     JSONB,                 -- AI-parsed structured data
    experience_yrs  NUMERIC(4,1),
    education_level VARCHAR(50),           -- e.g. 'B.Tech', 'M.Tech', 'PhD'
    current_role    VARCHAR(100),
    location        VARCHAR(100),
    overall_score   NUMERIC(4,1),          -- 0-100 AI quality score
    search_vector   TSVECTOR,              -- for full-text search
    uploaded_at     TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- 5. RESUME_SKILLS (junction: resume ↔ skills)
CREATE TABLE resume_skills (
    id             SERIAL PRIMARY KEY,
    resume_id      INTEGER NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
    skill_id       INTEGER NOT NULL REFERENCES skills(skill_id) ON DELETE CASCADE,
    proficiency    VARCHAR(20) DEFAULT 'intermediate'
                   CHECK (proficiency IN ('beginner', 'intermediate', 'expert')),
    years_exp      NUMERIC(3,1),
    UNIQUE(resume_id, skill_id)
);

-- 6. JOB_POSTINGS
CREATE TABLE job_postings (
    job_id          SERIAL PRIMARY KEY,
    company_id      INTEGER REFERENCES companies(company_id) ON DELETE SET NULL,
    title           VARCHAR(150) NOT NULL,
    description     TEXT NOT NULL,
    location        VARCHAR(100),
    job_type        VARCHAR(30) DEFAULT 'full-time'
                    CHECK (job_type IN ('full-time', 'part-time', 'internship', 'contract', 'remote')),
    experience_min  NUMERIC(3,1) DEFAULT 0,
    experience_max  NUMERIC(3,1),
    salary_min      INTEGER,
    salary_max      INTEGER,
    is_active       BOOLEAN DEFAULT TRUE,
    search_vector   TSVECTOR,
    posted_at       TIMESTAMP DEFAULT NOW(),
    expires_at      TIMESTAMP
);

-- 7. JOB_SKILLS (junction: job ↔ skills)
CREATE TABLE job_skills (
    id          SERIAL PRIMARY KEY,
    job_id      INTEGER NOT NULL REFERENCES job_postings(job_id) ON DELETE CASCADE,
    skill_id    INTEGER NOT NULL REFERENCES skills(skill_id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT TRUE,
    UNIQUE(job_id, skill_id)
);

-- 8. APPLICATIONS
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    job_id         INTEGER NOT NULL REFERENCES job_postings(job_id) ON DELETE CASCADE,
    resume_id      INTEGER REFERENCES resumes(resume_id) ON DELETE SET NULL,
    status         VARCHAR(30) DEFAULT 'applied'
                   CHECK (status IN ('applied', 'under_review', 'shortlisted', 'rejected', 'offered')),
    applied_at     TIMESTAMP DEFAULT NOW(),
    updated_at     TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);
````

---

### 5.3 Indexes

```sql
-- Full-text search indexes
CREATE INDEX idx_resumes_search   ON resumes        USING GIN (search_vector);
CREATE INDEX idx_jobs_search      ON job_postings   USING GIN (search_vector);

-- Foreign key / lookup indexes
CREATE INDEX idx_resume_skills_resume ON resume_skills (resume_id);
CREATE INDEX idx_resume_skills_skill  ON resume_skills (skill_id);
CREATE INDEX idx_job_skills_job       ON job_skills    (job_id);
CREATE INDEX idx_applications_user    ON applications  (user_id);
CREATE INDEX idx_jobs_active          ON job_postings  (is_active) WHERE is_active = TRUE;
```

---

### 5.4 Views

```sql
-- Resume skill summary
CREATE VIEW vw_resume_skill_summary AS
SELECT
    r.resume_id,
    u.full_name,
    u.email,
    r.current_role,
    r.experience_yrs,
    r.overall_score,
    ARRAY_AGG(s.name ORDER BY s.name) AS skills
FROM resumes r
JOIN users        u  ON r.user_id = u.user_id
JOIN resume_skills rs ON r.resume_id = rs.resume_id
JOIN skills       s  ON rs.skill_id = s.skill_id
GROUP BY r.resume_id, u.full_name, u.email, r.current_role, r.experience_yrs, r.overall_score;
```

---

### 5.5 Trigger

```sql
-- Auto-update updated_at on users table
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_resumes_updated
BEFORE UPDATE ON resumes
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

---

## 6. Project Folder Structure

```
ai-resume-analyser/
│
├── backend/
│   ├── main.py                     # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env                        # DB URL, API keys
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings (pydantic BaseSettings)
│   │   ├── database.py             # NeonDB async engine + session
│   │   │
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── skill.py
│   │   │   ├── job_posting.py
│   │   │   └── application.py
│   │   │
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job.py
│   │   │   └── match.py
│   │   │
│   │   ├── routers/                # FastAPI route handlers
│   │   │   ├── auth.py             # /auth/register, /auth/login
│   │   │   ├── resume.py           # /resume/upload, /resume/{id}
│   │   │   ├── jobs.py             # /jobs/, /jobs/{id}, /jobs/post
│   │   │   ├── recommendations.py  # /recommendations/user/me
│   │   │   └── applications.py     # /apply, /applications
│   │   │
│   │   ├── services/               # Business logic
│   │   │   ├── auth_service.py     # JWT, password hashing
│   │   │   ├── resume_service.py   # PDF extraction, DB save
│   │   │   ├── ai_service.py       # Gemini API calls
│   │   │   ├── match_service.py    # Dynamic Scoring algorithm
│   │   │   └── skill_service.py    # Skill normalisation
│   │   │
│   │   ├── utils/
│   │   │   ├── pdf_parser.py       # pdfplumber / PyMuPDF
│   │   │   └── jwt_handler.py
│   │   │
│   │   └── middleware/
│   │       └── auth_middleware.py  # JWT dependency
│   │
│   └── alembic/                    # DB migrations
│       ├── env.py
│       └── versions/
│
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   │
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css
│       │
│       ├── pages/
│       │   ├── Home.tsx
│       │   ├── Dashboard.tsx       # Resume metrics + top matched jobs
│       │   ├── Jobs.tsx            # Job search list
│       │   └── JobDetails.tsx      # Full job description
│       │
│       ├── components/
│       │   ├── Navbar.tsx
│       │   ├── AuthModal.tsx
│       │   ├── Hero.tsx
│       │   └── Features.tsx
│       │
│       ├── api/
│       │   └── client.ts           # Axios instance + interceptors
│       │
│       └── context/
│           └── AuthContext.tsx     # Context for auth state
│
├── sql/
│   ├── schema.sql                  # Full table definitions
│   ├── views.sql
│   ├── indexes.sql
│   └── seed_data.sql               # Sample companies, skills, jobs
│
└── README.md
```

---

## 7. API Endpoints

### Auth

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| POST   | `/auth/register` | Register new user        |
| POST   | `/auth/login`    | Login, returns JWT token |
| GET    | `/auth/me`       | Get current user info    |

### Resume

| Method | Endpoint                 | Description                  |
| ------ | ------------------------ | ---------------------------- |
| POST   | `/resume/upload`         | Upload PDF, trigger AI parse |
| GET    | `/resume/{resume_id}`    | Get parsed resume data       |
| GET    | `/resume/user/{user_id}` | All resumes of a user        |
| DELETE | `/resume/{resume_id}`    | Delete resume                |

### Jobs

| Method | Endpoint          | Description                      |
| ------ | ----------------- | -------------------------------- |
| GET    | `/jobs/`          | List all active jobs (paginated) |
| GET    | `/jobs/{job_id}`  | Get job details                  |
| POST   | `/jobs/`          | Post a new job (recruiter)       |
| PUT    | `/jobs/{job_id}`  | Update job listing               |
| DELETE | `/jobs/{job_id}`  | Remove job listing               |
| GET    | `/jobs/search?q=` | Full-text job search             |

### Recommendations

| Method | Endpoint                                          | Description                         |
| ------ | ------------------------------------------------- | ----------------------------------- |
| GET    | `/recommendations/user/me`                        | Top N matched jobs for current user |
| GET    | `/recommendations/skill-gap/{resume_id}/{job_id}` | Missing skills for a specific job   |

### Applications

| Method | Endpoint                        | Description                          |
| ------ | ------------------------------- | ------------------------------------ |
| POST   | `/applications/apply`           | Apply to a job                       |
| GET    | `/applications/user/{user_id}`  | All applications by user             |
| GET    | `/applications/job/{job_id}`    | All applicants for a job (recruiter) |
| PATCH  | `/applications/{app_id}/status` | Update application status            |

---

## 8. Core Features & Modules

### 8.1 Resume Upload & Parsing

1. User uploads a PDF file
2. Backend extracts raw text using `pdfplumber`
3. Raw text is sent to the Gemini API with a structured prompt
4. Gemini returns JSON with: name, email, skills, education, experience, certifications
5. Parsed data is stored in `resumes.parsed_json` and skills are inserted into `resume_skills`

### 8.2 AI Resume Scoring

- Gemini evaluates the resume and returns an `overall_score` (0–100) based on:
  - Clarity and structure
  - Quantified achievements
  - Keyword richness
  - Completeness

### 8.3 Dynamic Job Matching Algorithm

The match score between a resume and a job posting is calculated dynamically during queries based on multiple heuristics:

- **Skill Overlap Score:** Partial matching between resume and required job skills.
- **Experience Match Bonus:** Mapping between job seniority (junior, mid, senior) and candidate's role progression.
- **Education Match Bonus:** Aligning appropriate degree level to seniority of the role.
- **Role Category Match:** Categorizing candidates and jobs (e.g. backend, data, frontend) and assigning a heavy mapping weight.

### 8.4 Skill Gap Analysis

For a given resume ↔ job pair in memory, the system dynamically calculates:

- **Matched skills** – skills present in both resume and job
- **Missing required skills** – must-have skills the user lacks

### 8.5 Full-Text Search

Uses PostgreSQL `tsvector` and `GIN` index for fast keyword-based job and resume search:

```sql
SELECT * FROM job_postings
WHERE search_vector @@ to_tsquery('english', 'python & machine_learning');
```

---

## 9. AI/ML Pipeline

```
PDF Upload
    │
    ▼
Text Extraction (pdfplumber)
    │
    ▼
Prompt Engineering → Gemini API
    │  {
    │    "name": "...",
    │    "skills": ["Python", "SQL", ...],
    │    "experience": [...],
    │    "education": [...],
    │    "score": 78
    │  }
    ▼
Skill Normalisation (match to `skills` master table)
    │
    ▼
Insert into resumes + resume_skills
    │
    ▼
Return dynamically computed recommendations using matching algorithm on frontend request
```

**Gemini Prompt Template (Resume Parsing):**

```
You are a resume parser. Extract the following from the resume text below and return ONLY valid JSON:
{
  "full_name": "",
  "email": "",
  "phone": "",
  "current_role": "",
  "experience_years": 0.0,
  "education_level": "",
  "skills": [],
  "work_experience": [{"company": "", "role": "", "duration": ""}],
  "certifications": [],
  "overall_score": 0.0
}
Resume Text: {{raw_text}}
```

---

## 10. Frontend Pages

| Page        | Route        | Description                                       |
| ----------- | ------------ | ------------------------------------------------- |
| Home        | `/`          | Hero section, feature overview, CTA               |
| Jobs        | `/jobs`      | Paginated, searchable job list                    |
| Dashboard   | `/dashboard` | Resume metrics and dynamically matched top 5 jobs |
| Job Details | `/jobs/:id`  | Full job description + Apply button               |

_Note: Auth is handled primarily via an `AuthModal` rather than discrete routing pages._

---

## 11. Implementation Roadmap

### Phase 1 — Database & Backend Foundation (Week 1–2)

- [x] Set up NeonDB project, write `schema.sql`
- [x] Initialise FastAPI project, connect via asyncpg
- [x] Implement SQLAlchemy models for all 8 tables
- [x] Set up Alembic migrations
- [x] Implement auth routes (register, login, JWT)

### Phase 2 — Resume Pipeline (Week 2–3)

- [x] Build PDF upload endpoint (multipart/form-data)
- [x] Integrate pdfplumber for text extraction
- [x] Write Gemini API integration for resume parsing
- [x] Store parsed data + skills in DB
- [x] Build resume retrieval endpoints

### Phase 3 — Jobs & Matching (Week 3–4)

- [x] Seed skills master table + sample jobs
- [x] Build job posting CRUD endpoints
- [x] Implement dynamic match scoring logic in memory
- [x] Integrate full-text search with tsvector

### Phase 4 — Frontend (Week 4–5)

- [x] Scaffold React + Vite + TS project
- [x] Implement Auth Context and JWT storage
- [x] Build multi-purpose Auth Modal
- [x] Build Dashboard with score metrics and match cards
- [x] Build Job Listings and Job Detail pages

### Phase 5 — Polish & Demo Prep (Week 5–6)

- [x] Add seed data (jobs, users, resumes)
- [x] Wrap up documentation
- [ ] Final testing and bug fixes

---

## 12. Environment & Configuration

### `.env` (backend)

```env
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.neon.tech/neondb?sslmode=require
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=AIzaSy...
UPLOAD_DIR=./uploads
```

### `requirements.txt`

```
fastapi==0.110.0
uvicorn[standard]==0.29.0
sqlalchemy[asyncio]==2.0.29
asyncpg==0.29.0
alembic==1.13.1
python-multipart==0.0.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pdfplumber==0.11.0
google-genai==0.3.0
pydantic-settings==2.2.1
python-dotenv==1.0.1
```

---

## 13. Non-Functional Requirements

| Requirement          | Target                                       |
| -------------------- | -------------------------------------------- |
| API Response Time    | < 500ms for non-AI endpoints                 |
| Resume Parsing Time  | < 10 seconds (Gemini API-dependent)          |
| Database Connections | NeonDB connection pooling (min 2, max 10)    |
| File Upload Size     | Max 5MB per resume PDF                       |
| Auth Token Expiry    | 60 minutes (access token)                    |
| Concurrent Users     | Support 50 concurrent users (academic scope) |
| Code Coverage        | Core services > 70% unit test coverage       |

---

_PRD prepared for academic DBMS project submission. All AI integrations use the Google Gemini API. Database hosted on NeonDB (serverless PostgreSQL)._
