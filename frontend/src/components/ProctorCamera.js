/* eslint-disable no-unused-vars, no-console, react-hooks/exhaustive-deps, no-useless-escape */
import React, { useEffect, useRef, useState } from 'react';
import * as faceapi from '@vladmandic/face-api';
import * as tf from '@tensorflow/tfjs';
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import '../styles/ProctorCamera.css';
import API_BASE from '../config';

const ProctorCamera = React.forwardRef(({ sessionId, onViolation, examDuration, referenceDescriptor }, ref) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [micActive, setMicActive] = useState(false);
  const [isBlurred, setIsBlurred] = useState(false); // Default changed to false
  const [violations, setViolations] = useState({});
  const [cocoSsdModel, setCocoSsdModel] = useState(null);
  const detectionInterval = useRef(null);
  const aiDetectionInterval = useRef(null);
  const violationCooldown = useRef({});
  const isDetectingRef = useRef(false); // Lock to prevent overlapping AI detections

  useEffect(() => {
    const loadCocoModel = async () => {
      try {
        await tf.ready();
        const model = await cocoSsd.load();
        setCocoSsdModel(model);
        console.log('📱 Phone detection model loaded');
      } catch (err) {
        console.error('Failed to load phone detection model:', err);
      }
    };

    loadCocoModel();
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
      onViolation?.('camera_access_denied', 'high', null);
      // Notify parent to show a toast — no browser alert
    }
  };

  const startProctoring = () => {
    detectionInterval.current = setInterval(async () => {
      // Prevent running a new detection if the previous one is still processing
      if (isDetectingRef.current) return;
      isDetectingRef.current = true;
      await performDetections();
      isDetectingRef.current = false;
    }, 2000); // Check every 2 seconds
  };

  const stopProctoring = () => {
    if (detectionInterval.current) {
      clearInterval(detectionInterval.current);
      detectionInterval.current = null;
    }
    if (aiDetectionInterval.current) {
      clearInterval(aiDetectionInterval.current);
      aiDetectionInterval.current = null;
    }
    console.log('⏸️ Proctoring detection stopped');
  };

  // Expose stopProctoring to parent component
  React.useImperativeHandle(ref, () => ({
    stopProctoring
  }));

  const performDetections = async () => {
    if (!videoRef.current || videoRef.current.readyState !== 4) return;
    
    try {
      const detections = await faceapi.detectAllFaces(videoRef.current).withFaceLandmarks().withFaceDescriptors();
      
      if (detections.length === 0) {
        reportViolationWithCooldown('face_not_visible', 'medium', null);
      } else if (detections.length > 1) {
        reportViolationWithCooldown('multiple_persons', 'high', null);
      } else if (detections.length === 1 && referenceDescriptor) {
        // Create an array from the referenceDescriptor object
        const refDesc = new Float32Array(Object.values(referenceDescriptor));
        const distance = faceapi.euclideanDistance(detections[0].descriptor, refDesc);
        
        // Threshold: > 0.55 generally means different person
        if (distance > 0.55) {
          console.log(`🚨 Face match failed (distance: ${distance})`);
          reportViolationWithCooldown('unauthorized_person', 'high', null); // Different person detected
        }
      }

      // Check for cell phone objects (run this even if face detection fails)
      if (cocoSsdModel && videoRef.current) {
        try {
          // Increase max detection boxes and lower threshold for better phone detection
          const predictions = await cocoSsdModel.detect(videoRef.current, 20, 0.4);
          const hasPhone = predictions.some(p => p.class === 'cell phone');
          if (hasPhone) {
            reportViolationWithCooldown('phone_detected', 'high', null);
          }
        } catch (err) {
          console.error('Phone detection error:', err);
        }
      }
    } catch (err) {
      console.error('Face detection error:', err);
    }
  };

  const reportViolationWithCooldown = (type, severity, proof) => {
    const now = Date.now();
    const lastReport = violationCooldown.current[type] || 0;
    
    // Only report same violation type once every 10 seconds
    if (now - lastReport > 10000) {
      violationCooldown.current[type] = now;
      console.log(`🚨 Violation detected: ${type} (${severity})`);
      
      // Capture screenshot as evidence
      captureScreenshot().then(screenshot => {
        onViolation?.(type, severity, screenshot);
      });
    }
  };

  const captureScreenshot = async () => {
    try {
      if (videoRef.current && videoRef.current.readyState === videoRef.current.HAVE_ENOUGH_DATA) {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoRef.current, 0, 0);
        
        // Convert to blob
        return new Promise((resolve) => {
          canvas.toBlob((blob) => {
            resolve(blob);
          }, 'image/jpeg', 0.8);
        });
      }
    } catch (error) {
      console.error('Error capturing screenshot:', error);
    }
    return null;
  };

  const checkBackgroundBlur = () => {
    // Check if blur is disabled when it should be on
    // Disabled blur violation logic per user request
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };

  const toggleBlur = () => {
    const newBlurState = !isBlurred;
    setIsBlurred(newBlurState);

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