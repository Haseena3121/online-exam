import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

function Dashboard() {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [enrolledExams, setEnrolledExams] = useState([]);
  const [createdExams, setCreatedExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalExams: 0,
    completed: 0,
    pending: 0
  });

  useEffect(() => {
    // Redirect to login if not authenticated
    if (!user || !token) {
      navigate('/login');
      return;
    }
    fetchDashboardData();
  }, [user, token, navigate]);

  const fetchDashboardData = async () => {
    try {
      if (user.role === 'student') {
        // Fetch enrolled exams
        const response = await fetch('http://localhost:5000/api/exams/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setEnrolledExams(data.exams);
          setStats({
            totalExams: data.exams.length,
            completed: 0,
            pending: data.exams.length
          });
        }
      } else if (user.role === 'examiner') {
        // Fetch created exams
        const response = await fetch('http://localhost:5000/api/exams/my-exams', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setCreatedExams(data.exams);
          setStats({
            totalExams: data.exams.length,
            completed: data.exams.filter(e => e.is_published).length,
            pending: data.exams.filter(e => !e.is_published).length
          });
        }
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (!user) {
    return <div className="loading">Redirecting to login...</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>👋 Welcome, {user?.name || 'User'}!</h1>
        <p>Role: <span className="badge">{user?.role?.toUpperCase() || 'UNKNOWN'}</span></p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.totalExams}</h3>
            <p>Total Exams</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{stats.completed}</h3>
            <p>Completed</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <h3>{stats.pending}</h3>
            <p>Pending</p>
          </div>
        </div>
      </div>

      {user.role === 'student' && (
        <div className="dashboard-section">
          <div className="section-header">
            <h2>📝 Available Exams</h2>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/exam-list')}
            >
              View All Exams
            </button>
          </div>

          {enrolledExams.length > 0 ? (
            <div className="exams-grid">
              {enrolledExams.slice(0, 3).map(exam => (
                <div key={exam.id} className="exam-card">
                  <h3>{exam.title}</h3>
                  <p className="exam-desc">{exam.description}</p>
                  <div className="exam-meta">
                    <span>⏱️ {exam.duration} min</span>
                    <span>⭐ {exam.total_marks} marks</span>
                  </div>
                  <button 
                    className="btn btn-primary btn-block"
                    onClick={() => navigate(`/exam/${exam.id}/acceptance`)}
                  >
                    Take Exam
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No exams available yet</p>
            </div>
          )}
        </div>
      )}

      {user.role === 'examiner' && (
        <div className="dashboard-section">
          <div className="section-header">
            <h2>📚 My Exams</h2>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/examiner-dashboard')}
            >
              Manage Exams
            </button>
          </div>

          {createdExams.length > 0 ? (
            <div className="exams-grid">
              {createdExams.slice(0, 3).map(exam => (
                <div key={exam.id} className="exam-card">
                  <h3>{exam.title}</h3>
                  <p className="exam-desc">{exam.description}</p>
                  <div className="exam-meta">
                    <span>⏱️ {exam.duration} min</span>
                    <span>⭐ {exam.total_marks} marks</span>
                  </div>
                  <span className={`badge ${exam.is_published ? 'published' : 'draft'}`}>
                    {exam.is_published ? 'Published' : 'Draft'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No exams created yet</p>
            </div>
          )}
        </div>
      )}

      <div className="dashboard-section">
        <h2>📊 Quick Actions</h2>
        <div className="actions-grid">
          {user.role === 'student' && (
            <>
              <button 
                className="action-btn"
                onClick={() => navigate('/exam-list')}
              >
                <span className="action-icon">📝</span>
                <span>Browse Exams</span>
              </button>
              <button 
                className="action-btn"
                onClick={() => navigate('/results')}
              >
                <span className="action-icon">📊</span>
                <span>View Results</span>
              </button>
            </>
          )}
          {user.role === 'examiner' && (
            <>
              <button 
                className="action-btn"
                onClick={() => navigate('/examiner-dashboard')}
              >
                <span className="action-icon">🎓</span>
                <span>Student Monitoring</span>
              </button>
              <button 
                className="action-btn"
                onClick={() => navigate('/examiner-dashboard')}
              >
                <span className="action-icon">⚠️</span>
                <span>Violations Report</span>
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;