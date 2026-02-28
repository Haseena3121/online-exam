import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/LiveMonitoring.css';

function LiveMonitoring() {
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const [activeSessions, setActiveSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'examiner') {
      navigate('/dashboard');
      return;
    }

    fetchActiveSessions();

    // Auto-refresh every 5 seconds
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        fetchActiveSessions();
      }, 5000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh, user, navigate]);

  const fetchActiveSessions = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/proctoring/monitor/active-sessions', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setActiveSessions(data.active_sessions || []);
      }
    } catch (error) {
      console.error('Error fetching active sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSessionDetails = async (sessionId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/proctoring/monitor/session/${sessionId}/details`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSelectedSession(data);
      }
    } catch (error) {
      console.error('Error fetching session details:', error);
    }
  };

  const getTrustScoreClass = (score) => {
    if (score >= 80) return 'trust-high';
    if (score >= 50) return 'trust-medium';
    return 'trust-low';
  };

  const getViolationIcon = (type) => {
    const icons = {
      'tab_switch': '🔄',
      'copy_attempt': '📋',
      'paste_attempt': '📌',
      'cut_attempt': '✂️',
      'blur_disabled': '🟪',
      'multiple_persons': '👥',
      'face_not_visible': '👤',
      'suspicious_behavior': '⚠️',
      'camera_access_denied': '📷'
    };
    return icons[type] || '⚠️';
  };

  const formatTime = (isoString) => {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleTimeString();
  };

  const getElapsedTime = (startTime) => {
    if (!startTime) return '0:00';
    const start = new Date(startTime);
    const now = new Date();
    const diff = Math.floor((now - start) / 1000);
    const minutes = Math.floor(diff / 60);
    const seconds = diff % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return <div className="loading">Loading monitoring dashboard...</div>;
  }

  return (
    <div className="live-monitoring">
      <div className="monitoring-header">
        <h1>🎥 Live Exam Monitoring</h1>
        <div className="header-controls">
          <label className="auto-refresh">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh (5s)
          </label>
          <button onClick={fetchActiveSessions} className="btn-refresh">
            🔄 Refresh Now
          </button>
        </div>
      </div>

      {activeSessions.length === 0 ? (
        <div className="no-sessions">
          <h2>📭 No Active Exams</h2>
          <p>No students are currently taking exams.</p>
          <p>Active sessions will appear here in real-time.</p>
        </div>
      ) : (
        <div className="monitoring-content">
          <div className="sessions-list">
            <h2>Active Sessions ({activeSessions.length})</h2>
            {activeSessions.map((session) => (
              <div
                key={session.session_id}
                className={`session-card ${selectedSession?.session?.id === session.session_id ? 'selected' : ''}`}
                onClick={() => fetchSessionDetails(session.session_id)}
              >
                <div className="session-header">
                  <h3>{session.student.name}</h3>
                  <span className={`trust-badge ${getTrustScoreClass(session.trust_score)}`}>
                    {session.trust_score}%
                  </span>
                </div>
                <div className="session-info">
                  <p><strong>Exam:</strong> {session.exam.title}</p>
                  <p><strong>Started:</strong> {formatTime(session.start_time)}</p>
                  <p><strong>Elapsed:</strong> {getElapsedTime(session.start_time)}</p>
                </div>
                <div className="session-status">
                  <span className={session.camera_active ? 'status-on' : 'status-off'}>
                    📷 {session.camera_active ? 'ON' : 'OFF'}
                  </span>
                  <span className={session.mic_active ? 'status-on' : 'status-off'}>
                    🎤 {session.mic_active ? 'ON' : 'OFF'}
                  </span>
                  <span className="violation-count">
                    ⚠️ {session.violations.length} violations
                  </span>
                </div>
              </div>
            ))}
          </div>

          {selectedSession && (
            <div className="session-details">
              <div className="details-header">
                <h2>Session Details</h2>
                <button onClick={() => setSelectedSession(null)} className="btn-close">
                  ✕
                </button>
              </div>

              <div className="details-content">
                <div className="detail-section">
                  <h3>👤 Student Information</h3>
                  <p><strong>Name:</strong> {selectedSession.student.name}</p>
                  <p><strong>Email:</strong> {selectedSession.student.email}</p>
                  <p><strong>ID:</strong> {selectedSession.student.id}</p>
                </div>

                <div className="detail-section">
                  <h3>📝 Exam Information</h3>
                  <p><strong>Title:</strong> {selectedSession.exam.title}</p>
                  <p><strong>Duration:</strong> {selectedSession.exam.duration} minutes</p>
                  <p><strong>Total Marks:</strong> {selectedSession.exam.total_marks}</p>
                </div>

                <div className="detail-section">
                  <h3>📊 Session Status</h3>
                  <p><strong>Trust Score:</strong> 
                    <span className={`trust-badge ${getTrustScoreClass(selectedSession.session.trust_score)}`}>
                      {selectedSession.session.trust_score}%
                    </span>
                  </p>
                  <p><strong>Status:</strong> {selectedSession.session.status}</p>
                  <p><strong>Started:</strong> {formatTime(selectedSession.session.start_time)}</p>
                  <p><strong>Camera:</strong> {selectedSession.session.camera_active ? '✅ Active' : '❌ Inactive'}</p>
                  <p><strong>Microphone:</strong> {selectedSession.session.mic_active ? '✅ Active' : '❌ Inactive'}</p>
                </div>

                <div className="detail-section violations-section">
                  <h3>⚠️ Violations ({selectedSession.violation_count})</h3>
                  {selectedSession.violations.length === 0 ? (
                    <p className="no-violations">✅ No violations recorded</p>
                  ) : (
                    <div className="violations-list">
                      {selectedSession.violations.map((violation) => (
                        <div key={violation.id} className="violation-item">
                          <span className="violation-icon">
                            {getViolationIcon(violation.type)}
                          </span>
                          <div className="violation-info">
                            <strong>{violation.type.replace(/_/g, ' ').toUpperCase()}</strong>
                            <span className="violation-time">{formatTime(violation.time)}</span>
                          </div>
                          <span className="violation-reduction">
                            -{violation.reduction}%
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default LiveMonitoring;
