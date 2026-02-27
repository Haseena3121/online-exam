import React, { useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CameraTest() {
  const videoRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
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
      }
    } catch (err) {
      setError('Camera access denied. Please allow camera permissions.');
      console.error('Camera error:', err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '40px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '15px',
        padding: '40px',
        maxWidth: '800px',
        width: '100%',
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)'
      }}>
        <h1 style={{ color: '#667eea', marginBottom: '20px' }}>
          📹 Camera & Microphone Test
        </h1>
        
        {error && (
          <div style={{
            background: '#ffebee',
            color: '#c62828',
            padding: '15px',
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            {error}
          </div>
        )}

        <div style={{
          background: '#000',
          borderRadius: '10px',
          overflow: 'hidden',
          marginBottom: '20px'
        }}>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{ width: '100%', height: 'auto', display: 'block' }}
          />
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          marginBottom: '20px',
          padding: '15px',
          background: cameraActive ? '#e8f5e9' : '#ffebee',
          borderRadius: '8px'
        }}>
          <span style={{ fontSize: '24px' }}>
            {cameraActive ? '✅' : '❌'}
          </span>
          <span style={{ fontWeight: '600' }}>
            {cameraActive ? 'Camera is working!' : 'Camera not detected'}
          </span>
        </div>

        <div style={{
          background: '#f5f5f5',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <h3 style={{ marginTop: 0 }}>AI Proctoring Features:</h3>
          <ul style={{ lineHeight: '1.8' }}>
            <li>✅ Face Detection - Ensures you're present</li>
            <li>✅ Multiple Person Detection - Detects if someone else appears</li>
            <li>✅ Phone Detection - Alerts if phone is detected</li>
            <li>✅ Eye Gaze Tracking - Monitors where you're looking</li>
            <li>✅ Head Movement Detection - Tracks unusual movements</li>
            <li>✅ Sound Detection - Monitors audio for voices</li>
            <li>✅ Tab Switch Detection - Detects if you leave the exam</li>
          </ul>
        </div>

        <div style={{ display: 'flex', gap: '15px' }}>
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              padding: '12px 24px',
              background: '#f0f0f0',
              border: '2px solid #667eea',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600'
            }}
          >
            ← Back to Dashboard
          </button>
          
          <button
            onClick={() => navigate('/exam-list')}
            disabled={!cameraActive}
            style={{
              padding: '12px 24px',
              background: cameraActive ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: cameraActive ? 'pointer' : 'not-allowed',
              fontWeight: '600'
            }}
          >
            Continue to Exams →
          </button>
        </div>
      </div>
    </div>
  );
}

export default CameraTest;