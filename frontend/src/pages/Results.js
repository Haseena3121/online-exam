import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';

function Results() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [results, setResults] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResults();
  }, []);

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
                  <td>{new Date(result.submitted_at).toLocaleDateString()}</td>
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