import React from 'react';
import '../styles/Global.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner">
        <div className="spinner-circle"></div>
      </div>
      <p>Loading...</p>
    </div>
  );
}

export default LoadingSpinner;