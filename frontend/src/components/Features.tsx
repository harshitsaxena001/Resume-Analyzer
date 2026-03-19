import React from 'react';
import './Features.css';

export default function Features() {
  return (
    <section className="features-section section-padding" id="how-it-works">
      <div className="container">
        <div className="features-header">
          <span className="badge-pill">The Process</span>
          <h2 className="section-title">An unmatched advantage for<br/> landing your dream role.</h2>
          <p className="section-subtitle">Skip the guesswork. Let AI uncover what recruiters are actually looking for.</p>
        </div>

        <div className="roadmap-wrapper">
           <svg className="roadmap-path" viewBox="0 0 100 800" preserveAspectRatio="none">
             <path d="M50 0 C50 200, 10 300, 50 400 C90 500, 50 700, 50 800" fill="none" stroke="rgba(0,0,0,0.15)" strokeWidth="2" strokeDasharray="6 6" />
           </svg>

           {/* Step 1 */}
           <div className="roadmap-step">
              <div className="step-content">
                 <h3>1. Resume Parsing</h3>
                 <p>Upload your PDF. We meticulously pull out your skills, experiences, and educational background without losing a single detail.</p>
                 <button className="btn-pill btn-outline">Upload Now</button>
              </div>
              <div className="step-visual">
                 <div className="sketch-card bg-mint">
                    <svg viewBox="0 0 100 100" className="sketch-icon">
                       <rect x="25" y="15" width="50" height="70" rx="4" fill="none" stroke="#1A1C1B" strokeWidth="2"/>
                       <line x1="35" y1="35" x2="65" y2="35" stroke="#1A1C1B" strokeWidth="2"/>
                       <line x1="35" y1="45" x2="55" y2="45" stroke="#1A1C1B" strokeWidth="2"/>
                       <circle cx="50" cy="65" r="8" fill="none" stroke="#48C6B4" strokeWidth="2"/>
                       <path d="M55 70 L65 80" stroke="#48C6B4" strokeWidth="2"/>
                    </svg>
                 </div>
              </div>
           </div>

           {/* Step 2 */}
           <div className="roadmap-step reverse">
              <div className="step-content">
                 <h3>2. AI Gap Analysis</h3>
                 <p>Our Gemini 1.5 Pro engine analyzes your profile in real-time, pointing out exact missing keywords and matching you to open roles.</p>
                 <button className="btn-pill btn-outline">See Example</button>
              </div>
              <div className="step-visual">
                 <div className="sketch-card bg-peach">
                    <svg viewBox="0 0 100 100" className="sketch-icon">
                       <path d="M20 75 L35 50 L55 60 L80 25" fill="none" stroke="#1A1C1B" strokeWidth="2" strokeLinejoin="round"/>
                       <circle cx="80" cy="25" r="4" fill="#E74C3C"/>
                       <line x1="20" y1="20" x2="20" y2="80" stroke="#1A1C1B" strokeWidth="2"/>
                       <line x1="15" y1="80" x2="85" y2="80" stroke="#1A1C1B" strokeWidth="2"/>
                    </svg>
                 </div>
              </div>
           </div>

           {/* Step 3 */}
           <div className="roadmap-step">
              <div className="step-content">
                 <h3>3. One-Click Applications</h3>
                 <p>Find matches you love and apply directly. SkillSync formats and sends your resume securely over our API infrastructure.</p>
                 <button className="btn-pill btn-outline">View Jobs</button>
              </div>
              <div className="step-visual">
                 <div className="sketch-card bg-cream-darker">
                    <svg viewBox="0 0 100 100" className="sketch-icon">
                       <path d="M15 45 L50 20 L85 45 L85 80 L15 80 Z" fill="none" stroke="#1A1C1B" strokeWidth="2"/>
                       <path d="M35 80 L35 55 L65 55 L65 80" fill="none" stroke="#1A1C1B" strokeWidth="2"/>
                       <circle cx="70" cy="35" r="6" fill="#F4D03F" stroke="#1A1C1B" strokeWidth="2"/>
                    </svg>
                 </div>
              </div>
           </div>

        </div>
      </div>
    </section>
  );
}
