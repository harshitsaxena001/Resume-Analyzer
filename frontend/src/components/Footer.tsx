import "./Footer.css";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container site-footer-shell">
        <h2 className="site-footer-title">
          Ready to optimize your career?
        </h2>
        <p className="site-footer-subtitle">
          Join thousands of professionals who have accelerated their job search
          using SkillSync's AI matching engine.
        </p>

        <div className="site-footer-links">
          <a href="#">
            Features
          </a>
          <a href="#">
            Contact
          </a>
          <a href="#">
            Privacy
          </a>
        </div>

        <div className="site-footer-bottom">
          <span>© 2026 SkillSync Inc. All rights reserved.</span>
          <span>Designed for professionals.</span>
        </div>
      </div>
    </footer>
  );
}
