import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

function ViolationDetails() {
  const { examId } = useParams();
  const { token } = useAuth();
  const [result, setResult] = useState(null);
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResultDetails();
  }, [examId]);

  const fetchResultDetails = async () => {
    try {
      const resultResponse = await fetch(`http://localhost:5000/api/results/detailed/${examId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (resultResponse.ok) {
        const resultData = await resultResponse.json();
        setResult(resultData.result);
      }

      const violationResponse = await fetch(`http://localhost:5000/api/violations/history/${examId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (violationResponse.ok) {
        const violationData = await violationResponse.json();
        setViolations(violationData.violations);
      }
    } catch (error) {
      setError('Failed to load details');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading details...</div>;

  return (
    <div className="violation-details-container">
      <h1>📋 Exam Details & Violations</h1>

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-summary">
          <div className="summary-card">
            <h3>📊 Score</h3>
            <p className="big-number">{result.obtained_marks}/{result.total_marks}</p>
            <p>{result.percentage ? result.percentage.toFixed(2) : '0.00'}%</p>
          </div>
          <div className="summary-card">
            <h3>📌 Status</h3>
            <p className={`status-badge ${result.status}`}>{result.status.toUpperCase()}</p>
          </div>
          <div className="summary-card">
            <h3>⚠️ Violations</h3>
            <p className="big-number">{result.violation_count}</p>
          </div>
          <div className="summary-card">
            <h3>🎯 Trust Score</h3>
            <p className={result.final_trust_score < 50 ? 'critical' : 'normal'}>
              {result.final_trust_score}%
            </p>
          </div>
          <div className="summary-card">
            <h3>⏱️ Time Taken</h3>
            <p className="big-number">{result.total_time_taken || '-'}</p>
            <p>{result.total_time_taken ? 'minutes' : ''}</p>
          </div>
        </div>
      )}

      {violations.length > 0 && (
        <div className="violations-section">
          <h2>🚨 Violations Report</h2>
          <div className="violations-list">
            {violations.map(violation => (
              <div key={violation.id} className={`violation-item ${violation.severity}`}>
                <div className="violation-header">
                  <span className="violation-type">{violation.violation_type}</span>
                  <span className={`severity-badge severity-${violation.severity}`}>
                    {violation.severity.toUpperCase()}
                  </span>
                  <span className="trust-reduction">-{violation.trust_score_reduction}%</span>
                </div>
                <p className="violation-desc">{violation.description}</p>
                <p className="violation-time">{new Date(violation.timestamp).toLocaleString()}</p>
                {violation.screenshot_url && (
                  <a href={violation.screenshot_url} target="_blank" rel="noopener noreferrer" className="proof-link">
                    📷 View Screenshot
                  </a>
                )}
                {violation.video_url && (
                  <a href={violation.video_url} target="_blank" rel="noopener noreferrer" className="proof-link">
                    🎥 View Video
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {result && result.answers && (
        <div className="answers-section">
          <h2>📝 Your Answers</h2>
          <div className="answers-list">
            {result.answers.map((answer, idx) => (
              <div key={idx} className={`answer-item ${answer.is_correct ? 'correct' : 'incorrect'}`}>
                <div className="answer-question">
                  <h4>Q{idx + 1}: {answer.question_text}</h4>
                </div>
                <div className="answer-content">
                  <p><strong>Your Answer:</strong> {answer.selected_answer || 'Not answered'}</p>
                  <p><strong>Correct Answer:</strong> {answer.correct_answer}</p>
                  <p><strong>Marks:</strong> {answer.marks_obtained}/{answer.marks_total}</p>
                  {answer.explanation && (
                    <p className="explanation"><strong>Explanation:</strong> {answer.explanation}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ViolationDetails;