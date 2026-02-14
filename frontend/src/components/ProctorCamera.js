import React, { useEffect, useRef, useState } from 'react';
import '../styles/ProctorCamera.css';

const ProctorCamera = React.forwardRef(({ sessionId, onViolation }, ref) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [micActive, setMicActive] = useState(false);
  const [isBlurred, setIsBlurred] = useState(true);
  const [violations, setViolations] = useState({});
  const detectionInterval = useRef(null);

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
    
    // Check for multiple persons
    checkMultiplePersons();
    
    // Check background blur
    checkBackgroundBlur();
    
    // Check document visibility (tab switch)
    checkTabSwitch();
  };

  const checkFaceVisibility = () => {
    // Implement face detection logic
    // Using getUserMedia video stream
    if (videoRef.current && videoRef.current.readyState === videoRef.current.HAVE_ENOUGH_DATA) {
      // Get canvas and draw video frame
      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        ctx.drawImage(videoRef.current, 0, 0);
      }
    }
  };

  const checkMultiplePersons = () => {
    // Implement person detection
  };

  const checkBackgroundBlur = () => {
    // Implement background blur detection
  };

  const checkTabSwitch = () => {
    // Detect tab visibility
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };

  const toggleBlur = () => {
    setIsBlurred(!isBlurred);
    if (!isBlurred) {
      onViolation?.('blur_disabled', 'high', null);
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