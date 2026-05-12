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
          total: list.length,
          completed: list.filter(e => e.is_published).length,
          pending: list.filter(e => !e.is_published).length,
          avgScore: '95%'
        });
      }
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  if (loading) return <div className="db-loading">Loading…</div>;
  if (!user) return null;

  const firstName = user?.name?.split(' ')[0] || 'User';

  return (
    <div className="db-layout">

      {/* ══ SIDEBAR ══ */}
      <aside className="db-sidebar">
        <div className="db-sidebar-brand">
          <img src={require('../assets/shield-logo.jpg')} alt="logo" className="db-brand-logo" />
          <div>
            <div className="db-brand-title">ONLINE</div>
            <div className="db-brand-title">PROCTORING</div>
          </div>
        </div>

        <nav className="db-nav">
          <Link to="/dashboard" className="db-nav-item active">
            <span className="db-nav-icon">🏠</span> Dashboard
          </Link>
          <Link to="/exam-list" className="db-nav-item">
            <span className="db-nav-icon">📝</span> Exams
          </Link>
          {user.role === 'student' && (
            <Link to="/exam-list" className="db-nav-item">
              <span className="db-nav-icon">📚</span> My Exams
            </Link>
          )}
          <Link to="/camera-test" className="db-nav-item">
            <span className="db-nav-icon">📷</span> Camera Test
          </Link>
          {user.role === 'student' && (
            <Link to="/results" className="db-nav-item">
              <span className="db-nav-icon">📊</span> Reports
            </Link>
          )}
          {user.role === 'examiner' && (
            <Link to="/examiner-dashboard" className="db-nav-item">
              <span className="db-nav-icon">🎓</span> Examiner Panel
            </Link>
          )}
          <Link to="#" className="db-nav-item">
            <span className="db-nav-icon">💬</span> Messages
          </Link>
          <Link to="#" className="db-nav-item">
            <span className="db-nav-icon">⚙️</span> Settings
          </Link>
          <Link to="#" className="db-nav-item">
            <span className="db-nav-icon">❓</span> Help &amp; Support
          </Link>
        </nav>

        <div className="db-sidebar-help">
          <div className="db-help-box">
            <div className="db-help-icon">🤖</div>
            <div className="db-help-text">Need Help?<br /><span>We're here to assist you.</span></div>
            <button className="db-help-btn" onClick={() => navigate('/camera-test')}>Contact Support</button>
          </div>
        </div>
      </aside>

      {/* ══ MAIN ══ */}
      <main className="db-main">

        {/* Top bar */}
        <header className="db-topbar">
          <button className="db-menu-btn">☰</button>
          <div className="db-topbar-right">
            <button className="db-icon-btn">🔔 <span className="db-badge">3</span></button>
            <div className="db-user-chip">
              <div className="db-avatar">{firstName.charAt(0).toUpperCase()}</div>
              <div className="db-user-info">
                <span className="db-user-name">{user.name}</span>
                <span className="db-user-role">{user.role}</span>
              </div>
              <button className="db-logout-btn" onClick={() => { logout(); navigate('/login'); }}>↩</button>
            </div>
          </div>
        </header>

        <div className="db-content">

          {/* Welcome banner */}
          <div className="db-welcome-banner">
            <div className="db-welcome-text">
              <h1>Welcome back, {firstName}! 👋</h1>
              <p>Stay focused and do your best.</p>
            </div>
            <div className="db-welcome-illustration">📊</div>
          </div>

          {/* Stats row */}
          <div className="db-stats-row">
            <div className="db-stat-card">
              <div className="db-stat-icon blue">📅</div>
              <div>
                <div className="db-stat-num">{stats.total}</div>
                <div className="db-stat-label">Total Exams</div>
                <div className="db-stat-sub">All assigned exams</div>
              </div>
            </div>
            <div className="db-stat-card">
              <div className="db-stat-icon green">✅</div>
              <div>
                <div className="db-stat-num">{stats.completed}</div>
                <div className="db-stat-label">Completed</div>
                <div className="db-stat-sub">Exams finished</div>
              </div>
            </div>
            <div className="db-stat-card">
              <div className="db-stat-icon orange">⏳</div>
              <div>
                <div className="db-stat-num">{stats.pending}</div>
                <div className="db-stat-label">Pending</div>
                <div className="db-stat-sub">Exams remaining</div>
              </div>
            </div>
            <div className="db-stat-card">
              <div className="db-stat-icon purple">🏆</div>
              <div>
                <div className="db-stat-num">{stats.avgScore}</div>
                <div className="db-stat-label">Average Score</div>
                <div className="db-stat-sub">All time performance</div>
              </div>
            </div>
          </div>

          {/* Middle row */}
          <div className="db-mid-row">

            {/* Upcoming Exam */}
            <div className="db-card db-upcoming">
              <div className="db-card-header">
                <h3>Upcoming Exam</h3>
                <Link to="/exam-list" className="db-view-all">View All</Link>
              </div>
              {exams.length > 0 ? (
                exams.slice(0, 1).map(exam => (
                  <div key={exam.id} className="db-exam-row">
                    <div className="db-exam-thumb">📖</div>
                    <div className="db-exam-info">
                      <div className="db-exam-title">{exam.title}</div>
                      <div className="db-exam-subject">{exam.subject || 'General'}</div>
                      <div className="db-exam-meta">
                        <span>⏱ {exam.duration} min</span>
                        <span>⭐ {exam.total_marks} marks</span>
                      </div>
                    </div>
                    <div className="db-exam-actions">
                      <span className="db-badge-upcoming">Upcoming</span>
                      <button className="db-btn-start" onClick={() => navigate(`/exam/${exam.id}/acceptance`)}>
                        Start Exam
                      </button>
                      <button className="db-btn-details" onClick={() => navigate(`/exam/${exam.id}/acceptance`)}>
                        Details
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="db-empty">No upcoming exams.</div>
              )}
            </div>

            {/* Recent Activity */}
            <div className="db-card db-activity">
              <div className="db-card-header">
                <h3>Recent Activity</h3>
                <Link to="/results" className="db-view-all">View All</Link>
              </div>
              <div className="db-activity-list">
                {exams.slice(0, 3).map((exam, i) => (
                  <div key={exam.id} className="db-activity-item">
                    <div className={`db-activity-dot ${i === 2 ? 'orange' : 'green'}`}></div>
                    <div className="db-activity-info">
                      <div className="db-activity-name">{exam.title}</div>
                      <div className={`db-activity-status ${i === 2 ? 'pending' : 'completed'}`}>
                        {i === 2 ? 'Pending' : 'Completed'}
                      </div>
                    </div>
                    <div className="db-activity-time">{i + 1}d ago</div>
                  </div>
                ))}
                {exams.length === 0 && <div className="db-empty">No recent activity.</div>}
              </div>
            </div>
          </div>

          {/* Bottom row */}
          <div className="db-bottom-row">

            {/* Progress */}
            <div className="db-card db-progress-card">
              <h3>Your Progress</h3>
              <div className="db-progress-circle-wrap">
                <div className="db-progress-circle">
                  <svg viewBox="0 0 100 100" width="120" height="120">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#e2e8f0" strokeWidth="10"/>
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#3b82f6" strokeWidth="10"
                      strokeDasharray="251" strokeDashoffset="90" strokeLinecap="round"
                      transform="rotate(-90 50 50)"/>
                  </svg>
                  <div className="db-progress-label">
                    <div className="db-progress-pct">66%</div>
                    <div className="db-progress-sub">Completed</div>
                  </div>
                </div>
                <div className="db-progress-legend">
                  <div className="db-legend-item"><span className="dot green"></span> Completed <strong>{stats.completed}</strong></div>
                  <div className="db-legend-item"><span className="dot orange"></span> Pending <strong>{stats.pending}</strong></div>
                  <div className="db-legend-item"><span className="dot gray"></span> Not Started <strong>{Math.max(0, stats.total - stats.completed - stats.pending)}</strong></div>
                </div>
              </div>
            </div>

            {/* System Status */}
            <div className="db-card db-system-status">
              <div className="db-status-header">
                <span className="db-status-dot green"></span>
                <div>
                  <div className="db-status-title">System Status</div>
                  <div className="db-status-sub">All systems are running smoothly</div>
                </div>
              </div>
              <div className="db-status-grid">
                <div className="db-status-item">
                  <div className="db-status-icon">🤖</div>
                  <div className="db-status-name">AI Proctoring</div>
                  <div className="db-status-badge green">Active</div>
                </div>
                <div className="db-status-item">
                  <div className="db-status-icon">👁️</div>
                  <div className="db-status-name">Live Monitoring</div>
                  <div className="db-status-badge green">Active</div>
                </div>
                <div className="db-status-item">
                  <div className="db-status-icon">🔒</div>
                  <div className="db-status-name">Secure Browser</div>
                  <div className="db-status-badge blue">Enabled</div>
                </div>
                <div className="db-status-item">
                  <div className="db-status-icon">📷</div>
                  <div className="db-status-name">Camera</div>
                  <div className="db-status-badge green">Connected</div>
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <footer className="db-footer">
          © 2024 TI Online Examination System Pro &nbsp;|&nbsp; A Product of <a href="#">Trakus Infotek</a>
        </footer>
      </main>
    </div>
  );
}
