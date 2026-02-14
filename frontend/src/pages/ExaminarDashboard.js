import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

function ExaminerDashboard() {
  const { token } = useAuth();
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);
  const [results, setResults] = useState([]);
  const [violations, setViolations] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('results');

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/exams/my-exams', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setExams(data.exams);
      }
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchExamResults = async (examId) => {
    try {
      const [resultsRes, violationsRes] = await Promise.all([
        fetch(`http://localhost:5000/api/results/exam/${examId}/all-students`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`http://localhost:5000/api/violations/by-exam/${examId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      if (resultsRes.ok) {
        const resultsData = await resultsRes.json();
        setResults(resultsData.results);
        setStats(resultsData.statistics);
      }

      if (violationsRes.ok) {
        const violationsData = await violationsRes.json();
        setViolations(violationsData.violations);
      }

      setSelectedExam(examId);
    } catch (error) {
      console.error('Error fetching exam data:', error);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="examiner-dashboard">
      <h1>👨‍🏫 Examiner Dashboard</h1>

      <div className="examiner-grid">
        <div className="exams-sidebar">
          <h2>📚 My Exams</h2>
          <div className="exams-list">
            {exams.map(exam => (
              <div
                key={exam.id}
                className={`exam-item ${selectedExam === exam.id ? 'selected' : ''}`}
                onClick={() => fetchExamResults(exam.id)}
              >
                <h4>{exam.title}</h4>
                <p>⏱️ {exam.duration} min | ⭐ {exam.total_marks} marks</p>
                <span className={`badge ${exam.is_published ? 'published' : 'draft'}`}>
                  {exam.is_published ? '✓ Published' : '📝 Draft'}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="main-content">
          {selectedExam ? (
            <>
              <div className="stats-row">
                {stats && (
                  <>
                    <div className="stat-card">
                      <h4>Total Students</h4>
                      <p className="big-number">{stats.total_students}</p>
                    </div>
                    <div className="stat-card success">
                      <h4>Passed</h4>
                      <p className="big-number" style={{ color: '#4caf50' }}>{stats.passed}</p>
                    </div>
                    <div className="stat-card danger">
                      <h4>Failed</h4>
                      <p className="big-number" style={{ color: '#f44336' }}>{stats.failed}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Avg Score</h4>
                      <p className="big-number">{stats.average_score.toFixed(2)}%</p>
                    </div>
                  </>
                )}
              </div>

              <div className="tabs">
                <button
                  className={`tab ${activeTab === 'results' ? 'active' : ''}`}
                  onClick={() => setActiveTab('results')}
                >
                  📊 Student Results
                </button>
                <button
                  className={`tab ${activeTab === 'violations' ? 'active' : ''}`}
                  onClick={() => setActiveTab('violations')}
                >
                  🚨 Violations ({violations.length})
                </button>
              </div>

              {activeTab === 'results' && (
                <div className="tab-content">
                  <table className="results-table">
                    <thead>
                      <tr>
                        <th>Student ID</th>
                        <th>Score</th>
                        <th>Percentage</th>
                        <th>Status</th>
                        <th>Violations</th>
                        <th>Trust Score</th>
                        <th>Submitted</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.map(result => (
                        <tr key={result.id}>
                          <td>{result.student_id}</td>
                          <td>{result.obtained_marks}/{result.total_marks}</td>
                          <td>{result.percentage.toFixed(2)}%</td>
                          <td>
                            <span className={`badge badge-${result.status}`}>
                              {result.status === 'pass' ? '✓ PASS' : result.status === 'fail' ? '✗ FAIL' : '⊙ AUTO'}
                            </span>
                          </td>
                          <td>{result.violation_count}</td>
                          <td className={result.final_trust_score < 50 ? 'critical' : ''}>
                            {result.final_trust_score}%
                          </td>
                          <td>{new Date(result.submitted_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {activeTab === 'violations' && (
                <div className="tab-content">
                  {violations.length > 0 ? (
                    <div className="violations-grid">
                      {violations.map(violation => (
                        <div key={violation.id} className={`violation-card ${violation.severity}`}>
                          <div className="violation-header">
                            <span className="violation-type">🚨 {violation.violation_type}</span>
                            <span className={`severity-badge ${violation.severity}`}>
                              {violation.severity.toUpperCase()}
                            </span>
                          </div>
                          <p className="student-info">Student: {violation.student_id}</p>
                          <p className="time">{new Date(violation.timestamp).toLocaleString()}</p>
                          <p className="description">{violation.description}</p>
                          {violation.screenshot_url && (
                            <a href={violation.screenshot_url} target="_blank" rel="noopener noreferrer">
                              📷 Screenshot
                            </a>
                          )}
                          {violation.video_url && (
                            <a href={violation.video_url} target="_blank" rel="noopener noreferrer">
                              🎥 Video
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No violations for this exam</p>
                  )}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <p>Select an exam to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ExaminerDashboard;