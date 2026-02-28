import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import '../styles/Dashboard.css';

function Results() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { examId } = useParams();
  const [results, setResults] = useState([]);
  const [currentResult, setCurrentResult] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check if this is from auto-submit
  const autoSubmitted = location.state?.autoSubmitted;
  const autoSubmitReason = location.state?.reason;
  const resultData = location.state?.result;

  useEffect(() => {
    if (examId && resultData) {
      // Show specific result from auto-submit
      setCurrentResult(resultData);
      setLoading(false);
    } else {
      fetchResults();
    }
  }, [examId, resultData]);

  const fetchResults = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/results/all', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
        
        // Calculate statistics
        const passed = data.results.filter(r => r.status === 'pass').length;
        const failed = data.results.filter(r => r.status === 'fail').length;
        const avgScore = data.results.reduce((sum, r) => sum + (r.percentage || 0), 0) / (data.results.length || 1);

        setStatistics({
          total: data.results.length,
          passed,
          failed,
          avgScore: avgScore.toFixed(2)
        });
      } else {
        setError('Failed to fetch results');
      }
    } catch (error) {
      setError('An error occurred while fetching results');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading results...</div>;

  // Show single result if from auto-submit
  if (currentResult) {
    return (
      <div className="results-container">
        {autoSubmitted && (
          <div className="alert alert-warning" style={{ 
            background: '#fff3cd', 
            border: '2px solid #ffc107', 
            padding: '20px', 
            borderRadius: '10px',
            marginBottom: '20px'
          }}>
            <h2 style={{ color: '#856404', margin: '0 0 10px 0' }}>
              ⚠️ Exam Auto-Submitted
            </h2>
            <p style={{ margin: 0, fontSize: '16px' }}>
              {autoSubmitReason || 'Your exam was automatically submitted due to rule violations.'}
            </p>
          </div>
        )}

        <h1>📊 Exam Result</h1>

        <div className="result-card" style={{
          background: 'white',
          padding: '30px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          marginBottom: '20px'
        }}>
          <div className="result-header" style={{ textAlign: 'center', marginBottom: '30px' }}>
            <h2 style={{ fontSize: '48px', margin: '10px 0', color: currentResult.percentage >= 50 ? '#4caf50' : '#f44336' }}>
              {currentResult.percentage?.toFixed(2) || '0.00'}%
            </h2>
            <p style={{ fontSize: '24px', color: '#666' }}>
              {currentResult.obtained_marks} / {currentResult.total_marks} marks
            </p>
          </div>

          <div className="result-details" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="detail-item">
              <strong>Correct Answers:</strong>
              <span style={{ color: '#4caf50', fontSize: '20px', marginLeft: '10px' }}>
                ✓ {currentResult.correct_answers || 0}
              </span>
            </div>
            <div className="detail-item">
              <strong>Total Questions:</strong>
              <span style={{ fontSize: '20px', marginLeft: '10px' }}>
                {currentResult.total_questions || 0}
              </span>
            </div>
            <div className="detail-item">
              <strong>Violations:</strong>
              <span style={{ color: '#f44336', fontSize: '20px', marginLeft: '10px' }}>
                🚨 {currentResult.violation_count || 0}
              </span>
            </div>
            <div className="detail-item">
              <strong>Final Trust Score:</strong>
              <span style={{ 
                color: currentResult.final_trust_score >= 50 ? '#4caf50' : '#f44336',
                fontSize: '20px',
                marginLeft: '10px'
              }}>
                {currentResult.final_trust_score || 0}%
              </span>
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '30px' }}>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/exam-list')}
            style={{ padding: '15px 30px', fontSize: '16px' }}
          >
            Back to Exam List
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="results-container">
      <h1>📊 Your Exam Results</h1>

      {error && <div className="error-message">{error}</div>}

      {statistics && (
        <div className="statistics">
          <div className="stat-card">
            <h3>{statistics.total}</h3>
            <p>Total Exams</p>
          </div>
          <div className="stat-card success">
            <h3 style={{ color: '#4caf50' }}>{statistics.passed}</h3>
            <p>Passed ✓</p>
          </div>
          <div className="stat-card danger">
            <h3 style={{ color: '#f44336' }}>{statistics.failed}</h3>
            <p>Failed ✗</p>
          </div>
          <div className="stat-card">
            <h3>{statistics.avgScore}%</h3>
            <p>Average Score</p>
          </div>
        </div>
      )}

      <div className="results-table-wrapper">
        {results.length > 0 ? (
          <table className="results-table">
            <thead>
              <tr>
                <th>Exam</th>
                <th>Score</th>
                <th>Percentage</th>
                <th>Status</th>
                <th>Violations</th>
                <th>Trust Score</th>
                <th>Time Taken</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {results.map(result => (
                <tr key={result.id}>
                  <td className="exam-name">Exam #{result.exam_id}</td>
                  <td className="score">{result.obtained_marks}/{result.total_marks}</td>
                  <td className="percentage">{result.percentage ? result.percentage.toFixed(2) : '0.00'}%</td>
                  <td>
                    <span className={`badge badge-${result.status}`}>
                      {result.status === 'pass' ? '✓ PASS' : result.status === 'fail' ? '✗ FAIL' : '⊙ AUTO'}
                    </span>
                  </td>
                  <td className="violations">{result.violation_count} 🚨</td>
                  <td className={result.final_trust_score < 50 ? 'critical' : 'normal'}>
                    {result.final_trust_score}%
                  </td>
                  <td>{result.total_time_taken ? result.total_time_taken + ' min' : '-'}</td>
                  <td>{result.submitted_at ? new Date(result.submitted_at).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <button 
                      className="btn btn-small"
                      onClick={() => navigate(`/result/${result.exam_id}`)}
                    >
                      📋 View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <p>No exam results yet</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Results;