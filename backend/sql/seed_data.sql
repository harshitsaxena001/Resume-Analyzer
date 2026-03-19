-- Sample Seed Data
INSERT INTO users (full_name, email, password_hash, role) VALUES
('Admin User', 'admin@skillsync.com', '$2b$12$K...', 'admin'),
('Recruiter One', 'recruiter1@techcorp.com', '$2b$12$K...', 'recruiter'),
('John Doe', 'john.doe@example.com', '$2b$12$K...', 'jobseeker');

INSERT INTO companies (recruiter_id, name, industry, location) VALUES
(2, 'Tech Corp', 'Software', 'San Francisco, CA');

INSERT INTO skills (name, category) VALUES
('Python', 'Programming'),
('SQL', 'Database'),
('React', 'Frontend');

INSERT INTO job_postings (company_id, title, description, location, job_type, is_active) VALUES
(1, 'Senior Backend Engineer', 'Looking for a Python expert with SQL experience.', 'Remote', 'full-time', TRUE);

INSERT INTO job_skills (job_id, skill_id, is_required) VALUES
(1, 1, TRUE),
(1, 2, TRUE);
