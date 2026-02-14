import React from 'react';
import '../styles/Navbar.css';

function NotificationPanel({ notifications, onClose }) {
  return (
    <div className="notification-panel">
      {notifications.map(notif => (
        <div key={notif.id} className={`notification notification-${notif.type}`}>
          <span>{notif.message}</span>
          <button onClick={() => onClose?.(notif.id)}>×</button>
        </div>
      ))}
    </div>
  );
}

export default NotificationPanel;