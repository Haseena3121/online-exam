/* eslint-disable no-unused-vars, no-console */
import API_BASE from '../config';
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Auth.css';

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPwd, setShowPwd] = useState(false);
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = e => setFormData(p => ({ ...p, [e.target.name]: e.target.value }));

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || 'Login failed'); return; }
      login(data.user, data.access_token);
      navigate(data.user.role === 'examiner' ? '/examiner-dashboard' : '/dashboard');
    } catch { setError('Network error. Please check if the backend is running.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* LEFT PANEL - Branding */}
        <div className="auth-left">
          <div className="auth-brand">
            <div className="auth-logo">
              <div className="logo-shield">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L3 7V12C3 17.55 6.84 22.74 12 24C17.16 22.74 21 17.55 21 12V7L12 2Z" fill="url(#shield-gradient)"/>
                  <circle cx="12" cy="12" r="4" fill="#1a1a2e"/>
                  <circle cx="12" cy="12" r="2" fill="#4f46e5"/>
                  <defs>
                    <linearGradient id="shield-gradient" x1="3" y1="2" x2="21" y2="24">
                      <stop stopColor="#3b82f6"/>
                      <stop offset="1" stopColor="#8b5cf6"/>
                    </linearGradient>
                  </defs>
                </svg>
                <div className="logo-graduation-cap">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="#1e293b">
                    <path d="M12 3L1 9L5 11.18V17.18L12 21L19 17.18V11.18L21 10.09V17H23V9L12 3ZM18.82 9L12 12.72L5.18 9L12 5.28L18.82 9ZM17 15.99L12 18.72L7 15.99V12.27L12 15L17 12.27V15.99Z"/>
                  </svg>
                </div>
              </div>
            </div>
            <h1 className="brand-title">ONLINE<br/><span>PROCTORING</span></h1>
            <p className="brand-tagline">Secure. Smart. Seamless.</p>
            <p className="brand-desc">AI-Powered Exam Monitoring<br/>for a Fair & Trusted Evaluation</p>
          </div>

          <div className="auth-illustration">
            <img src={require('../assets/login_illustration.png')} alt="Proctoring illustration" onError={(e) => e.target.style.display='none'} />
            <div className="illustration-overlay">
              <div className="overlay-item">
                <span className="overlay-icon green">&#10003;</span>
                Live Monitoring
              </div>
              <div className="overlay-item">
                <span className="overlay-icon blue">&#128065;</span>
                AI Proctoring
              </div>
              <div className="overlay-item">
                <span className="overlay-icon purple">&#128274;</span>
                Secure Browser
              </div>
              <div className="overlay-item">
                <span className="overlay-icon orange">&#128276;</span>
                Real-time Alerts
              </div>
            </div>
          </div>

          <div className="auth-features">
            <div className="feature-item">
              <div className="feature-icon blue">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
              </div>
              <div>
                <strong>100% Secure</strong>
                <span>Your data is encrypted and protected</span>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon purple">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                </svg>
              </div>
              <div>
                <strong>Live Monitoring</strong>
                <span>AI-powered live proctoring</span>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon orange">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l4.59-4.59L18 11l-6 6z"/>
                </svg>
              </div>
              <div>
                <strong>Fair & Transparent</strong>
                <span>Ensuring integrity in every exam</span>
              </div>
            </div>
          </div>

          <div className="auth-footer-features">
            <div className="footer-feature">
              <span className="ff-icon green">&#10003;</span>
              <div>
                <strong>End-to-End Encryption</strong>
                <span>256-bit SSL security</span>
              </div>
            </div>
            <div className="footer-feature">
              <span className="ff-icon blue">&#9729;</span>
              <div>
                <strong>Reliable & Scalable</strong>
                <span>99.9% Uptime Guarantee</span>
              </div>
            </div>
            <div className="footer-feature">
              <span className="ff-icon purple">&#128222;</span>
              <div>
                <strong>24/7 Support</strong>
                <span>{"We're here to help you"}</span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL - Login Form */}
        <div className="auth-right">
          <div className="auth-security-badge">
            <div className="security-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" fill="#3b82f6"/>
                <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z" fill="white"/>
              </svg>
            </div>
            <div>
              <span className="security-label">Your Security,</span>
              <span className="security-highlight">Our Priority</span>
            </div>
          </div>

          <div className="auth-form-header">
            <span className="wave-emoji">&#128075;</span>
            <h2>Welcome Back!</h2>
            <p>Login to continue your exam journey</p>
          </div>

          {error && <div className="error-alert">{error}</div>}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </span>
              <input 
                type="email" 
                name="email" 
                value={formData.email} 
                onChange={handleChange} 
                placeholder="Email" 
                required 
              />
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input 
                type={showPwd ? 'text' : 'password'} 
                name="password" 
                value={formData.password} 
                onChange={handleChange} 
                placeholder="Password" 
                required 
              />
              <button 
                type="button" 
                className="toggle-pwd" 
                onClick={() => setShowPwd(!showPwd)}
              >
                {showPwd ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                ) : (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                )}
              </button>
            </div>

            <div className="form-row-between">
              <label className="check-label">
                <input type="checkbox" checked={remember} onChange={e => setRemember(e.target.checked)} />
                <span className="checkmark"></span>
                Show Password
              </label>
              <Link to="#" className="link-primary">Forgot Password?</Link>
            </div>

            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? (
                <span className="btn-loading">Logging in...</span>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="11" width="18" height="11" rx="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  Login
                </>
              )}
            </button>

            <div className="auth-divider"><span>OR</span></div>

            <button type="button" className="btn-secondary">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 4a4 4 0 0 1 4 4 4 4 0 0 1-4 4 4 4 0 0 1-4-4 4 4 0 0 1 4-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z"/>
                <path d="M20 10h2v2h-2v2h-2v-2h-2v-2h2V8h2v2z"/>
              </svg>
              <div className="btn-text">
                <strong>Create New Account</strong>
                <span>Register and start your exam journey</span>
              </div>
            </button>
          </form>

          <div className="auth-bottom-illustration">
            <img src={require('../assets/student_desk.png')} alt="Student" onError={(e) => e.target.style.display='none'} />
            <div className="ai-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#10b981">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
              </svg>
              AI is watching for a fair examination
            </div>
          </div>

          <div className="auth-page-footer">
            &copy; 2024 TI Online Examination System Pro<br/>
            A Product of <a href="#">Trakus Infotek</a>
          </div>
        </div>
      </div>
    </div>
  );
}
