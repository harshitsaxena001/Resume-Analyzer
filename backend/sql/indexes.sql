-- Full-text search indexes
CREATE INDEX idx_resumes_search   ON resumes        USING GIN (search_vector);
CREATE INDEX idx_jobs_search      ON job_postings   USING GIN (search_vector);

-- Foreign key / lookup indexes
CREATE INDEX idx_resume_skills_resume ON resume_skills (resume_id);
CREATE INDEX idx_resume_skills_skill  ON resume_skills (skill_id);
CREATE INDEX idx_job_skills_job       ON job_skills    (job_id);
CREATE INDEX idx_match_resume         ON match_scores  (resume_id);
CREATE INDEX idx_match_score          ON match_scores  (score DESC);
CREATE INDEX idx_applications_user    ON applications  (user_id);
CREATE INDEX idx_jobs_active          ON job_postings  (is_active) WHERE is_active = TRUE;
