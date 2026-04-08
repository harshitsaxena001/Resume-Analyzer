import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import "./Navbar.css";

interface NavbarProps {
  onOpenAuth: (type: "login" | "register") => void;
}

export default function Navbar({ onOpenAuth }: NavbarProps) {
  const { user, logout } = useAuth();

  return (
    <nav className="site-navbar">
      <div className="container nav-wrapper">
        <div className="nav-left">
          <a href="/" className="nav-logo">
            {/* Elegant compass/astrolabe placeholder SVG */}
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
            </svg>
            <span className="logo-text">SkillSync</span>
          </a>
        </div>

        <div className="nav-center">
          {user && <Link to="/dashboard">Dashboard</Link>}
          <Link to="/jobs">Explore Jobs</Link>
          <a href="/#how-it-works">How it works</a>
          <a href="/#features">Features</a>
        </div>

        <div className="nav-right">
          {user ? (
            <div className="user-controls">
              <span className="user-name">
                Hello, {user.full_name.split(" ")[0]}
              </span>
              <button onClick={logout} className="nav-text-btn">
                Log out
              </button>
            </div>
          ) : (
            <div className="auth-controls">
              <button
                onClick={() => onOpenAuth("login")}
                className="nav-text-btn"
              >
                Log in
              </button>
              <button
                onClick={() => onOpenAuth("register")}
                className="btn-pill btn-teal"
              >
                Start analyzing
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
