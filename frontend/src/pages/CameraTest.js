import React, { useRef, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/CameraTest.css';

function CameraTest() {
  const videoRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [micActive, setMicActive] = useState(false);
  const [error, setError] = useState('');
  const [checking, setChecking] = useState(true);
  const navigate = useNavigate();
  const { examId } = useParams();

  useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: true
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
        setMicActive(true);
      }
    } catch (err) {
      setError('Camera/Microphone access denied. Please allow permissions and refresh.');
    } finally {
      setChecking(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(t => t.stop());
    }
  };

  const handleContinue = () => {
    stopCamera();
    if (examId) {
      navigate(`/exam/${examId}/acceptance`);
    } else {
      navigate('/exam-list');
    }
  };

  const checks = [
    { label: 'Camera Active', ok: cameraActive },
    { label: 'Microphone Active', ok: micActive },
    { label: 'Browser Compatible', ok: true },
    { label: 'Stable Connection', ok: true },
  ];

  return (
    <div className="camera-test-page">
      <div className="camera-test-card">
        <div className="camera-test-header">
          <div className="step-indicator">
            <div className="step active">1</div>
            <div className="step-line active" />
            <div className="step">2</div>
          </div>
          <h1>📹 System Check</h1>
          <p>Make sure your camera and microphone are working before the exam</p>
        </div>

        {error && <div className="camera-error">{error}</div>}

        <div className="camera-preview-box">
          {checking && <div className="camera-checking">Checking camera...</div>}
          <video ref={videoRef} autoPlay playsInline muted className="camera-preview-video" />
          {cameraActive && <div className="camera-live-badge">● LIVE</div>}
        </div>

        <div className="system-checks">
          {checks.map((c, i) => (
            <div key={i} className={`check-item ${c.ok ? 'ok' : 'fail'}`}>
              <span className="check-icon">{c.ok ? '✅' : '❌'}</span>
              <span>{c.label}</span>
              <span className="check-status">{c.ok ? 'Ready' : 'Not Ready'}</span>
            </div>
          ))}
        </div>

        <div className="camera-test-actions">
          <button onClick={() => navigate('/exam-list')} className="btn-ghost">
            ← Back
          </button>
          <button
            onClick={handleContinue}
            disabled={!cameraActive}
            className={`btn-proceed ${cameraActive ? 'enabled' : 'disabled'}`}
          >
            Continue to Rules →
          </button>
        </div>
      </div>
    </div>
  );
}

export default CameraTest;
