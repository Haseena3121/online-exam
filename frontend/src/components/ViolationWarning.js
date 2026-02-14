import React, { useEffect } from 'react';
import '../styles/ProctorCamera.css';

function ViolationWarning({ message }) {
  useEffect(() => {
    // Play warning sound
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gain = audioContext.createGain();
      
      oscillator.connect(gain);
      gain.connect(audioContext.destination);
      
      oscillator.frequency.value = 800;
      oscillator.type = 'sine';
      
      gain.gain.setValueAtTime(0.3, audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
      console.log('Audio context not available');
    }
  }, []);

  return (
    <div className="violation-warning">
      <div className="warning-content">
        <span className="warning-icon">⚠️</span>
        <span className="warning-message">{message}</span>
      </div>
    </div>
  );
}

export default ViolationWarning;