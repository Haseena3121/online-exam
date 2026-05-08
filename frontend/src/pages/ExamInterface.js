/* eslint-disable no-unused-vars, no-console, react-hooks/exhaustive-deps, no-useless-escape */
import api from '../services/api';
import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ProctorCamera from '../components/ProctorCamera';
import CountdownTimer from '../components/CountdownTimer';
import * as faceapi from '@vladmandic/face-api';
import ViolationWarning from '../components/ViolationWarning';
import Toast from '../components/Toast';
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
  const [toast, setToast] = useState(null);
  const showToast = (message, type = 'info') => setToast({ message, type });
  const [examStarted, setExamStarted] = useState(false); // New flag
  const [verified, setVerified] = useState(false); // For Pre-Exam Check
  const [referenceDescriptor, setReferenceDescriptor] = useState(null);
  const [verifyingCamera, setVerifyingCamera] = useState(false);
  const [modelsLoaded, setModelsLoaded] = useState(false);
  const [setupError, setSetupError] = useState("");
  const cameraRef = useRef(null);
  const timerIntervalRef = useRef(null);
  const setupVideoRef = useRef(null);
  const warningTimeoutRef = useRef(null);

  // Load models on mount
  useEffect(() => {
    const loadModels = async () => {
      try {
        await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        setModelsLoaded(true);
        console.log('Face API models loaded');
      } catch (err) {
        console.error('Failed to load Face API models', err);
        setSetupError('Failed to load AI proctoring models. Please refresh.');
      }
    };
    loadModels();
  }, []);

  // Setup Camera for pre-exam verification
  useEffect(() => {
    if (!loading && exam && !verified) {
      startSetupCamera();
    }
    return () => {
      if (setupVideoRef.current && setupVideoRef.current.srcObject) {
        setupVideoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, [loading, exam, verified]);

  const startSetupCamera = async () => {
    try {
      // Camera API requires HTTPS or localhost — check first
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setSetupError('Camera access requires HTTPS. Please use https:// or access from localhost. On Chrome mobile, go to chrome://flags and enable "Insecure origins treated as secure" for this address.');
        return;
      }
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: true });
      if (setupVideoRef.current) {
        setupVideoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error(err);
      setSetupError('Camera and Microphone access is required to start the exam.');
    }
  };

  const handleCaptureReference = async () => {
    if (!modelsLoaded || !setupVideoRef.current) return;
    setVerifyingCamera(true);
    setSetupError("");
    
    try {
      const detections = await faceapi.detectAllFaces(setupVideoRef.current).withFaceLandmarks().withFaceDescriptors();
      
      if (detections.length === 0) {
        setSetupError("No face detected! Please ensure your face is clearly visible in poor lighting.");
      } else if (detections.length > 1) {
        setSetupError("Multiple persons detected! Ensure you are alone in the room.");
      } else {
        // Success! Save the descriptor
        setReferenceDescriptor(detections[0].descriptor);
        setVerified(true);
        
        // Stop setup camera to release resource for Exam camera
        if (setupVideoRef.current.srcObject) {
            setupVideoRef.current.srcObject.getTracks().forEach(track => track.stop());
        }
      }
    } catch (err) {
      console.error("Verification error:", err);
      setSetupError("Error capturing face. Please try again.");
    }
    setVerifyingCamera(false);
  };

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
        setViolationMessage('⚠️ VIOLATION DETECTED: You switched to another tab! This has been recorded.');
        if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
        warningTimeoutRef.current = setTimeout(() => setShowWarning(false), 6000);
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

  // Detect copy/paste/cut
  useEffect(() => {
    const handleCopy = (e) => {
      e.preventDefault();
      reportViolation('copy_attempt', 'high', null);
      setShowWarning(true);
      setViolationMessage('⚠️ VIOLATION DETECTED: COPYING IS NOT ALLOWED! This action has been recorded.');
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
      warningTimeoutRef.current = setTimeout(() => setShowWarning(false), 6000);
    };

    const handlePaste = (e) => {
      e.preventDefault();
      reportViolation('paste_attempt', 'high', null);
      setShowWarning(true);
      setViolationMessage('⚠️ VIOLATION DETECTED: PASTING IS NOT ALLOWED! This action has been recorded.');
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
      warningTimeoutRef.current = setTimeout(() => setShowWarning(false), 6000);
    };

    const handleCut = (e) => {
      e.preventDefault();
      reportViolation('cut_attempt', 'medium', null);
      setShowWarning(true);
      setViolationMessage('⚠️ VIOLATION DETECTED: CUTTING TEXT IS NOT ALLOWED! This action has been recorded.');
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
      warningTimeoutRef.current = setTimeout(() => setShowWarning(false), 6000);
    };

    document.addEventListener('copy', handleCopy);
    document.addEventListener('paste', handlePaste);
    document.addEventListener('cut', handleCut);

    return () => {
      document.removeEventListener('copy', handleCopy);
      document.removeEventListener('paste', handlePaste);
      document.removeEventListener('cut', handleCut);
    };
  }, [sessionStatus]);

  const fetchExamDetails = async () => {
    try {
      console.log('Fetching exam details for exam ID:', examId);
      const response = await api.get(`/exams/${examId}`);
      const data = response.data;
      console.log('Exam data received:', data);
      setExam(data);
      setQuestions(data.questions || []);
      if (!data.questions || data.questions.length === 0) {
        showToast('This exam has no questions. Please contact the examiner.', 'warning');
      }
    } catch (error) {
      console.error('Error fetching exam:', error);
      showToast('Failed to load exam. Please try again.', 'error');
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
    if (violationType === 'camera_access_denied') {
      showToast('⚠️ Camera access is required for exam proctoring', 'warning');
    }
    reportViolation(violationType, severity, proof);
  };

  const reportViolation = async (violationType, severity, proof) => {
    if (sessionStatus !== 'active') return;

    try {
      console.log(`📊 Reporting violation: ${violationType} (${severity})`);
      
      const formData = new FormData();
      formData.append('violation_type', violationType);
      formData.append('severity', severity);

      formData.append('description', 'Violation detected during exam');
      if (proof) formData.append('evidence', proof, 'screenshot.jpg');

      const response = await api.post('/proctoring/violation', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const data = response.data;

      console.log(`✅ Violation reported. New trust score: ${data.current_trust_score}%`);
      setTrustScore(data.current_trust_score);

      // Function to handle showing the warning with a clear timeout
      const showDetailedWarning = (message) => {
        setShowWarning(true);
        setViolationMessage(message);
        if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
        warningTimeoutRef.current = setTimeout(() => setShowWarning(false), 6000);
      };

      if (violationType === 'unauthorized_person') {
        showDetailedWarning(`⚠️ VIOLATION DETECTED: Unauthorized person found in camera view! Your trust score decreased to ${data.current_trust_score}%.`);
      } else if (violationType === 'phone_detected') {
        showDetailedWarning(`⚠️ VIOLATION DETECTED: Mobile phone detected in your hands! Your trust score decreased to ${data.current_trust_score}%.`);
      } else if (violationType === 'multiple_persons') {
        showDetailedWarning(`⚠️ VIOLATION DETECTED: Multiple people found in the camera view! Your trust score decreased to ${data.current_trust_score}%.`);
      } else if (violationType === 'face_not_visible') {
        showDetailedWarning(`⚠️ VIOLATION DETECTED: Your face is not clearly visible in the camera! Your trust score decreased to ${data.current_trust_score}%.`);
      } else if (data.warning) {
        showDetailedWarning(`⚠️ WARNING: Trust Score ${data.current_trust_score}% - Please continue following the rules!`);
      }

      if (data.critical_message) {
        setSessionStatus('ended');
        if (cameraRef.current?.stopProctoring) cameraRef.current.stopProctoring();
        showToast('🔴 ' + data.critical_message, 'error');
        setTimeout(() => navigate('/results', { state: { autoSubmitted: true, reason: 'Trust score fell below 50%' } }), 2000);
      }
    } catch (error) {
      const errData = error.response?.data;
      if (errData?.error === 'No active session' || error.response?.status === 404) {
        console.log('⏸️ Session ended - stopping violation reports');
        setSessionStatus('ended');
        if (cameraRef.current?.stopProctoring) cameraRef.current.stopProctoring();
      } else {
        console.error('❌ Error reporting violation:', error);
      }
    }
  };

  const handleSubmitExam = async () => {
    try {
      setSessionStatus('submitting');
      if (cameraRef.current?.stopProctoring) cameraRef.current.stopProctoring();

      const submissionData = {
        answers: questions.map(q => ({
          question_id: q.id,
          selected_answer: answers[q.id] || ''
        }))
      };

      const response = await api.post('/proctoring/submit', submissionData);
      navigate(`/result/${examId}`, { state: { result: response.data.result } });
    } catch (error) {
      console.error('Submit error:', error);
      showToast('Error submitting exam: ' + (error.response?.data?.error || error.message), 'error');
      setSessionStatus('active');
    }
  };

  const autoSubmitExam = async () => {
    try {
      setSessionStatus('submitting');
      if (cameraRef.current?.stopProctoring) cameraRef.current.stopProctoring();

      const submissionData = {
        answers: questions.map(q => ({
          question_id: q.id,
          selected_answer: answers[q.id] || ''
        })),
        auto_submitted: true
      };

      const response = await api.post('/proctoring/submit', submissionData);
      navigate(`/result/${examId}`, { state: { result: response.data.result, autoSubmitted: true } });
    } catch (error) {
      console.error('Auto-submit error:', error);
      navigate(`/result/${examId}`);
    }
  };

  if (loading) {
    return <div className="loading">Loading exam...</div>;
  }

  if (!exam || questions.length === 0) {
    return <div className="error">Exam not found</div>;
  }

  // PRE-EXAM SETUP SCREEN
  if (!verified) {
    return (
      <div className="exam-screen" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5' }}>
        <div style={{ background: 'white', padding: '30px', borderRadius: '10px', boxShadow: '0 4px 15px rgba(0,0,0,0.1)', maxWidth: '600px', textAlign: 'center' }}>
          <h2 style={{ marginBottom: '20px', color: '#333' }}>📸 Camera & Face Verification</h2>
          <p style={{ marginBottom: '20px', color: '#666' }}>Before starting the exam, we need to capture a reference photo to verify your identity throughout the session.</p>
          
          <div style={{ position: 'relative', width: '100%', maxWidth: '400px', margin: '0 auto 20px', borderRadius: '8px', overflow: 'hidden', backgroundColor: '#000' }}>
            <video 
              ref={setupVideoRef} 
              autoPlay 
              playsInline 
              muted 
              style={{ width: '100%', display: 'block', transform: 'scaleX(-1)' }} 
            />
          </div>

          {setupError && (
            <div style={{ color: '#d32f2f', backgroundColor: '#ffebee', padding: '10px', borderRadius: '5px', marginBottom: '20px' }}>
              ⚠️ {setupError}
            </div>
          )}

          <button 
            className="btn btn-primary btn-large" 
            onClick={handleCaptureReference}
            disabled={!modelsLoaded || verifyingCamera || !!setupError.includes("Camera")}
            style={{ width: '100%', padding: '15px', fontSize: '1.1rem' }}
          >
            {!modelsLoaded ? '⏳ Loading AI Models...' : verifyingCamera ? '📷 Capturing...' : 'Capture Reference & Start Exam'}
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const answered = Object.keys(answers).length;

  return (
    <div className="exam-screen">
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
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
              referenceDescriptor={referenceDescriptor}
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