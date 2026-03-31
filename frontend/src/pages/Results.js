import API_BASE from '../config';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import '../styles/Results.css';

function Results() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { examId } = useParams();

  const [results, setResults] = useState([]);
  const [currentResult, setCurrentResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviewData, setReviewData] = useState(null);
  const [reviewLoading, setReviewLoading] = useState(false);
  const [showReview, setShowReview] = useState(false);

  const autoSubmitted = location.state?.autoSubmitted;
  const autoSubmitReason = location.state?.reason;
  const resultData = location.state?.result;

  useEffect(() => {
    if (examId && resultData) {
      setCurrentResult({ ...resultData, exam_id: examId });
      setLoading(false);
    } else {
      fetchResults();
    }
  }, [examId, resultData]);

  const fetchResults = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/results/all`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data.results);
      } else {
        setError('Failed to fetch results');
      }
    } catch {
      setError('An error occurred while fetching results');
    } finally {
      setLoading(false);
    }
  };

  const handleViewExam = async (eId) => {
    setReviewLoading(true);
    setShowReview(true);
    try {
      const res = await fetch(`${API_BASE}/api/results/${eId}/review`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setReviewData(await res.json());
      } else {
        setReviewData(null);
      }
    } catch {
      setReviewData(null);
    } finally {
      setReviewLoading(false);
    }
  };

  const formatTime = (minutes) => {
    if (!minutes && minutes !== 0) return 'N/A';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return h > 0 ? `${h}h ${m}m` : `${m} min`;
  };

  if (loading) return <div className="results-loading">Loading results...</div>;

  // Single result view (after submit / auto-submit)
  if (currentResult) {
    const pct = currentResult.percentage?.toFixed(1) || '0.0';
    const passed = currentResult.percentage >= 50 && (currentResult.final_trust_score ?? 100) >= 50;

    return (
      <div className="results-page">
        {autoSubmitted && (
          <div className="auto-submit-banner">
            <span className="auto-icon">⚠️</span>
            <div>
              <strong>Exam Auto-Submitted</strong>
              <p>{autoSubmitReason || 'Your exam was automatically submitted due to rule violations.'}</p>
              {currentResult.obtained_marks !== undefined && (
                <p className="partial-note">
                  Partial marks awarded for {currentResult.correct_answers || 0} answered question(s).
                </p>
              )}
            </div>
          </div>
        )}

        <div className="result-hero">
          <div className={`result-circle ${passed ? 'pass' : 'fail'}`}>
            <span className="result-pct">{pct}%</span>
            <span className="result-label">{passed ? 'PASSED' : 'FAILED'}</span>
          </div>
        </div>

        <div className="result-stats-grid">
          <div className="rstat">
            <span className="rstat-val">{currentResult.obtained_marks ?? 0}</span>
            <span className="rstat-lbl">Marks Obtained</span>
          </div>
          <div className="rstat">
            <span className="rstat-val">{currentResult.total_marks ?? 0}</span>
            <span className="rstat-lbl">Total Marks</span>
          </div>
          <div className="rstat">
            <span className="rstat-val green">{currentResult.correct_answers ?? 0}</span>
            <span className="rstat-lbl">Correct</span>
          </div>
          <div className="rstat">
            <span className="rstat-val red">{currentResult.violation_count ?? 0}</span>
            <span className="rstat-lbl">Violations</span>
          </div>
          <div className="rstat">
            <span className={`rstat-val ${(currentResult.final_trust_score ?? 100) < 50 ? 'red' : 'green'}`}>
              {currentResult.final_trust_score ?? 100}%
            </span>
            <span className="rstat-lbl">Trust Score</span>
          </div>
          <div className="rstat">
            <span className="rstat-val">{formatTime(currentResult.time_taken ?? currentResult.total_time_taken)}</span>
            <span className="rstat-lbl">Time Taken</span>
          </div>
        </div>

        <div className="result-actions">
          {examId && (
            <button className="btn-review" onClick={() => handleViewExam(examId)}>
              📖 View My Answers
            </button>
          )}
          <button className="btn-back-list" onClick={() => navigate('/exam-list')}>
            Back to Exams
          </button>
        </div>

        {showReview && (
          <ExamReview
            data={reviewData}
            loading={reviewLoading}
            onClose={() => setShowReview(false)}
          />
        )}
      </div>
    );
  }

  // All results list
  return (
    <div className="results-page">
      <h1 className="results-heading">📊 Your Exam Results</h1>
      {error && <div className="results-error">{error}</div>}

      {results.length === 0 ? (
        <div className="results-empty">No exam results yet.</div>
      ) : (
        <div className="results-table-wrap">
          <table className="results-table">
            <thead>
              <tr>
                <th>Exam</th>
                <th>Score</th>
                <th>%</th>
                <th>Status</th>
                <th>Violations</th>
                <th>Trust</th>
                <th>Time Taken</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {results.map(r => (
                <tr key={r.id}>
                  <td className="td-exam">{r.exam_title || `Exam #${r.exam_id}`}</td>
                  <td>{r.obtained_marks}/{r.total_marks}</td>
                  <td>{r.percentage?.toFixed(1)}%</td>
                  <td>
                    <span className={`badge-status ${r.status}`}>
                      {r.status === 'pass' ? '✓ PASS' :
                       r.status === 'fail' ? '✗ FAIL' :
                       r.status === 'auto_submitted' ? '⚡ AUTO' :
                       r.status === 'completed' ? '✓ DONE' : r.status?.toUpperCase()}
                    </span>
                  </td>
                  <td>{r.violation_count ?? 0} 🚨</td>
                  <td className={r.final_trust_score < 50 ? 'td-red' : ''}>{r.final_trust_score ?? 100}%</td>
                  <td>{formatTime(r.total_time_taken)}</td>
                  <td>{r.submitted_at ? new Date(r.submitted_at).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <button className="btn-view-exam" onClick={() => handleViewExam(r.exam_id)}>
                      📖 View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showReview && (
        <ExamReview
          data={reviewData}
          loading={reviewLoading}
          onClose={() => setShowReview(false)}
        />
      )}
    </div>
  );
}

function ExamReview({ data, loading, onClose }) {
  return (
    <div className="review-overlay" onClick={onClose}>
      <div className="review-modal" onClick={e => e.stopPropagation()}>
        <div className="review-header">
          <h2>📖 {data?.exam_title || 'Exam Review'}</h2>
          <button className="review-close" onClick={onClose}>✕</button>
        </div>

        {loading && <div className="review-loading">Loading answers...</div>}

        {!loading && !data && (
          <div className="review-error">Could not load exam review.</div>
        )}

        {!loading && data && (
          <div className="review-body">
            <div className="review-summary">
              <span>Score: <strong>{data.result.obtained_marks}/{data.result.total_marks}</strong></span>
              <span>Percentage: <strong>{data.result.percentage?.toFixed(1)}%</strong></span>
              {data.result.total_time_taken && (
                <span>Time: <strong>{data.result.total_time_taken} min</strong></span>
              )}
            </div>

            {data.questions.map((q, i) => (
              <div key={q.question_id} className={`review-question ${q.is_correct ? 'rq-correct' : q.selected_answer ? 'rq-wrong' : 'rq-skipped'}`}>
                <div className="rq-num">Q{i + 1}</div>
                <div className="rq-content">
                  <p className="rq-text">{q.question_text}</p>
                  <div className="rq-options">
                    {['a', 'b', 'c', 'd'].map(opt => {
                      const isCorrect = q.correct_answer === opt;
                      const isSelected = q.selected_answer === opt;
                      return (
                        <div
                          key={opt}
                          className={`rq-option ${isCorrect ? 'opt-correct' : ''} ${isSelected && !isCorrect ? 'opt-wrong' : ''}`}
                        >
                          <span className="opt-letter">{opt.toUpperCase()}</span>
                          <span>{q[`option_${opt}`]}</span>
                          {isCorrect && <span className="opt-tag correct">✓ Correct</span>}
                          {isSelected && !isCorrect && <span className="opt-tag wrong">✗ Your Answer</span>}
                        </div>
                      );
                    })}
                  </div>
                  {!q.selected_answer && (
                    <p className="rq-skipped-note">⚪ Not answered</p>
                  )}
                  <div className="rq-marks">
                    Marks: {q.marks_awarded}/{q.marks}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Results;
