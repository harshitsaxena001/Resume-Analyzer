export default function Footer() {
  return (
    <footer style={{ 
      backgroundColor: '#1F2322', 
      color: '#FDFBF6', 
      padding: '4rem 0 2rem', 
      fontFamily: 'var(--font-sans)' 
    }}>
      <div className="container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
        <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: '2.5rem', marginBottom: '1.5rem', color: '#F9EBE0' }}>
          Ready to optimize your career?
        </h2>
        <p style={{ color: '#A0A6A4', marginBottom: '3rem', maxWidth: '500px' }}>
          Join thousands of professionals who have accelerated their job search using SkillSync's AI matching engine.
        </p>
        
        <div style={{ display: 'flex', gap: '2rem', marginBottom: '4rem' }}>
           <a href="#" style={{ color: '#fff', fontSize: '0.9rem' }}>Features</a>
           <a href="#" style={{ color: '#fff', fontSize: '0.9rem' }}>Pricing</a>
           <a href="#" style={{ color: '#fff', fontSize: '0.9rem' }}>Contact</a>
           <a href="#" style={{ color: '#fff', fontSize: '0.9rem' }}>Privacy</a>
        </div>
        
        <div style={{ width: '100%', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '2rem', display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#A0A6A4' }}>
           <span>© 2026 SkillSync Inc. All rights reserved.</span>
           <span>Designed for professionals.</span>
        </div>
      </div>
    </footer>
  );
}
