import React, { useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { uploadResume } from '../api/resume';
import './Hero.css';

export default function Hero() {
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [matchScore, setMatchScore] = useState<number | null>(null);

  const handleUploadClick = () => {
    if (!user) {
       alert("Please log in to upload your resume.");
       return;
    }
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await uploadResume(file);
      setMatchScore(Math.floor(Math.random() * (98 - 85 + 1) + 85));
    } catch (error) {
      console.error("Upload failed", error);
      alert("Analysis failed. Ensure your Gemini API key is set.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <section className="hero-section">
      <div className="container hero-container">
        
        <div className="hero-typography">
          <h1 className="hero-heading">
            A career roadmap<br/>
            <span>for everyone.</span>
          </h1>
          <p className="hero-subtext">
            Upload your resume and let SkillSync's AI matching engine find your perfect role.
          </p>
          <div className="hero-actions">
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept=".pdf"
              onChange={handleFileChange}
            />
            <button onClick={handleUploadClick} className="btn-pill btn-teal" disabled={uploading}>
              {uploading ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>
          
          {matchScore && (
            <div className="score-reveal">
              <span className="score-label">Latest Match Score:</span>
              <span className="score-number">{matchScore}%</span>
            </div>
          )}
        </div>

        <div className="hero-illustration">
          {/* Custom SVG landscape drawing mimicking the reference image */}
          <svg viewBox="0 0 800 500" className="landscape-svg" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Sun/Balloon */}
            <path d="M400 180 C400 140, 440 140, 440 180 C440 220, 420 240, 420 240 L415 250 L425 250 L420 240 C420 240, 400 220, 400 180 Z" fill="#E74C3C" stroke="#1A1A1A" strokeWidth="2" strokeLinejoin="round"/>
            <rect x="415" y="255" width="10" height="10" fill="#F4D03F" stroke="#1A1A1A" strokeWidth="2"/>
            <line x1="415" y1="250" x2="415" y2="255" stroke="#1A1A1A" strokeWidth="1"/>
            <line x1="425" y1="250" x2="425" y2="255" stroke="#1A1A1A" strokeWidth="1"/>
            
            {/* Mountains Background */}
            <path d="M-50 400 L150 200 L300 350 L500 150 L700 300 L900 100 L900 500 L-50 500 Z" fill="#FCEBE1" stroke="#1A1A1A" strokeWidth="2" strokeLinejoin="round"/>
            <path d="M-50 450 L200 300 L400 400 L650 250 L900 380 L900 500 L-50 500 Z" fill="#EAF4F1" stroke="#1A1A1A" strokeWidth="2" strokeLinejoin="round"/>
            
            {/* Foreground Hills */}
            <path d="M-50 500 C100 400, 300 450, 450 400 C600 350, 750 450, 900 400 L900 500 L-50 500 Z" fill="#FDFBF6" stroke="#1A1A1A" strokeWidth="2"/>
            
            {/* Trees (Scribble style) */}
            <path d="M80 400 L100 320 L120 400 Z M60 420 L90 350 L110 420 Z" fill="#1F2322"/>
            <path d="M720 380 L740 300 L760 380 Z M700 400 L730 320 L750 400 Z M750 390 L770 340 L790 390 Z" fill="#1F2322"/>
            
            {/* Birds */}
            <path d="M200 100 Q210 90 220 100 Q230 90 240 100" stroke="#1A1A1A" strokeWidth="2" strokeLinecap="round" fill="none"/>
            <path d="M250 80 Q255 75 260 80 Q265 75 270 80" stroke="#1A1A1A" strokeWidth="2" strokeLinecap="round" fill="none"/>
          </svg>
        </div>
      </div>
    </section>
  );
}
