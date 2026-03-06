import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';
import shieldLogo from '../assets/shield-logo.jpg';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Don't show navbar if not logged in
  if (!user) return null;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <img src={shieldLogo} alt="Logo" className="navbar-logo" />
          <h2>Exam Proctoring</h2>
        </div>
        
        <div className="navbar-menu">
          <div className="navbar-user">
            <span className="user-name">👤 {user.name}</span>
            <span className={`user-role ${user.role}`}>
              {user.role === 'examiner' ? '👨‍🏫 Examiner' : '👨‍🎓 Student'}
            </span>
          </div>
          
          <div className="navbar-links">
            <button onClick={() => navigate('/dashboard')} className="nav-link">
              🏠 Dashboard
            </button>
            
            {user.role === 'student' && (
              <>
                <button onClick={() => navigate('/exam-list')} className="nav-link">
                  📝 Exams
                </button>
                <button onClick={() => navigate('/camera-test')} className="nav-link">
                  📹 Camera Test
                </button>
              </>
            )}
            
            {user.role === 'examiner' && (
              <>
                <button onClick={() => navigate('/examiner-dashboard')} className="nav-link">
                  📊 My Exams
                </button>
                <button onClick={() => navigate('/create-exam')} className="nav-link">
                  ➕ Create Exam
                </button>
              </>
            )}
            
            <button onClick={handleLogout} className="nav-link logout">
              🚪 Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;