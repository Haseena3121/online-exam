import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';

function Navbar() {
  const { user, handleLogout } = useAuth();
  const navigate = useNavigate();
  const [showMenu, setShowMenu] = useState(false);

  const handleLogoutClick = () => {
    handleLogout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          📚 Exam Proctoring
        </Link>

        <div className="navbar-menu">
          {user?.role === 'student' && (
            <>
              <Link to="/exams" className="nav-link">📝 Exams</Link>
              <Link to="/results" className="nav-link">📊 Results</Link>
            </>
          )}
          
          {user?.role === 'examiner' && (
            <>
              <Link to="/examiner/dashboard" className="nav-link">👨‍🏫 Dashboard</Link>
            </>
          )}

          <div className="nav-user">
            <span className="user-name">👤 {user?.name}</span>
            <button className="btn btn-logout" onClick={handleLogoutClick}>
              🚪 Logout
            </button>
          </div>
        </div>

        <button className="hamburger" onClick={() => setShowMenu(!showMenu)}>
          ☰
        </button>

        {showMenu && (
          <div className="mobile-menu">
            {user?.role === 'student' && (
              <>
                <Link to="/exams">Exams</Link>
                <Link to="/results">Results</Link>
              </>
            )}
            {user?.role === 'examiner' && (
              <Link to="/examiner/dashboard">Dashboard</Link>
            )}
            <button onClick={handleLogoutClick}>Logout</button>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;