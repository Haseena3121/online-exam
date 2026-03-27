import React, { useEffect, useState } from 'react';
import '../styles/ViolationWarning.css';

function ViolationWarning({ message, onClose }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Trigger pop animation
    requestAnimationFrame(() => setVisible(true));
    playBeep();
  }, []);

  const playBeep = () => {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();

      // Two beeps
      [0, 0.35].forEach(offset => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.value = 880;
        osc.type = 'square';
        gain.gain.setValueAtTime(0.25, ctx.currentTime + offset);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + offset + 0.25);
        osc.start(ctx.currentTime + offset);
        osc.stop(ctx.currentTime + offset + 0.25);
      });
    } catch (e) {
      // Audio not available
    }
  };

  return (
    <div className={`vw-overlay ${visible ? 'vw-show' : ''}`}>
      <div className={`vw-popup ${visible ? 'vw-pop' : ''}`}>
        <div className="vw-icon">⚠️</div>
        <div className="vw-body">
          <div className="vw-title">VIOLATION DETECTED</div>
          <div className="vw-message">{message}</div>
        </div>
        {onClose && (
          <button className="vw-close" onClick={onClose}>✕</button>
        )}
      </div>
    </div>
  );
}

export default ViolationWarning;
