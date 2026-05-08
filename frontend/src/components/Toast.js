import React, { useEffect } from 'react';
import './Toast.css';

/**
 * Toast notification component.
 * Props:
 *   message  – text to display
 *   type     – 'success' | 'error' | 'warning' | 'info'
 *   onClose  – callback to clear the message
 *   duration – ms before auto-dismiss (default 3000)
 */
function Toast({ message, type = 'info', onClose, duration = 3000 }) {
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(onClose, duration);
    return () => clearTimeout(t);
  }, [message, duration, onClose]);

  if (!message) return null;

  const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };

  return (
    <div className={`toast toast-${type}`} role="alert">
      <span className="toast-icon">{icons[type]}</span>
      <span className="toast-message">{message}</span>
      <button className="toast-close" onClick={onClose} aria-label="Close">×</button>
    </div>
  );
}

export default Toast;
