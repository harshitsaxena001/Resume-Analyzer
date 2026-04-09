import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getJobs, type JobResponse } from "../api/jobs";
import {
  getMyRecommendations,
  type JobRecommendationResponse,
} from "../api/recommendations";
import { getUserResumes, type ResumeUploadResponse } from "../api/resume";
import { useAuth } from "../context/AuthContext";
import "./Dashboard.css";

type SkillCount = {
  skill: string;
  count: number;
};

const topSkillCounts = (items: string[], limit = 8): SkillCount[] => {
  const map = new Map<string, number>();
  for (const raw of items) {
    const skill = raw.trim();
    if (!skill) continue;
    map.set(skill, (map.get(skill) || 0) + 1);
  }
  return [...map.entries()]
    .map(([skill, count]) => ({ skill, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
};

const Dashboard = () => {
  const { user, isLoading } = useAuth();
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [recommendations, setRecommendations] = useState<
    JobRecommendationResponse[]
  >([]);
  const [latestResume, setLatestResume] = useState<ResumeUploadResponse | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const firstName = user?.full_name?.trim()?.split(" ")[0] || "there";

  useEffect(() => {
    if (isLoading) return;
    if (!user) {
      setLoading(false);
      return;
    }

    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");
        const [jobData, recData, resumeData] = await Promise.all([
          getJobs(0, 200),
          getMyRecommendations(20),
          getUserResumes(user.user_id),
        ]);
        setJobs(jobData);
        setRecommendations(recData);
        // Get the latest resume
        if (resumeData.length > 0) {
          setLatestResume(resumeData[0]);
        }
      } catch (err: any) {
        const detail = err?.response?.data?.detail;
        setError(detail || "Unable to load dashboard insights right now.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [user, isLoading]);

  const trendingSkills = useMemo(() => {
    const allRequiredSkills = jobs.flatMap((job) =>
      (job.job_skills || [])
        .filter((jobSkill) => jobSkill.is_required)
        .map((jobSkill) => jobSkill.skill.name),
    );
    return topSkillCounts(allRequiredSkills, 10);
  }, [jobs]);

  const missingSkills = useMemo(() => {
    const allMissing = recommendations.flatMap(
      (rec) => rec.missing_skills || [],
    );
    return topSkillCounts(allMissing, 10);
  }, [recommendations]);

  const resumeUpgradeSuggestions = useMemo(() => {
    const suggestions =
      latestResume?.parsed_json?.resume_upgrade_suggestions || [];
    if (!Array.isArray(suggestions)) return [];
    return suggestions
      .map((item) => item?.trim())
      .filter((item): item is string => Boolean(item));
  }, [latestResume]);

  if (isLoading || loading) {
    return (
      <div className="dashboard-shell">
        <div className="container dashboard-loading-wrap">
          <div className="dashboard-loading-title shimmer" />
          <div className="dashboard-loading-grid">
            <div className="dashboard-loading-card shimmer" />
            <div className="dashboard-loading-card shimmer" />
          </div>
          <div className="dashboard-loading-wide shimmer" />
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="dashboard-shell">
        <div className="dashboard-card">
          <h2>Login required</h2>
          <p>
            Please login and analyze your resume to view dashboard insights.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-shell">
      <div className="container">
        <section className="dashboard-hero">
          <span className="badge-pill">Dashboard</span>
          <h1>Hi {firstName}, here are your career insights</h1>
          <p>
            Data is based on your parsed resume profile and currently active job
            requirements.
          </p>
          <div className="dashboard-actions">
            <Link to="/jobs" className="btn-pill btn-teal">
              Explore matching jobs
            </Link>
          </div>
        </section>

        {error && <div className="dashboard-error">{error}</div>}

        {latestResume && latestResume.parsed_json?.skills && (
          <section className="dashboard-your-skills">
            <article className="dashboard-card">
              <h3>Your Skills (from resume)</h3>
              <div className="your-skills-container">
                <div className="skill-profile">
                  <div className="profile-item">
                    <label>Current Role:</label>
                    <span>
                      {latestResume.parsed_json.current_role || "Not specified"}
                    </span>
                  </div>
                  <div className="profile-item">
                    <label>Experience:</label>
                    <span>
                      {latestResume.parsed_json.experience_years} years
                    </span>
                  </div>
                  <div className="profile-item">
                    <label>Education:</label>
                    <span>
                      {latestResume.parsed_json.education_level ||
                        "Not specified"}
                    </span>
                  </div>
                </div>
                <ul className="skill-list your-skills">
                  {latestResume.parsed_json.skills.map((skill) => (
                    <li key={skill}>
                      <span>{skill}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </article>
          </section>
        )}

        <section className="dashboard-grid">
          <article className="dashboard-card">
            <h3>Trending Skills Companies Require</h3>
            {trendingSkills.length === 0 ? (
              <p className="muted">No active job skill data available yet.</p>
            ) : (
              <ul className="skill-list">
                {trendingSkills.map((item) => (
                  <li key={item.skill}>
                    <span>{item.skill}</span>
                    <strong>{item.count}</strong>
                  </li>
                ))}
              </ul>
            )}
          </article>

          <article className="dashboard-card">
            <h3>Resume Upgrade Suggestions</h3>
            {resumeUpgradeSuggestions.length > 0 ? (
              <ul className="skill-list upgrades">
                {resumeUpgradeSuggestions.map((suggestion, index) => (
                  <li key={`${suggestion}-${index}`}>
                    <span>{suggestion}</span>
                  </li>
                ))}
              </ul>
            ) : missingSkills.length === 0 ? (
              <p className="muted">
                Great! No major skill gaps found, or upload a resume to get
                personalized analysis.
              </p>
            ) : (
              <ul className="skill-list missing">
                {missingSkills.map((item) => (
                  <li key={item.skill}>
                    <span>
                      Add evidence for {item.skill} in projects and experience
                      bullets
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </article>
        </section>

        <section className="dashboard-recs">
          <h3>Your Top Recommendations</h3>
          {recommendations.length === 0 ? (
            <p className="muted">
              No recommendations yet. Analyze your resume and ensure active jobs
              are available.
            </p>
          ) : (
            <div className="rec-grid">
              {recommendations.slice(0, 6).map((rec) => (
                <Link
                  key={`${rec.resume_id}-${rec.job_id}`}
                  className="rec-card"
                  to={`/jobs/${rec.job_id}`}
                >
                  <div className="rec-top">
                    <h4>{rec.title}</h4>
                    <span>{Math.round(rec.score)}% match</span>
                  </div>
                  <p>
                    {rec.company_name || "Confidential"} •{" "}
                    {rec.location || "Remote"}
                  </p>
                  <div className="rec-tags">
                    {(rec.matched_skills || []).slice(0, 4).map((skill) => (
                      <em key={skill}>{skill}</em>
                    ))}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
