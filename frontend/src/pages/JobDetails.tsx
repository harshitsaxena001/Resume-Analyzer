import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Briefcase,
  Clock,
  DollarSign,
  ExternalLink,
  MapPin,
  Send,
} from "lucide-react";
import { getJobById, type JobResponse } from "../api/jobs";
import { applyToJob } from "../api/applications";
import { useAuth } from "../context/AuthContext";
import { createCompanyAvatarDataUri } from "../utils/companyImage";
import "./JobDetails.css";

const extractApplyLink = (description: string): string | null => {
  if (!description) return null;

  const directMatch = description.match(
    /apply\s*link\s*:\s*(https?:\/\/[^\s<]+)/i,
  );
  if (directMatch?.[1]) return directMatch[1].trim();

  const anyUrl = description.match(/https?:\/\/[^\s<]+/i);
  return anyUrl?.[0]?.trim() || null;
};

const normalizeExternalUrl = (
  url: string | null | undefined,
): string | null => {
  if (!url) return null;
  const clean = url.trim();
  if (!clean) return null;
  if (/^https?:\/\//i.test(clean)) return clean;
  return `https://${clean}`;
};

const JobDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [job, setJob] = useState<JobResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showApplyModal, setShowApplyModal] = useState(false);
  const [coverLetter, setCoverLetter] = useState("");
  const [applying, setApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);
  const [applyError, setApplyError] = useState("");

  const companyName = job?.company?.name || "Confidential";
  const companyAvatar = createCompanyAvatarDataUri(companyName, 200);
  const requiredSkills = (job?.job_skills || []).filter((js) => js.is_required);
  const preferredSkills = (job?.job_skills || []).filter(
    (js) => !js.is_required,
  );
  const directApplyUrl =
    normalizeExternalUrl(job?.company?.website) ||
    normalizeExternalUrl(extractApplyLink(job?.description || ""));

  useEffect(() => {
    if (id) {
      loadJob(parseInt(id, 10));
    }
  }, [id]);

  const loadJob = async (jobId: number) => {
    try {
      setLoading(true);
      const data = await getJobById(jobId);
      setJob(data);
    } catch (err) {
      setError("Failed to load job details. It may have been removed.");
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!job) return;

    try {
      setApplying(true);
      setApplyError("");
      await applyToJob({
        job_id: job.job_id,
        cover_letter: coverLetter.trim() || undefined,
      });
      setApplySuccess(true);
      setTimeout(() => setShowApplyModal(false), 2000);
    } catch (err: any) {
      setApplyError(
        err.response?.data?.detail ||
          "Failed to submit application. Please try again.",
      );
    } finally {
      setApplying(false);
    }
  };

  if (loading)
    return (
      <div className="job-details-container">
        <div style={{ textAlign: "center" }}>Loading...</div>
      </div>
    );
  if (error || !job)
    return (
      <div className="job-details-container">
        <div className="apply-error">{error}</div>
      </div>
    );

  return (
    <div className="job-details-container">
      <button
        className="btn-pill btn-outline btn-back"
        onClick={() => navigate("/jobs")}
      >
        <ArrowLeft size={16} /> Back to jobs
      </button>

      <section className="job-hero-card">
        <div className="job-hero-topline">
          <span className="badge-pill">Job details</span>
          <span className="job-status">Active opening</span>
        </div>

        <div className="job-hero-company">
          <img
            className="jd-company-avatar"
            src={companyAvatar}
            alt={`${companyName} logo`}
          />
          <div>
            <div className="jd-company">{companyName}</div>
            <p className="jd-company-subtitle">
              Carefully presented role information
            </p>
          </div>
        </div>

        <h1 className="jd-title">{job.title}</h1>

        <p className="jd-summary">
          Clean role overview, location, pay range, and skills laid out for
          quick scanning without visual clutter.
        </p>

        <div className="jd-actions">
          <button
            className="btn-pill btn-teal btn-apply"
            onClick={() => {
              if (!user) {
                alert("Please login first to apply.");
                return;
              }
              setShowApplyModal(true);
            }}
          >
            <Send size={18} /> Apply now
          </button>

          {directApplyUrl && (
            <a
              className="btn-pill btn-outline btn-company-apply"
              href={directApplyUrl}
              target="_blank"
              rel="noreferrer noopener"
            >
              <ExternalLink size={16} /> Apply on company site
            </a>
          )}
        </div>
      </section>

      <div className="jd-meta-card">
        <div className="jd-meta">
          <div className="jd-meta-item">
            <MapPin size={16} /> {job.location || "Remote"}
          </div>
          <div className="jd-meta-item">
            <Briefcase size={16} /> {job.job_type.replace("-", " ")}
          </div>
          <div className="jd-meta-item">
            <Clock size={16} /> {job.experience_min}-{job.experience_max} yrs
          </div>
          <div className="jd-meta-item">
            <DollarSign size={16} />
            {job.salary_min ? `$${job.salary_min.toLocaleString()}` : ""}
            {job.salary_max ? ` - $${job.salary_max.toLocaleString()}` : ""}
          </div>
        </div>
      </div>

      <div className="jd-content-card">
        <h3>About the role</h3>
        <div
          className="jd-content"
          dangerouslySetInnerHTML={{
            __html: job.description.replace(/\n/g, "<br/>"),
          }}
        />
      </div>

      {job.job_skills && job.job_skills.length > 0 && (
        <div className="jd-skills-card">
          <h3>Skills the company is demanding</h3>
          {requiredSkills.length > 0 && (
            <>
              <h4 className="jd-skill-subtitle">Required</h4>
              <div className="jd-skills-list">
                {requiredSkills.map((js) => (
                  <span key={js.id} className="jd-skill-badge required">
                    {js.skill.name}
                  </span>
                ))}
              </div>
            </>
          )}

          {preferredSkills.length > 0 && (
            <>
              <h4 className="jd-skill-subtitle">Preferred</h4>
              <div className="jd-skills-list">
                {preferredSkills.map((js) => (
                  <span key={js.id} className="jd-skill-badge preferred">
                    {js.skill.name}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {showApplyModal && (
        <div className="apply-modal-overlay">
          <div className="apply-modal">
            {applySuccess ? (
              <div className="apply-success">
                <h3>Application submitted</h3>
                <p>The recruiter will review your profile shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleApply}>
                <h2>Apply for {job.title}</h2>
                <p>at {job.company?.name || "Confidential Company"}</p>

                {directApplyUrl && (
                  <div className="apply-direct-link">
                    <strong>Prefer company application portal?</strong>
                    <a
                      href={directApplyUrl}
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      Continue on company site <ExternalLink size={14} />
                    </a>
                  </div>
                )}

                {(requiredSkills.length > 0 || preferredSkills.length > 0) && (
                  <div className="apply-skill-preview">
                    <strong>Company skill expectations</strong>
                    {requiredSkills.length > 0 && (
                      <p>
                        Required:{" "}
                        {requiredSkills.map((s) => s.skill.name).join(", ")}
                      </p>
                    )}
                    {preferredSkills.length > 0 && (
                      <p>
                        Preferred:{" "}
                        {preferredSkills.map((s) => s.skill.name).join(", ")}
                      </p>
                    )}
                  </div>
                )}

                {applyError && <div className="apply-error">{applyError}</div>}

                <div className="form-group">
                  <label>Cover Letter (Optional)</label>
                  <textarea
                    value={coverLetter}
                    onChange={(e) => setCoverLetter(e.target.value)}
                    placeholder="Tell the company why you're a great fit..."
                  />
                </div>

                <div className="apply-actions">
                  <button
                    type="button"
                    className="btn-pill btn-outline"
                    onClick={() => setShowApplyModal(false)}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn-pill btn-teal"
                    disabled={applying}
                  >
                    {applying ? "Submitting..." : "Submit Application"}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobDetails;
