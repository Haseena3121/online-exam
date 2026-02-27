import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ProctorCamera from '../components/ProctorCamera';
import CountdownTimer from '../components/CountdownTimer';
import ViolationWarning from '../components/ViolationWarning';
import '../styles/ExamScreen.css';

function ExamInterface() {
  const { examId, sessionId } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();
  
  const [exam, setExam] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(null); // Changed from 0 to null
  const [sessionStatus, setSessionStatus] = useState('active');
  const [trustScore, setTrustScore] = useState(100);
  const [showWarning, setShowWarning] = useState(false);
  const [violationMessage, setViolationMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [examStarted, setExamStarted] = useState(false); // New flag
  const cameraRef = useRef(null);
  const timerIntervalRef = useRef(null);

  useEffect(() => {
    fetchExamDetails();
  }, [examId]);

  useEffect(() => {
    if (exam && exam.duration) {
      setTimeLeft(exam.duration * 60); // Convert to seconds
      setExamStarted(true);
    }
  }, [exam]);

  useEffect(() => {
    // Only start timer if exam has started and time is set
    if (sessionStatus === 'active' && timeLeft !== null && timeLeft > 0 && examStarted) {
      timerIntervalRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmitExam();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (timeLeft === 0 && sessionStatus === 'active' && examStarted) {
      handleSubmitExam();
    }

    return () => {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
    };
  }, [timeLeft, sessionStatus, examStarted]);

  // Prevent tab switching
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden && sessionStatus === 'active') {
        reportViolation('tab_switch', 'high', null);
        setShowWarning(true);
        setViolationMessage('⚠️ You switched to another tab! This is a violation.');
        setTimeout(() => setShowWarning(false), 5000);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [sessionStatus]);

  // Prevent right-click and shortcuts
  useEffect(() => {
    const handleContextMenu = (e) => e.preventDefault();
    const handleKeyDown = (e) => {
      if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I') || 
          (e.ctrlKey && e.shiftKey && e.key === 'C') || (e.ctrlKey && e.key === 's')) {
        e.preventDefault();
        reportViolation('suspicious_behavior', 'high', null);
      }
    };

    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const fetchExamDetails = async () => {
    try {
      console.log('Fetching exam details for exam ID:', examId);
      const response = await fetch(`http://localhost:5000/api/exams/${examId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Exam data received:', data);
        setExam(data);
        setQuestions(data.questions || []);
        
        if (!data.questions || data.questions.length === 0) {
          alert('This exam has no questions. Please contact the examiner.');
        }
      } else {
        console.error('Failed to fetch exam:', response.status);
        alert('Failed to load exam. Please try again.');
        navigate('/exam-list');
      }
    } catch (error) {
      console.error('Error fetching exam:', error);
      alert('Error loading exam. Please check your connection.');
      navigate('/exam-list');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleViolation = (violationType, severity, proof) => {
    reportViolation(violationType, severity, proof);
  };

  const reportViolation = async (violationType, severity, proof) => {
    try {
      console.log(`📊 Reporting violation: ${violationType} (${severity})`);
      
      const formData = new FormData();
      formData.append('violation_type', violationType);
      formData.append('severity', severity);
      formData.append('description', `Violation detected during exam`);
      
      if (proof) {
        formData.append('evidence', proof);
      }

      const response = await fetch('http://localhost:5000/api/proctoring/violation', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`✅ Violation reported. New trust score: ${data.current_trust_score}%`);
        setTrustScore(data.current_trust_score);
        
        if (data.warning) {
          setShowWarning(true);
          setViolationMessage('⚠️ WARNING: Your trust score is low. Continue following rules!');
          setTimeout(() => setShowWarning(false), 5000);
        }
        
        if (data.critical_message) {
          alert('🔴 ' + data.critical_message);
          handleSubmitExam();
        }
      } else {
        const errorData = await response.json();
        console.error('❌ Failed to report violation:', response.status, errorData);
      }
    } catch (error) {
      console.error('❌ Error reporting violation:', error);
    }
  };

  const handleSubmitExam = async () => {
    try {
      setSessionStatus('submitting');

      const submissionData = {
        answers: questions.map(q => ({
          question_id: q.id,
          selected_answer: answers[q.id] || ''
        }))
      };

      const response = await fetch('http://localhost:5000/api/proctoring/submit', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(submissionData)
      });

      if (response.ok) {
        const data = await response.json();
        navigate(`/result/${examId}`, { state: { result: data.result } });
      } else {
        alert('Error submitting exam');
      }
    } catch (error) {
      console.error('Error submitting exam:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading exam...</div>;
  }

  if (!exam || questions.length === 0) {
    return <div className="error">Exam not found</div>;
  }

  const currentQuestion = questions[currentQuestionIndex];
  const answered = Object.keys(answers).length;

  return (
    <div className="exam-screen">
      {showWarning && <ViolationWarning message={violationMessage} />}
      
      <div className="exam-header">
        <div className="exam-title">{exam.title}</div>
        <div className="exam-info">
          <span 
            className={`trust-score ${trustScore < 50 ? 'critical' : 'normal'}`}
            title="Trust Score: Falls below 50% = Auto-submission"
          >
            🎯 Trust: {trustScore}%
          </span>
          <CountdownTimer timeLeft={timeLeft} totalTime={exam.duration * 60} />
        </div>
      </div>

      <div className="exam-container">
        <div className="exam-main">
          <div className="question-section">
            <div className="question-header">
              <h3>Question {currentQuestionIndex + 1} of {questions.length}</h3>
              <span className="question-marks">⭐ {currentQuestion.marks} marks</span>
            </div>

            <div className="question-content">
              <p className="question-text">{currentQuestion.question_text}</p>
              
              {currentQuestion.question_type === 'mcq' && (
                <div className="options">
                  {['a', 'b', 'c', 'd'].map(opt => (
                    <label key={opt} className="option">
                      <input
                        type="radio"
                        name={`q${currentQuestion.id}`}
                        value={opt}
                        checked={answers[currentQuestion.id] === opt}
                        onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                      />
                      <span className="option-text">
                        <strong>{opt.toUpperCase()}:</strong> {currentQuestion[`option_${opt}`]}
                      </span>
                    </label>
                  ))}
                </div>
              )}

              {currentQuestion.question_type === 'short-answer' && (
                <textarea
                  className="answer-textarea"
                  value={answers[currentQuestion.id] || ''}
                  onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                  placeholder="Enter your answer here..."
                />
              )}
            </div>

            <div className="question-controls">
              <button 
                onClick={handlePreviousQuestion} 
                disabled={currentQuestionIndex === 0}
                className="btn btn-secondary"
              >
                ← Previous
              </button>
              
              <span className="question-counter">
                {currentQuestionIndex + 1} / {questions.length}
              </span>
              
              <button 
                onClick={handleNextQuestion} 
                disabled={currentQuestionIndex === questions.length - 1}
                className="btn btn-secondary"
              >
                Next →
              </button>

              <button 
                onClick={handleSubmitExam}
                className="btn btn-primary btn-large"
                title="Submit the exam now"
              >
                Submit Exam ✓
              </button>
            </div>
          </div>

          <div className="proctor-section">
            <ProctorCamera 
              ref={cameraRef}
              sessionId={sessionId}
              onViolation={handleViolation}
              examDuration={exam.duration}
            />
            
            <div className="exam-progress">
              <h4>📊 Progress</h4>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${(answered / questions.length) * 100}%` }}></div>
              </div>
              <p><strong>{answered}</strong> of <strong>{questions.length}</strong> answered</p>
            </div>
          </div>
        </div>

        <div className="questions-list">
          <h4>Questions</h4>
          <div className="question-list-items">
            {questions.map((q, idx) => (
              <button
                key={q.id}
                className={`question-item ${idx === currentQuestionIndex ? 'active' : ''} ${answers[q.id] ? 'answered' : ''}`}
                onClick={() => setCurrentQuestionIndex(idx)}
                title={`Q${idx + 1}: ${answers[q.id] ? 'Answered' : 'Not answered'}`}
              >
                {idx + 1}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExamInterface;