import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Auth.css';

function AcceptanceForm() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();
  
  const [formData, setFormData] = useState({
    accepted: false,
    rules_accepted: false,
    honor_code_accepted: false,
    privacy_accepted: false,
    technical_requirements_met: false
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: checked
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:5000/api/exams/${examId}/acceptance-form`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Failed to submit acceptance form');
        setLoading(false);
        return;
      }

      // Start exam
      const startResponse = await fetch(`http://localhost:5000/api/exams/${examId}/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (startResponse.ok) {
        const startData = await startResponse.json();
        navigate(`/exam/${examId}/${startData.session_id}`);
      } else {
        setError('Failed to start exam');
        setLoading(false);
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setLoading(false);
      console.error(err);
    }
  };

  return (
    <div className="acceptance-container">
      <div className="acceptance-form">
        <div className="form-header">
          <h1>⚖️ Exam Rules & Acceptance</h1>
          <p>Please read and accept all terms before proceeding</p>
        </div>
        
        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="rules-section">
            <h3>📋 Exam Rules & Guidelines</h3>
            
            <div className="rule">
              <h4>🎥 Proctoring Requirements</h4>
              <ul>
                <li>You must enable your camera throughout the entire exam</li>
                <li>Your face must be clearly visible at all times</li>
                <li>Keep your microphone enabled for sound detection</li>
                <li>Maintain a neutral background or use blur feature</li>
                <li>No other persons should be visible in the camera frame</li>
                <li>Adequate lighting in your exam room is required</li>
              </ul>
            </div>

            <div className="rule">
              <h4>❌ Prohibited Activities</h4>
              <ul>
                <li>Using phone, tablet, or any mobile devices</li>
                <li>Switching to other browser tabs or windows</li>
                <li>Looking away from the screen for extended periods</li>
                <li>Communicating with others during the exam</li>
                <li>Using external materials, books, or references</li>
                <li>Taking screenshots or recording the exam</li>
                <li>Suspicious head movements or behavior</li>
                <li>Attempting to disable camera, microphone, or blur</li>
              </ul>
            </div>

            <div className="rule warning">
              <h4>⚠️ Consequences of Rule Violation</h4>
              <ul>
                <li>Each violation reduces your Trust Score by 5-20%</li>
                <li>If Trust Score falls below 50%, your exam will be <strong>automatically submitted</strong></li>
                <li>Multiple violations may result in exam cancellation</li>
                <li>Serious violations may lead to account suspension</li>
                <li>Examiner receives notifications with video proof of violations</li>
              </ul>
            </div>

            <div className="rule">
              <h4>✅ Technical Requirements</h4>
              <ul>
                <li>Working webcam and microphone</li>
                <li>Stable internet connection (minimum 2 Mbps recommended)</li>
                <li>Updated browser (Chrome, Firefox, Safari, Edge)</li>
                <li>Computer/Laptop (mobile not recommended)</li>
                <li>Private and quiet examination environment</li>
              </ul>
            </div>
          </div>

          <div className="checkboxes-section">
            <h3>📝 Confirmations Required</h3>

            <label className="checkbox-label">
              <input
                type="checkbox"
                name="accepted"
                checked={formData.accepted}
                onChange={handleCheckboxChange}
                required
              />
              <span>I have read and understood all exam rules</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                name="rules_accepted"
                checked={formData.rules_accepted}
                onChange={handleCheckboxChange}
                required
              />
              <span>I promise to follow all the rules and will not engage in any form of cheating</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                name="honor_code_accepted"
                checked={formData.honor_code_accepted}
                onChange={handleCheckboxChange}
                required
              />
              <span>I accept the Honor Code and pledge complete academic integrity</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                name="privacy_accepted"
                checked={formData.privacy_accepted}
                onChange={handleCheckboxChange}
                required
              />
              <span>I consent to video and audio recording for proctoring verification</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                name="technical_requirements_met"
                checked={formData.technical_requirements_met}
                onChange={handleCheckboxChange}
                required
              />
              <span>I confirm my system meets all technical requirements</span>
            </label>
          </div>

          <button 
            type="submit" 
            disabled={loading || !Object.values(formData).every(v => v)} 
            className="btn btn-primary btn-large btn-block"
          >
            {loading ? '⏳ Starting Exam...' : '✓ Accept & Start Exam'}
          </button>

          <button 
            type="button"
            onClick={() => navigate('/exams')}
            className="btn btn-secondary btn-block"
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
}

export default AcceptanceForm;