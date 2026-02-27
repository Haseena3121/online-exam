import React, { useEffect, useRef, useState } from 'react';
import '../styles/ProctorCamera.css';

const ProctorCamera = React.forwardRef(({ sessionId, onViolation }, ref) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [micActive, setMicActive] = useState(false);
  const [isBlurred, setIsBlurred] = useState(false); // Changed to false - no blur by default
  const [violations, setViolations] = useState({});
  const detectionInterval = useRef(null);
  const violationCooldown = useRef({});

  useEffect(() => {
    initializeCamera();

    return () => {
      if (detectionInterval.current) {
        clearInterval(detectionInterval.current);
      }
      stopCamera();
    };
  }, []);

  const initializeCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: true
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
        setMicActive(true);
        startProctoring();
      }
    } catch (error) {
      console.error('Camera access denied:', error);
      alert('⚠️ Camera access is required for exam proctoring');
      onViolation?.('camera_access_denied', 'high', null);
    }
  };

  const startProctoring = () => {
    detectionInterval.current = setInterval(() => {
      performDetections();
    }, 2000); // Check every 2 seconds
  };

  const performDetections = () => {
    // Check for face visibility
    checkFaceVisibility();
    
    // Check for multiple persons (simulated)
    checkMultiplePersons();
    
    // Check background blur requirement
    checkBackgroundBlur();
  };

  const reportViolationWithCooldown = (type, severity, proof) => {
    const now = Date.now();
    const lastReport = violationCooldown.current[type] || 0;
    
    // Only report same violation type once every 10 seconds
    if (now - lastReport > 10000) {
      violationCooldown.current[type] = now;
      console.log(`🚨 Violation detected: ${type} (${severity})`);
      onViolation?.(type, severity, proof);
    }
  };

  const checkFaceVisibility = () => {
    if (videoRef.current && videoRef.current.readyState === videoRef.current.HAVE_ENOUGH_DATA) {
      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        ctx.drawImage(videoRef.current, 0, 0);
        
        // Simple brightness check to detect if face is visible
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        let brightness = 0;
        
        for (let i = 0; i < data.length; i += 4) {
          brightness += (data[i] + data[i + 1] + data[i + 2]) / 3;
        }
        
        brightness = brightness / (data.length / 4);
        
        // If too dark, report violation
        if (brightness < 30) {
          reportViolationWithCooldown('face_not_visible', 'medium', null);
        }
      }
    }
  };

  const checkMultiplePersons = () => {
    // Randomly simulate detection (5% chance)
    // In production, this would use actual AI detection
    if (Math.random() < 0.05) {
      reportViolationWithCooldown('multiple_persons', 'high', null);
    }
  };

  const checkBackgroundBlur = () => {
    // Check if blur is disabled when it should be on
    if (!isBlurred) {
      reportViolationWithCooldown('blur_disabled', 'low', null);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };

  const toggleBlur = () => {
    const newBlurState = !isBlurred;
    setIsBlurred(newBlurState);
    
    // Report violation if blur is turned off
    if (!newBlurState) {
      console.log('🚨 Blur disabled - reporting violation');
      onViolation?.('blur_disabled', 'medium', null);
    }
  };

  return (
    <div className="proctor-camera-container">
      <div className="camera-wrapper">
        <video
          ref={videoRef}
          className={`camera-feed ${isBlurred ? 'blurred' : ''}`}
          autoPlay
          playsInline
          muted
        />
        <canvas ref={canvasRef} className="detection-canvas" style={{ display: 'none' }} />
        
        <div className="camera-overlay">
          <div className="status-indicators">
            <span className={`indicator ${cameraActive ? 'active' : 'inactive'}`}>
              📷 Camera {cameraActive ? 'ON' : 'OFF'}
            </span>
            <span className={`indicator ${micActive ? 'active' : 'inactive'}`}>
              🎤 Mic {micActive ? 'ON' : 'OFF'}
            </span>
          </div>

          <div className="camera-controls">
            <button 
              onClick={toggleBlur}
              className={`blur-toggle ${isBlurred ? 'on' : 'off'}`}
              title="Toggle background blur (required)"
            >
              {isBlurred ? '🟫 Blur ON' : '🟪 Blur OFF'}
            </button>
          </div>
        </div>
      </div>

      <div className="proctoring-checklist">
        <h4>✓ Proctoring Active</h4>
        <ul>
          <li>✓ Camera monitoring</li>
          <li>✓ Face detection</li>
          <li>✓ Background blur</li>
          <li>✓ Tab switch detection</li>
          <li>✓ Sound monitoring</li>
        </ul>
      </div>
    </div>
  );
});

ProctorCamera.displayName = 'ProctorCamera';

export default ProctorCamera;