# Product Requirements Document (PRD)

## AI Resume Analyser & Job Recommendation System

**Version:** 1.0  
**Stack:** FastAPI · NeonDB (PostgreSQL) · Python · React (Frontend TypeScript)  
**Project Type:** DBMS Academic Project  
**Date:** March 2026
# SkillSync AI

## Full Project Report and Product Requirements Document (PRD)

## 1. Executive Summary

SkillSync AI is a full-stack recruitment intelligence platform that connects jobseekers and recruiters through AI-assisted resume extraction, role-fit scoring, and direct job application workflows. The system combines FastAPI, PostgreSQL (NeonDB), and a React frontend to deliver an end-to-end product where users can:

- register/login securely,
- upload resumes for AI parsing,
- get ranked job recommendations,
- apply to jobs with optional cover letters,
- track and manage applications.

The project is designed for clean API layering, role-based authorization, and scalable matching logic that can evolve from rule-based heuristics to more advanced ranking models.

## 2. Product Vision and Objectives

### 2.1 Vision

Create a reliable and explainable hiring assistant that improves candidate-job fit quality and shortens application turnaround time.

### 2.2 Primary Objectives

- Provide a frictionless resume upload and structured profile extraction experience.
- Offer high-signal recommendations from active job postings.
- Ensure recruiters can create/manage jobs and review candidate applications quickly.
- Maintain strict access controls for user and recruiter data.

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
### 2.3 Success Indicators

- Resume upload to parsed profile completion time.
- Recommendation relevance (click-through and apply-through rates).
- Duplicate application prevention rate.
- API reliability and error rates.

## 3. Scope

### 3.1 In Scope

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
- JWT-based auth (register/login/me).
- Resume upload, parsing, storage, and listing.
- Job CRUD (create/list/detail/delete).
- Recommendation API for authenticated users.
- Application submission and status updates.

### 3.2 Out of Scope (Current Version)

- Multi-tenant organization isolation.
- Real-time recruiter chat.
- Interview scheduling automation.
- Payment/billing flows.

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
### 4.1 High-Level Architecture

- Frontend (React + Vite + TypeScript)
  - Responsible for UI, auth session handling, API integration.
- Backend API (FastAPI)
  - Router layer for endpoint contracts.
  - Service layer for domain logic.
  - Middleware for JWT auth and role checks.
- Database (PostgreSQL/NeonDB)
  - Normalized relational schema with join tables for skills and applications.
- AI Integration (Google Gemini)
  - Resume extraction using model call with strict JSON output expectation.
  - Heuristic fallback parser for resilience.

### 4.2 Backend Layered Design

- Router Layer (`app/routers`)
  - Handles request validation, dependency injection, and HTTP status management.
- Service Layer (`app/services`)
  - Contains core business rules: auth, resume processing, matching, applications.
- Model Layer (`app/models`)
  - SQLAlchemy ORM models and relationships.
- Schema Layer (`app/schemas`)
  - Pydantic request/response contracts.
- Utility Layer (`app/utils`)
  - JWT helpers, PDF text extraction utilities.
- Middleware Layer (`app/middleware`)
  - Current-user resolution and role-backed route security.

### 4.3 Request Lifecycle

1. Frontend sends request with token from localStorage.
2. FastAPI dependency graph resolves DB session and auth middleware.
3. Router validates payload and calls service method.
4. Service executes DB queries and business rules.
5. Router returns schema-validated response.
6. Frontend updates state and UI.

## 5. Core Functional Workflows

### 5.1 Authentication Workflow

1. User registers with name/email/password/role.
2. Password is hashed in auth service.
3. User logs in using OAuth2 password flow endpoint.
4. JWT includes `email`, `user_id`, and `role` claims.
5. Frontend stores token and injects `Authorization: Bearer <token>` on API calls.
6. Protected routes resolve current user from token.

### 5.2 Resume Upload and Parsing Workflow

1. Authenticated jobseeker uploads PDF.
2. Backend validates extension (`.pdf`) and stores file under upload directory.
3. PDF parser extracts raw text.
4. AI service sends prompt to Gemini with strict JSON schema requirements.
5. On model failure/unavailable response:
   - fallback parser extracts name/email/phone/skills/experience heuristically.
6. Parsed profile is stored in `resumes` with `parsed_json` snapshot.
7. Skills are normalized and deduplicated.
8. Existing skills are reused; missing skills are inserted.
9. Resume-to-skill mappings are stored in `resume_skills`.

### 5.3 Job Management Workflow

1. Recruiter/admin submits job payload.
2. Authorization gate rejects non-recruiter roles.
3. Job posting row inserted and associated with company.
4. Skills mapped through `job_skills` with `is_required` marker.
5. Public job listing endpoint serves active jobs.
6. Search endpoint filters by query term.

### 5.4 Recommendation Workflow

1. User requests recommendations (`/recommendations/user/me`).
2. Service loads latest user resume.
3. Service loads active jobs and related required/preferred skills.
4. Match score computed using weighted components:
   - skill overlap and partial skill similarity,
   - experience band fit,
   - role progression fit,
   - role category compatibility,
   - education appropriateness.
5. Jobs below minimum threshold are excluded.
6. Remaining jobs sorted by score and returned.

### 5.5 Application Workflow

1. User opens job detail and submits application (optional cover letter).
2. Backend checks:
   - job exists,
   - duplicate `(user_id, job_id)` does not exist,
   - selected resume belongs to same user when provided.
3. New row inserted in `applications` with default status `applied`.
4. Jobseeker can view own applications.
5. Recruiter/admin can view applications for a job.
6. Recruiter/admin updates application status through patch endpoint.

## 6. API Surface (Backend)

### 6.1 Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### 6.2 Resume

- `POST /resume/upload`
- `GET /resume/{resume_id}`
- `GET /resume/user/{user_id}`
- `DELETE /resume/{resume_id}`

### 6.3 Jobs

- `POST /jobs/`
- `GET /jobs/`
- `GET /jobs/search?q=...`
- `GET /jobs/{job_id}`
- `DELETE /jobs/{job_id}`

### 6.4 Recommendations

- `GET /recommendations/user/me?limit=10`

### 6.5 Applications

- `POST /applications/apply`
- `GET /applications/user/{user_id}`
- `GET /applications/job/{job_id}`
- `PATCH /applications/{app_id}/status`

## 7. Database Report

### 7.1 Database Engine and Patterns

- Engine: PostgreSQL (NeonDB).
- ORM: SQLAlchemy Async.
- Migrations: Alembic.
- Important patterns:
  - `ON DELETE CASCADE` for ownership-driven cleanup,
  - `ON DELETE SET NULL` where historical record retention is needed,
  - unique constraints to prevent duplicate user applications.

### 7.2 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
      USERS ||--o{ RESUMES : uploads
      USERS ||--o{ APPLICATIONS : submits
      USERS ||--o{ COMPANIES : manages

      COMPANIES ||--o{ JOB_POSTINGS : owns

      JOB_POSTINGS ||--o{ JOB_SKILLS : requires
      SKILLS ||--o{ JOB_SKILLS : tagged_as

      RESUMES ||--o{ RESUME_SKILLS : contains
      SKILLS ||--o{ RESUME_SKILLS : listed_as

      JOB_POSTINGS ||--o{ APPLICATIONS : receives
      RESUMES ||--o{ APPLICATIONS : references

      USERS {
         int user_id PK
         string full_name
         string email UK
         text password_hash
         string role
         datetime created_at
         datetime updated_at
      }

      COMPANIES {
         int company_id PK
         int recruiter_id FK
         string name
         string logo_url
         string industry
         string location
         string website
         text description
         datetime created_at
      }

      JOB_POSTINGS {
         int job_id PK
         int company_id FK
         string title
         text description
         string location
         string job_type
         numeric experience_min
         numeric experience_max
         int salary_min
         int salary_max
         bool is_active
         datetime posted_at
         datetime expires_at
      }

      SKILLS {
         int skill_id PK
         string name UK
         string category
         datetime created_at
      }

      JOB_SKILLS {
         int id PK
         int job_id FK
         int skill_id FK
         bool is_required
      }

      RESUMES {
         int resume_id PK
         int user_id FK
         string file_name
         text file_path
         text raw_text
         jsonb parsed_json
         numeric experience_yrs
         string education_level
         string current_role
         string location
         numeric overall_score
         datetime uploaded_at
         datetime updated_at
      }

      RESUME_SKILLS {
         int id PK
         int resume_id FK
         int skill_id FK
         string proficiency
         numeric years_exp
      }

      APPLICATIONS {
         int application_id PK
         int user_id FK
         int job_id FK
         int resume_id FK
         text cover_letter
         string status
         datetime applied_at
         datetime updated_at
      }
```

### 7.3 Data Dictionary

#### `users`

- Stores platform identities.
- `email` is unique and indexed.
- `role` controls access (`jobseeker`, `recruiter`, `admin`).

#### `companies`

- Recruiter-managed company profiles.
- `recruiter_id` uses `SET NULL` on user deletion for record survivability.

#### `job_postings`

- Active role listings.
- `is_active` indexed for fast filtering.
- Search vector column available for PostgreSQL full-text search evolution.

#### `skills`

- Canonical skill master table.
- Unique name prevents duplicate taxonomies.

#### `job_skills`

- Many-to-many bridge between jobs and skills.
- `is_required` differentiates must-have vs nice-to-have.

#### `resumes`

- Uploaded file metadata and extracted profile data.
- `parsed_json` preserves full AI extraction payload.

#### `resume_skills`

- Many-to-many bridge between resumes and skills.
- Carries proficiency and years-of-experience qualifiers.

#### `applications`

- Candidate submissions to jobs.
- Constraint `uq_applications_user_job` enforces one application per user per job.

### 7.4 Referential Integrity Rules

- Deleting a user cascades their resumes and applications.
- Deleting a job cascades related job_skills and applications.
- Deleting a resume sets referenced `applications.resume_id` to null.
- Deleting a skill cascades bridge table rows.

## 8. Security Architecture

### 8.1 Authentication and Authorization

- JWT bearer token on protected endpoints.
- Middleware resolves current user from token claims.
- Role checks are enforced at router level (recruiter/admin restrictions).

### 8.2 Data Protection Controls

- Password hashing before persistence.
- Input validation through Pydantic schemas.
- Restricted file type acceptance for resume uploads (`.pdf`).

### 8.3 Abuse and Integrity Protection

- Duplicate applications blocked via both logic check and DB unique constraint.
- Resume ownership checks prevent cross-user resume misuse.

## 9. Error Handling and Resilience

- Layered exception handling in routers and services.
- Explicit HTTP error mapping (400/401/403/404/409/422/500).
- AI parser fallback ensures platform continuity if external model call fails.

## 10. Frontend Workflow Summary

### 10.1 Session and API Integration

- Auth context stores user session state.
- Axios client attaches JWT automatically.

### 10.2 Core Screens and Journey

- Home and marketing sections.
- Auth modal for sign-in/sign-up.
- Dashboard for resumes and recommendations.
- Jobs list and detail pages.
- Job details application modal with apply flow.

### 10.3 UX Feedback States

- Loading states for async data requests.
- Success confirmation after application submit.
- Error toasts/messages for API failures.

## 11. Backend Operational Workflow (Runbook)

1. Configure `.env` values (DB URL, secret key, Gemini key).
2. Create Python virtual environment and install requirements.
3. Run Alembic migrations to sync schema.
4. Start FastAPI app (`uvicorn main:app --reload`).
5. Start frontend Vite server.
6. Validate key paths:
   - register/login,
   - upload resume,
   - fetch recommendations,
   - apply to job.

## 12. Performance and Scalability Notes

- Async SQLAlchemy sessions reduce request blocking.
- Relationship loading strategies in matching service reduce N+1 risk.
- Indexed foreign keys support joins on large datasets.
- Recommendation scoring is deterministic and can be parallelized or cached in future.

## 13. Risks and Mitigations

- AI output inconsistency: mitigated by schema parsing + fallback extraction.
- Data drift in skill naming: mitigated by normalization and canonical skill table.
- Unauthorized data access: mitigated by route-level role checks and ownership checks.
- Duplicate submissions: mitigated by uniqueness constraint and pre-insert checks.

## 14. Known Gaps and Improvement Opportunities

- Add recruiter ownership validation on job deletion/update.
- Add audit trails for status transitions.
- Add pagination and filtering to applications endpoints.
- Add observability stack (structured logs, metrics, trace IDs).
- Add automated tests for recommendation scoring edge cases.

## 15. Release Readiness Checklist

- Environment variables configured and verified.
- Migrations applied successfully.
- Auth, resume, jobs, recommendations, applications endpoints smoke-tested.
- Seed/import data loaded for demo environments.
- Frontend-to-backend integration verified with valid JWT flow.

## 16. Conclusion

SkillSync AI already contains a strong foundation for AI-assisted hiring workflows with clear separation of concerns, robust relational modeling, and practical recommendation logic. With focused improvements in test coverage, observability, and recruiter governance rules, the project is well-positioned for production hardening and scale.
