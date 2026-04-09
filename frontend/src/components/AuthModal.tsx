import React, { useState } from "react";
import client from "../api/client";
import { useAuth } from "../context/AuthContext";
import "./AuthModal.css";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: "login" | "register";
  switchTo: (type: "login" | "register") => void;
}

const formatApiError = (payload: any): string => {
  const detail = payload?.response?.data?.detail;

  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item: any) => {
        if (typeof item === "string") return item;

        const location = Array.isArray(item?.loc)
          ? item.loc.filter((part: string) => part !== "body").join(".")
          : "";
        const message = typeof item?.msg === "string" ? item.msg : "";

        if (location && message) return `${location}: ${message}`;
        return message || "";
      })
      .filter(Boolean);

    if (messages.length) {
      return messages.join(" | ");
    }
  }

  if (typeof detail === "object" && detail !== null) {
    return "Request validation failed. Please check your input values.";
  }

  return "Authentication failed. Please check credentials.";
};

export default function AuthModal({
  isOpen,
  onClose,
  type,
  switchTo,
}: AuthModalProps) {
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    full_name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (type === "register") {
        await client.post("/auth/register", {
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
        });
      }

      const params = new URLSearchParams();
      params.append("username", formData.email);
      params.append("password", formData.password);

      const response = await client.post("/auth/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      login(response.data.access_token);
      onClose();
    } catch (err: any) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content panel" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            {type === "login" ? "Sign in to SkillSync" : "Join SkillSync"}
          </h2>
          <button className="close-btn" onClick={onClose}>
            &times;
          </button>
        </div>

        <div className="modal-body">
          <form onSubmit={handleSubmit} className="auth-form">
            {type === "register" && (
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  placeholder="Enter your name"
                  required
                  value={formData.full_name}
                  onChange={(e) =>
                    setFormData({ ...formData, full_name: e.target.value })
                  }
                />
              </div>
            )}
            <div className="form-group">
              <label>Email address</label>
              <input
                type="email"
                placeholder="Enter email"
                required
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
              />
            </div>
            <div className="form-group">
              <div className="label-row">
                <label>Password</label>
                {type === "login" && (
                  <a href="#" className="forgot-pass">
                    Forgot password?
                  </a>
                )}
              </div>
              <input
                type="password"
                placeholder="Enter password"
                required
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
              />
            </div>

            {error && <div className="error-banner">{error}</div>}

            <button
              type="submit"
              className="btn btn-primary submit-btn"
              disabled={loading}
            >
              {loading
                ? "Sign in..."
                : type === "login"
                  ? "Sign in"
                  : "Create account"}
            </button>
          </form>

          <div className="auth-footer">
            {type === "login"
              ? "New to SkillSync? "
              : "Already have an account? "}
            <button
              className="switch-btn"
              onClick={() => switchTo(type === "login" ? "register" : "login")}
            >
              {type === "login" ? "Create an account" : "Sign in"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
