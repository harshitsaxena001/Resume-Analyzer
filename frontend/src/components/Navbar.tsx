import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import "./Navbar.css";

interface NavbarProps {
  onOpenAuth: (type: "login" | "register") => void;
}

export default function Navbar({ onOpenAuth }: NavbarProps) {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleNavItemClick = () => setMenuOpen(false);

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
          <button
            type="button"
            className={`nav-toggle ${menuOpen ? "is-open" : ""}`}
            onClick={() => setMenuOpen((prev) => !prev)}
            aria-label={
              menuOpen ? "Close navigation menu" : "Open navigation menu"
            }
            aria-expanded={menuOpen}
            aria-controls="mobile-main-nav"
          >
            <span />
            <span />
            <span />
          </button>
        </div>

        <div
          id="mobile-main-nav"
          className={`nav-center ${menuOpen ? "is-open" : ""}`}
        >
          {user && (
            <Link to="/dashboard" onClick={handleNavItemClick}>
              Dashboard
            </Link>
          )}
          <Link to="/jobs" onClick={handleNavItemClick}>
            Explore Jobs
          </Link>
          <a href="/#how-it-works" onClick={handleNavItemClick}>
            How it works
          </a>
          <a href="/#features" onClick={handleNavItemClick}>
            Features
          </a>
        </div>

        <div className={`nav-right ${menuOpen ? "is-open" : ""}`}>
          {user ? (
            <div className="user-controls">
              <span className="user-name">
                Hello, {user.full_name.split(" ")[0]}
              </span>
              <button
                onClick={() => {
                  logout();
                  handleNavItemClick();
                }}
                className="nav-text-btn"
              >
                Log out
              </button>
            </div>
          ) : (
            <div className="auth-controls">
              <button
                onClick={() => {
                  onOpenAuth("login");
                  handleNavItemClick();
                }}
                className="nav-text-btn"
              >
                Log in
              </button>
              <button
                onClick={() => {
                  onOpenAuth("register");
                  handleNavItemClick();
                }}
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
