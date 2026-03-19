import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Metrics from './components/Metrics';
import Footer from './components/Footer';
import AuthModal from './components/AuthModal';
import { AuthProvider } from './context/AuthContext';
import './index.css';

function App() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [authType, setAuthType] = useState<'login' | 'register'>('login');

  const openAuth = (type: 'login' | 'register') => {
    setAuthType(type);
    setIsAuthOpen(true);
  };

  return (
    <AuthProvider>
      <Navbar onOpenAuth={openAuth} />
      <Hero />
      <Features />
      <Metrics />
      <Footer />
      
      <AuthModal 
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        type={authType}
        switchTo={setAuthType}
      />
    </AuthProvider>
  );
}

export default App;
