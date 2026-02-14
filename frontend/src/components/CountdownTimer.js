import React, { useEffect, useState } from 'react';
import '../styles/ExamScreen.css';

function CountdownTimer({ timeLeft, totalTime }) {
  const [displayTime, setDisplayTime] = useState('00:00:00');
  const [urgency, setUrgency] = useState('normal');

  useEffect(() => {
    const hours = Math.floor(timeLeft / 3600);
    const minutes = Math.floor((timeLeft % 3600) / 60);
    const seconds = timeLeft % 60;

    setDisplayTime(
      `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
    );

    const percentageLeft = (timeLeft / totalTime) * 100;
    if (percentageLeft <= 10) {
      setUrgency('critical');
    } else if (percentageLeft <= 25) {
      setUrgency('warning');
    } else {
      setUrgency('normal');
    }
  }, [timeLeft, totalTime]);

  return (
    <div className={`countdown-timer ${urgency}`}>
      <span className="timer-icon">⏱️</span>
      <span className="timer-text">{displayTime}</span>
    </div>
  );
}

export default CountdownTimer;