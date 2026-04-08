import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import AuthModal from "./components/AuthModal";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import Jobs from "./pages/Jobs";
import JobDetails from "./pages/JobDetails";
import Dashboard from "./pages/Dashboard";
import "./index.css";

function App() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [authType, setAuthType] = useState<"login" | "register">("login");

  const openAuth = (type: "login" | "register") => {
    setAuthType(type);
    setIsAuthOpen(true);
  };

  return (
    <AuthProvider>
      <Navbar onOpenAuth={openAuth} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/jobs/:id" element={<JobDetails />} />
      </Routes>

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
