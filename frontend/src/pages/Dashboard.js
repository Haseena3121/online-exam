/* eslint-disable no-unused-vars, no-console */
import API_BASE from '../config';
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

export default function Dashboard() {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, avgScore: '95%' });
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!user || !token) { navigate('/login'); return; }
    fetchData();
  }, [user, token]);

  const fetchData = async () => {
    try {
      const url = user.role === 'examiner' ? `${API_BASE}/api/exams/my-exams` : `${API_BASE}/api/exams/`;
      const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        const list = data.exams || [];
        setExams(list);
        setStats({
          total: list.length || 1,
          completed: list.filter(e => e.is_published).length,
          pending: list.filter(e => !e.is_published).length || 1,
          avgScore: '95%'
        });
      }
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  if (loading) return (
    <div className="db-loading">
      <div className="loading-spinner"></div>
      <span>Loading...</span>
    </div>
  );
  if (!user) return null;

  const firstName = user?.name?.split(' ')[0] || 'User';

  return (
    <div className="dashboard-page">
      {/* Header */}
      <header className="db-header">
        <div className="db-header-left">
          <div className="db-logo">
            <div className="logo-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L3 7V12C3 17.55 6.84 22.74 12 24C17.16 22.74 21 17.55 21 12V7L12 2Z" fill="url(#hdr-gradient)"/>
                <circle cx="12" cy="12" r="3" fill="#1a1a2e"/>
                <circle cx="12" cy="12" r="1.5" fill="#4f46e5"/>
                <defs>
                  <linearGradient id="hdr-gradient" x1="3" y1="2" x2="21" y2="24">
                    <stop stopColor="#3b82f6"/>
                    <stop offset="1" stopColor="#8b5cf6"/>
                  </linearGradient>
                </defs>
              </svg>
              <div className="logo-cap">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#1e293b">
                  <path d="M12 3L1 9L5 11.18V17.18L12 21L19 17.18V11.18L21 10.09V17H23V9L12 3Z"/>
                </svg>
              </div>
            </div>
            <div className="logo-text">
              <span className="logo-title">Exam Proctoring</span>
              <span className="logo-subtitle">Secure &bull; Smart &bull; Reliable</span>
            </div>
          </div>
          <div className="db-user-tag">
            <span className="user-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </span>
            <span className="user-name">{firstName}</span>
            <span className="user-role-badge">{user.role}</span>
          </div>
        </div>

        <nav className="db-nav">
          <Link to="/dashboard" className="nav-item active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
            </svg>
            Dashboard
          </Link>
          <Link to="/exam-list" className="nav-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            Exams
          </Link>
          <Link to="/camera-test" className="nav-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="3.2"/>
              <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
            </svg>
            Camera Test
          </Link>
        </nav>

        <button className="btn-logout" onClick={() => { logout(); navigate('/login'); }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Logout
        </button>
      </header>

      {/* Main Content */}
      <main className="db-main">
        <div className="db-content-wrapper">
          {/* Left Content */}
          <div className="db-left-content">
            {/* Welcome Section */}
            <section className="welcome-section">
              <div className="welcome-text">
                <h1>
                  <span className="wave">&#128075;</span> Welcome, {firstName}!
                </h1>
                <p>Good to see you again. Ready to excel today?</p>
                <div className="role-tag">
                  <span>Role:</span>
                  <span className="role-value">{user.role.toUpperCase()}</span>
                </div>
              </div>
              <div className="welcome-illustration">
                <img src={require('../assets/dashboard_student.png')} alt="Student" onError={(e) => e.target.style.display='none'} />
              </div>
            </section>

            {/* Stats Cards */}
            <section className="stats-section">
              <div className="stat-card blue">
                <div className="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                  </svg>
                </div>
                <div className="stat-info">
                  <span className="stat-number">{stats.total}</span>
                  <span className="stat-label">Total Exams</span>
                  <span className="stat-sub">All assigned exams</span>
                </div>
              </div>
              <div className="stat-card green">
                <div className="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                </div>
                <div className="stat-info">
                  <span className="stat-number">{stats.completed}</span>
                  <span className="stat-label">Completed</span>
                  <span className="stat-sub">Exams finished</span>
                </div>
              </div>
              <div className="stat-card orange">
                <div className="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M6 2v6h.01L6 8.01 10 12l-4 4 .01.01H6V22h12v-5.99h-.01L18 16l-4-4 4-3.99-.01-.01H18V2H6z"/>
                  </svg>
                </div>
                <div className="stat-info">
                  <span className="stat-number">{stats.pending}</span>
                  <span className="stat-label">Pending</span>
                  <span className="stat-sub">Exams remaining</span>
                </div>
              </div>
            </section>

            {/* Available Exams */}
            <section className="exams-section">
              <div className="section-header">
                <h2>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="#3b82f6">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                  </svg>
                  Available Exams
                </h2>
                <Link to="/exam-list" className="view-all-btn">
                  View All Exams
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="5" y1="12" x2="19" y2="12"/>
                    <polyline points="12 5 19 12 12 19"/>
                  </svg>
                </Link>
              </div>

              <div className="exam-cards">
                {exams.length > 0 ? exams.slice(0, 2).map(exam => (
                  <div key={exam.id} className="exam-card">
                    <div className="exam-thumb">
                      <svg width="40" height="40" viewBox="0 0 24 24" fill="#3b82f6">
                        <path d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99L12 18.72 7 15.99v-3.72L12 15l5-2.73v3.72z"/>
                      </svg>
                    </div>
                    <div className="exam-details">
                      <h3>{exam.title}</h3>
                      <p>{exam.subject || 'General'}</p>
                      <div className="exam-meta">
                        <span className="meta-item">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
                          </svg>
                          {exam.duration} min
                        </span>
                        <span className="meta-item">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                          </svg>
                          {exam.total_marks} marks
                        </span>
                      </div>
                    </div>
                    <div className="exam-actions">
                      <button className="btn-take-exam" onClick={() => navigate(`/exam/${exam.id}/acceptance`)}>
                        Take Exam
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <line x1="5" y1="12" x2="19" y2="12"/>
                          <polyline points="12 5 19 12 12 19"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                )) : (
                  <div className="no-exams">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="#cbd5e1">
                      <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                    </svg>
                    <p>No exams available at the moment.</p>
                  </div>
                )}
              </div>
            </section>
          </div>

          {/* Right Sidebar */}
          <aside className="db-sidebar">
            {/* Security Card */}
            <div className="security-card">
              <div className="security-shield-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" fill="url(#sec-gradient)"/>
                  <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z" fill="white"/>
                  <defs>
                    <linearGradient id="sec-gradient" x1="3" y1="1" x2="21" y2="23">
                      <stop stopColor="#3b82f6"/>
                      <stop offset="1" stopColor="#6366f1"/>
                    </linearGradient>
                  </defs>
                </svg>
                <div className="lock-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
                    <rect x="3" y="11" width="18" height="11" rx="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </div>
              </div>
              <h3>Safe & Secure</h3>
              <p>Your privacy and security are our top priority.</p>
            </div>

            {/* Features List */}
            <div className="features-list">
              <div className="feature-item">
                <div className="feature-icon blue">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/>
                  </svg>
                </div>
                <div>
                  <strong>AI Proctoring</strong>
                  <span>Smart AI monitors the exam</span>
                </div>
              </div>
              <div className="feature-item">
                <div className="feature-icon cyan">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
                  </svg>
                </div>
                <div>
                  <strong>Live Monitoring</strong>
                  <span>Real-time activity monitoring</span>
                </div>
              </div>
              <div className="feature-item">
                <div className="feature-icon purple">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                </div>
                <div>
                  <strong>Fair & Transparent</strong>
                  <span>Ensuring fairness for everyone</span>
                </div>
              </div>
            </div>

            {/* Motivational Quote */}
            <div className="quote-card">
              <div className="quote-icon">&ldquo;</div>
              <p className="quote-text"><em>Focus, Attempt, Achieve</em></p>
              <p className="quote-sub">{"We're here to support your success!"}</p>
              <div className="quote-star">&#9733;</div>
            </div>
          </aside>
        </div>
      </main>

      {/* Footer */}
      <footer className="db-footer">
        &copy; 2024 TI Online Examination System Pro | A Product of <a href="#">Trakus Infotek</a>
      </footer>
    </div>
  );
}
