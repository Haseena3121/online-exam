import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/ExamResults.css';

function ExamResults() {
  const { examId } = useParams();
  const { token, user } = useAuth();
  const navigate = useNavigate();
  
  const [exam, setExam] = useState(null);
  const [results, setResults] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, passed, failed
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!user || user.role !== 'examiner') {
      navigate('/dashboard');
      return;
    }
    fetchResults();
  }, [examId, user, navigate]);

  const fetchResults = async () => {
    try {
      console.log('Fetching results for exam:', examId);
      const response = await fetch(`http://localhost:5000/api/exams/${examId}/results`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Results data received:', data);
        console.log('Number of results:', data.results?.length);
        console.log('First result:', data.results?.[0]);
        setExam(data.exam);
        setResults(data.results);
      } else {
        console.error('Failed to fetch results, status:', response.status);
        const errorText = await response.text();
        console.error('Error response:', errorText);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (percentage, trustScore) => {
    if (trustScore < 50) return { text: 'AUTO-SUBMITTED', class: 'auto' };
    if (percentage >= 50) return { text: 'PASSED', class: 'pass' };
    return { text: 'FAILED', class: 'fail' };
  };

  const filteredResults = results.filter(result => {
    const matchesSearch = result.student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.student.email.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return false;
    
    if (filter === 'passed') return result.marks.percentage >= 50 && result.trust_score >= 50;
    if (filter === 'failed') return result.marks.percentage < 50 || result.trust_score < 50;
    return true;
  });

  const stats = {
    total: results.length,
    passed: results.filter(r => r.marks.percentage >= 50 && r.trust_score >= 50).length,
    failed: results.filter(r => r.marks.percentage < 50 || r.trust_score < 50).length,
    avgScore: results.length > 0 
      ? (results.reduce((sum, r) => sum + r.marks.percentage, 0) / results.length).toFixed(2)
      : 0
  };

  if (loading) return <div className="loading">Loading results...</div>;

  return (
    <div className="exam-results-page">
      <div className="results-header">
        <button onClick={() => navigate('/examiner-dashboard')} className="btn-back">
          ← Back
        </button>
        <div>
          <h1>📊 Exam Results: {exam?.title}</h1>
          <p className="exam-info">
            Duration: {exam?.duration} min | Total Marks: {exam?.total_marks}
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.total}</h3>
          <p>Total Students</p>
        </div>
        <div className="stat-card success">
          <h3>{stats.passed}</h3>
          <p>Passed</p>
        </div>
        <div className="stat-card danger">
          <h3>{stats.failed}</h3>
          <p>Failed</p>
        </div>
        <div className="stat-card">
          <h3>{stats.avgScore}%</h3>
          <p>Average Score</p>
        </div>
      </div>

      <div className="results-controls">
        <input
          type="text"
          placeholder="🔍 Search by name or email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <div className="filter-buttons">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All ({results.length})
          </button>
          <button 
            className={`filter-btn ${filter === 'passed' ? 'active' : ''}`}
            onClick={() => setFilter('passed')}
          >
            Passed ({stats.passed})
          </button>
          <button 
            className={`filter-btn ${filter === 'failed' ? 'active' : ''}`}
            onClick={() => setFilter('failed')}
          >
            Failed ({stats.failed})
          </button>
        </div>
      </div>

      <div className="results-content">
        <div className="results-list">
          {filteredResults.length === 0 ? (
            <div className="no-results">
              <p>No results found</p>
            </div>
          ) : (
            filteredResults.map((result) => {
              const status = getStatusBadge(result.marks.percentage, result.trust_score);
              return (
                <div
                  key={result.result_id}
                  className={`result-card ${selectedStudent?.result_id === result.result_id ? 'selected' : ''}`}
                  onClick={() => setSelectedStudent(result)}
                >
                  <div className="result-card-header">
                    <div>
                      <h3>{result.student.name}</h3>
                      <p className="student-email">{result.student.email}</p>
                    </div>
                    <span className={`status-badge ${status.class}`}>
                      {status.text}
                    </span>
                  </div>
                  <div className="result-card-body">
                    <div className="result-metric">
                      <span className="metric-label">Score:</span>
                      <span className="metric-value">
                        {result.marks.obtained}/{result.marks.total} ({result.marks.percentage}%)
                      </span>
                    </div>
                    <div className="result-metric">
                      <span className="metric-label">Trust Score:</span>
                      <span className={`metric-value ${result.trust_score < 50 ? 'critical' : ''}`}>
                        {result.trust_score}%
                      </span>
                    </div>
                    <div className="result-metric">
                      <span className="metric-label">Violations:</span>
                      <span className="metric-value">
                        {result.violation_count} 🚨
                      </span>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {selectedStudent && (
          <div className="student-details">
            <div className="details-header">
              <h2>{selectedStudent.student.name}</h2>
              <button onClick={() => setSelectedStudent(null)} className="btn-close">
                ✕
              </button>
            </div>

            <div className="details-body">
              <div className="detail-section">
                <h3>📊 Performance</h3>
                <div className="performance-grid">
                  <div className="perf-item">
                    <span className="perf-label">Marks Obtained:</span>
                    <span className="perf-value">{selectedStudent.marks.obtained}</span>
                  </div>
                  <div className="perf-item">
                    <span className="perf-label">Total Marks:</span>
                    <span className="perf-value">{selectedStudent.marks.total}</span>
                  </div>
                  <div className="perf-item">
                    <span className="perf-label">Percentage:</span>
                    <span className="perf-value">{selectedStudent.marks.percentage}%</span>
                  </div>
                  <div className="perf-item">
                    <span className="perf-label">Trust Score:</span>
                    <span className={`perf-value ${selectedStudent.trust_score < 50 ? 'critical' : ''}`}>
                      {selectedStudent.trust_score}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>⚠️ Violations ({selectedStudent.violation_count})</h3>
                {selectedStudent.violations.length === 0 ? (
                  <p className="no-violations">✅ No violations recorded</p>
                ) : (
                  <div className="violations-list">
                    {selectedStudent.violations.map((violation) => (
                      <div key={violation.id} className="violation-item">
                        <div className="violation-header">
                          <span className="violation-type">
                            {violation.type.replace(/_/g, ' ').toUpperCase()}
                          </span>
                          <span className={`severity-badge severity-${violation.severity || 'medium'}`}>
                            {(violation.severity || 'medium').toUpperCase()}
                          </span>
                          <span className="violation-reduction">
                            -{violation.reduction}%
                          </span>
                        </div>
                        {violation.description && (
                          <p className="violation-description">{violation.description}</p>
                        )}
                        <div className="violation-meta">
                          <span className="violation-time">
                            {new Date(violation.time).toLocaleString()}
                          </span>
                        </div>
                        
                        {/* Inline Evidence Display */}
                        {violation.evidence_url && (
                          <div className="evidence-container">
                            <div className="evidence-header">
                              <span className="evidence-label">📸 Evidence:</span>
                              <a
                                href={violation.evidence_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="evidence-link-small"
                              >
                                🔍 View Full Size
                              </a>
                            </div>
                            <div className="evidence-preview">
                              {violation.evidence_url.match(/\.(jpg|jpeg|png|gif)$/i) ? (
                                <img
                                  src={violation.evidence_url}
                                  alt={`Evidence for ${violation.type}`}
                                  className="evidence-image"
                                  onError={(e) => {
                                    e.target.style.display = 'none';
                                    e.target.nextSibling.style.display = 'block';
                                  }}
                                />
                              ) : violation.evidence_url.match(/\.(mp4|avi|mov|webm)$/i) ? (
                                <video
                                  src={violation.evidence_url}
                                  className="evidence-video"
                                  controls
                                  preload="metadata"
                                  onError={(e) => {
                                    e.target.style.display = 'none';
                                    e.target.nextSibling.style.display = 'block';
                                  }}
                                >
                                  Your browser does not support video playback.
                                </video>
                              ) : (
                                <div className="evidence-placeholder">
                                  📄 Evidence file available
                                </div>
                              )}
                              <div className="evidence-error" style={{display: 'none'}}>
                                ❌ Could not load evidence file
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="detail-section">
                <h3>📅 Submission Details</h3>
                <p><strong>Submitted At:</strong> {new Date(selectedStudent.submitted_at).toLocaleString()}</p>
                <p><strong>Status:</strong> {selectedStudent.status || 'Completed'}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ExamResults;
