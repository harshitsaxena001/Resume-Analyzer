-- Top job matches per resume
CREATE OR REPLACE VIEW vw_top_matches AS
SELECT
    ms.resume_id,
    ms.job_id,
    jp.title,
    c.name AS company,
    ms.score,
    ms.matched_skills,
    ms.missing_skills
FROM match_scores ms
JOIN job_postings jp ON ms.job_id = jp.job_id
JOIN companies    c  ON jp.company_id = c.company_id
WHERE jp.is_active = TRUE
ORDER BY ms.score DESC;

-- Resume skill summary
CREATE OR REPLACE VIEW vw_resume_skill_summary AS
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
