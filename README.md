# SkillSync AI - AI Resume Analyser & Job Recommendation System

Full-stack web application for AI-powered resume analysis and job matching.

## Tech Stack

- **Backend:** FastAPI, NeonDB (PostgreSQL), Google Gemini AI
- **Frontend:** React, Vite, Vanilla CSS (Premium Aesthetic)

## Project Structure

- `/backend`: FastAPI application
- `/frontend`: Vite + React application

## Setup Instructions

### 1. Backend Setup

1. Navigate to `/backend`.
2. Create a `.env` file from `.env.example` and fill in your keys.
3. Create a virtual environment: `python -m venv venv`.
4. Activate it: `.\venv\Scripts\activate`.
5. Install dependencies: `pip install -r requirements.txt`.
6. Run migrations:
   ```bash
   alembic revision --autogenerate -m "Initial Schema"
   alembic upgrade head
   ```
7. Start server: `uvicorn main:app --reload`.

### Import Jobs From Unstop/Naukri/Internshala Exports

1. Put exported job files (CSV/JSON) inside `backend/imports/`.
2. Ensure each row contains at least title and company name. You can follow `backend/imports/jobs_import_template.csv`.
3. Run migration and import:

   ```bash
   cd backend
   alembic upgrade head

   python import_jobs_from_sources.py --source unstop --input imports/unstop_jobs.csv
   python import_jobs_from_sources.py --source naukri --input imports/naukri_jobs.csv
   python import_jobs_from_sources.py --source internshala --input imports/internshala_jobs.csv
   ```

4. To quickly add more companies and role diversity, generate dynamic jobs directly:

   ```bash
   cd backend
   python import_jobs_from_sources.py --source dynamic --count 120
   ```

### 2. Frontend Setup

1. Navigate to `/frontend`.
2. Install dependencies: `npm install`.
3. Start development server: `npm run dev`.

## Quick Start

You can use the `start_app.bat` script in the root directory to launch both servers simultaneously (requires two terminal windows or background process handling).
