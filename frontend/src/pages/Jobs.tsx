import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Briefcase, Clock, DollarSign, MapPin, Search } from "lucide-react";
import { getJobs, searchJobs, type JobResponse } from "../api/jobs";
import {
  getMyRecommendations,
  type JobRecommendationResponse,
} from "../api/recommendations";
import { useAuth } from "../context/AuthContext";
import { createCompanyAvatarDataUri } from "../utils/companyImage";
import "./Jobs.css";

const formatSalary = (min: number, max: number) => {
  if (!min && !max) return "Salary unpublished";
  if (min && !max) return `$${min.toLocaleString()}+`;
  if (!min && max) return `Up to $${max.toLocaleString()}`;
  return `$${min.toLocaleString()} - $${max.toLocaleString()}`;
};

const timeAgo = (dateStr: string) => {
  const diff = Date.now() - new Date(dateStr).getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  return days === 0 ? "Today" : `${days}d ago`;
};

const getJobExcerpt = (description: string) => {
  const cleanText = description.replace(/\s+/g, " ").trim();
  return cleanText.length > 160 ? `${cleanText.slice(0, 160)}...` : cleanText;
};

const getCompanyImage = (companyName?: string) =>
  createCompanyAvatarDataUri(companyName || "SkillSync");

const Jobs = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [recommendations, setRecommendations] = useState<
    JobRecommendationResponse[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [recommendationError, setRecommendationError] = useState("");
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    if (!user) {
      setRecommendations([]);
      return;
    }
    fetchRecommendations();
  }, [user]);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const data = await getJobs();
      setJobs(data);
    } catch (err: any) {
      setError("Failed to load jobs. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      setRecommendationError("");
      const data = await getMyRecommendations(6);
      setRecommendations(data);
    } catch (err: any) {
      const status = err?.response?.status;
      if (status === 404) {
        setRecommendationError("Upload your resume to get recommendations.");
      } else if (status === 401 || status === 403) {
        setRecommendationError("Login to view personalized recommendations.");
      } else {
        setRecommendationError("Could not load recommendations right now.");
      }
    }
  };

  const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);
    if (!val.trim()) {
      fetchJobs();
      return;
    }
    try {
      const data = await searchJobs(val);
      setJobs(data);
    } catch {
      // ignore
    }
  };

  return (
    <div className="jobs-container">
      <div className="jobs-hero">
        <span className="badge-pill jobs-badge">Open roles</span>
        <h1 className="jobs-title">Explore jobs</h1>
        <p className="jobs-subtitle">
          Discover roles that match your strengths with a clean, focused
          browsing experience.
        </p>
        <p className="jobs-count">
          {jobs.length || 0} roles currently available
        </p>
      </div>

      <div className="jobs-filters">
        <div className="jobs-search-shell">
          <Search size={18} />
          <input
            type="text"
            value={query}
            onChange={handleSearch}
            placeholder="Search by title, skill, or keyword..."
            className="jobs-search-input"
          />
        </div>
      </div>

      {user && (
        <section className="recommended-section">
          <div className="recommended-head">
            <h2>Recommended for you</h2>
            <p>Based on your latest parsed resume skills and profile.</p>
          </div>

          {recommendationError ? (
            <div className="jobs-error">{recommendationError}</div>
          ) : recommendations.length === 0 ? (
            <div className="jobs-loading">No recommendations yet.</div>
          ) : (
            <div className="recommendation-grid">
              {recommendations.map((rec) => (
                <div
                  key={`${rec.resume_id}-${rec.job_id}`}
                  className="recommendation-card"
                  role="button"
                  tabIndex={0}
                  onClick={() => navigate(`/jobs/${rec.job_id}`)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      navigate(`/jobs/${rec.job_id}`);
                    }
                  }}
                >
                  <div className="recommendation-topline">
                    <strong>{rec.title}</strong>
                    <span className="match-badge">
                      {Math.round(rec.score)}% match
                    </span>
                  </div>
                  <div className="recommendation-company">
                    {rec.company_name || "Confidential"} •{" "}
                    {rec.location || "Remote"}
                  </div>
                  <div className="recommendation-reasons">
                    {rec.match_reasons.slice(0, 2).map((reason) => (
                      <p key={reason}>{reason}</p>
                    ))}
                  </div>
                  {rec.matched_skills.length > 0 && (
                    <div className="recommendation-skills">
                      {rec.matched_skills.slice(0, 4).map((skill) => (
                        <span key={skill}>{skill}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      {loading ? (
        <div className="jobs-loading">Loading opportunities...</div>
      ) : error ? (
        <div className="jobs-error">{error}</div>
      ) : jobs.length === 0 ? (
        <div className="jobs-error">No jobs found matching your search.</div>
      ) : (
        <div className="jobs-grid">
          {jobs.map((job) => (
            <div
              key={job.job_id}
              className="job-card"
              role="button"
              tabIndex={0}
              onClick={() => navigate(`/jobs/${job.job_id}`)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  navigate(`/jobs/${job.job_id}`);
                }
              }}
            >
              <div className="job-card-visual">
                <img
                  className="job-company-image"
                  src={getCompanyImage(job.company?.name)}
                  alt={`${job.company?.name || "Confidential"} company mark`}
                />
                <div>
                  <div className="job-company-chip">
                    {job.company?.name || "Confidential"}
                  </div>
                  <p className="job-company-note">Company profile</p>
                </div>
              </div>

              <div className="job-card-header">
                <div>
                  <h3 className="job-title">{job.title}</h3>
                  <p className="job-description">
                    {getJobExcerpt(job.description)}
                  </p>
                </div>
              </div>

              <div className="job-meta-list">
                <div className="job-meta-item">
                  <MapPin size={14} />
                  {job.location || "Remote"}
                </div>
                <div className="job-meta-item">
                  <Briefcase size={14} />
                  {job.job_type.replace("-", " ")}
                </div>
                <div className="job-meta-item">
                  <Clock size={14} />
                  {job.experience_min}-{job.experience_max} yrs
                </div>
              </div>

              <div className="job-footer">
                <div>
                  <div className="job-salary">
                    <DollarSign
                      size={14}
                      style={{
                        display: "inline",
                        verticalAlign: "text-bottom",
                      }}
                    />
                    {formatSalary(job.salary_min, job.salary_max)}
                  </div>
                  <div className="job-date">
                    Posted {timeAgo(job.posted_at)}
                  </div>
                </div>
                <span className="job-open-link">View role</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Jobs;
