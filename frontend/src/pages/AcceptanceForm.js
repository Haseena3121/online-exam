import API_BASE from '../config';
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/AcceptanceForm.css';

const RULES = [
  {
    icon: '🎥',
    title: 'Camera & Microphone',
    items: [
      'Keep your camera ON throughout the entire exam',
      'Your face must be clearly visible at all times',
      'Microphone must remain enabled for sound detection',
      'No other persons should appear in the camera frame',
      'Ensure adequate lighting in your exam room',
    ],
  },
  {
    icon: '🚫',
    title: 'Prohibited Activities',
    items: [
      'No phones, tablets, or any mobile devices',
      'Do not switch browser tabs or windows',
      'Do not look away from the screen for extended periods',
      'No communication with others during the exam',
      'No external materials, books, or references',
      'No screenshots or recording of the exam',
    ],
  },
  {
    icon: '⚠️',
    title: 'Consequences of Violations',
    items: [
      'Each violation reduces your Trust Score by 5–20%',
      'Trust Score below 50% → exam auto-submitted immediately',
      'Partial marks awarded for answers completed before auto-submit',
      'Examiner receives notifications with video proof',
      'Serious violations may lead to account suspension',
    ],
    warning: true,
  },
  {
    icon: '💻',
    title: 'Technical Requirements',
    items: [
      'Working webcam and microphone',
      'Stable internet connection (min 2 Mbps)',
      'Updated browser: Chrome, Firefox, Safari, or Edge',
      'Use a computer or laptop (mobile not recommended)',
      'Private and quiet examination environment',
    ],
  },
];

const CONFIRMATIONS = [
  { name: 'accepted', label: 'I have read and understood all exam rules' },
  { name: 'rules_accepted', label: 'I will not engage in any form of cheating' },
  { name: 'honor_code_accepted', label: 'I accept the Honor Code and pledge academic integrity' },
  { name: 'privacy_accepted', label: 'I consent to video/audio recording for proctoring' },
  { name: 'technical_requirements_met', label: 'My system meets all technical requirements' },
];

function AcceptanceForm() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();

  const [visibleRules, setVisibleRules] = useState(0);
  const [formData, setFormData] = useState({
    accepted: false,
    rules_accepted: false,
    honor_code_accepted: false,
    privacy_accepted: false,
    technical_requirements_met: false,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const allAccepted = Object.values(formData).every(Boolean);

  // Animate rules appearing one by one
  useEffect(() => {
    if (visibleRules < RULES.length) {
      const timer = setTimeout(() => setVisibleRules(v => v + 1), 600);
      return () => clearTimeout(timer);
    }
  }, [visibleRules]);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: checked }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/exams/${examId}/acceptance-form`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) { setError(data.error || 'Failed to submit'); setLoading(false); return; }

      const startRes = await fetch(`${API_BASE}/api/exams/${examId}/start`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (startRes.ok) {
        const startData = await startRes.json();
        navigate(`/exam/${examId}/${startData.session_id}`);
      } else {
        setError('Failed to start exam. Please try again.');
        setLoading(false);
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="acceptance-page">
      <div className="acceptance-card">
        {/* Step indicator */}
        <div className="acceptance-steps">
          <div className="step done">✓</div>
          <div className="step-line done" />
          <div className="step active">2</div>
          <div className="step-line" />
          <div className="step">3</div>
        </div>

        <div className="acceptance-title">
          <h1>📋 Exam Rules & Acceptance</h1>
          <p>Read each rule carefully before proceeding to your exam</p>
        </div>

        {error && <div className="acceptance-error">{error}</div>}

        {/* Animated rules */}
        <div className="rules-list">
          {RULES.map((rule, idx) => (
            <div
              key={idx}
              className={`rule-card ${rule.warning ? 'rule-warning' : ''} ${idx < visibleRules ? 'rule-visible' : 'rule-hidden'}`}
            >
              <div className="rule-card-header">
                <span className="rule-icon">{rule.icon}</span>
                <h3>{rule.title}</h3>
              </div>
              <ul className="rule-items">
                {rule.items.map((item, i) => (
                  <li key={i} style={{ animationDelay: `${i * 80}ms` }}>{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Confirmations — only show after all rules visible */}
        {visibleRules >= RULES.length && (
          <form onSubmit={handleSubmit} className="confirmations-form">
            <h3 className="confirm-title">✅ Confirm & Accept</h3>
            {CONFIRMATIONS.map((c) => (
              <label key={c.name} className={`confirm-checkbox ${formData[c.name] ? 'checked' : ''}`}>
                <input
                  type="checkbox"
                  name={c.name}
                  checked={formData[c.name]}
                  onChange={handleCheckboxChange}
                />
                <span className="checkmark">{formData[c.name] ? '✓' : ''}</span>
                <span>{c.label}</span>
              </label>
            ))}

            <div className="acceptance-actions">
              <button type="button" onClick={() => navigate('/exam-list')} className="btn-ghost">
                ← Cancel
              </button>
              <button
                type="submit"
                disabled={loading || !allAccepted}
                className={`btn-start ${allAccepted ? 'enabled' : 'disabled'}`}
              >
                {loading ? '⏳ Starting...' : '🚀 Accept & Start Exam'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default AcceptanceForm;
