import './Metrics.css';

export default function Metrics() {
  return (
    <section className="metrics-section section-padding">
      <div className="container">
         <div className="metrics-grid">
            <div className="metric-primary bg-mint">
               <h2 className="metric-title">Level up your <br/> job search.</h2>
               <p>We've analyzed over 500,000 resumes to understand exactly what traits lead to hiring manager interviews.</p>
               <button className="btn-pill btn-teal" style={{marginTop: '2rem'}}>Read the Report</button>
            </div>
            
            <div className="metric-card bg-peach">
               <div className="icon-wrapper">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                     <path d="M12 2L2 7l10 5 10-5-10-5z" />
                     <path d="M2 17l10 5 10-5" />
                     <path d="M2 12l10 5 10-5" />
                  </svg>
               </div>
               <h3>Deep Data Models</h3>
               <p>Our AI doesn't just look for words; it understands the semantic meaning behind your career trajectory.</p>
            </div>

            <div className="metric-card bg-cream-darker">
               <div className="icon-wrapper">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                     <circle cx="12" cy="12" r="10"/>
                     <path d="M12 6v6l4 2"/>
                  </svg>
               </div>
               <h3>Save Hours of Tailoring</h3>
               <p>Stop rewriting bullet points. Instantly see which phrases maximize your match probability for each specific job.</p>
            </div>
         </div>
      </div>
    </section>
  );
}
