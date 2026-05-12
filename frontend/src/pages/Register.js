/* eslint-disable no-unused-vars, no-console */
import API_BASE from '../config';
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/Auth.css';
import Toast from '../components/Toast';

export default function Register() {
  const [formData, setFormData] = useState({
    name: '', email: '', phone: '', password: '', confirmPassword: '', role: 'student'
  });
  const [showPwd, setShowPwd] = useState(false);
  const [showConfirmPwd, setShowConfirmPwd] = useState(false);
  const [agreed, setAgreed] = useState(false);
  const [error, setError] = useState('');
  const [toast, setToast] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => setFormData(p => ({ ...p, [e.target.name]: e.target.value }));

  const validate = () => {
    if (formData.password !== formData.confirmPassword) { setError('Passwords do not match'); return false; }
    if (formData.password.length < 8) { setError('Password must be at least 8 characters'); return false; }
    if (!/[A-Z]/.test(formData.password)) { setError('Password needs an uppercase letter'); return false; }
    if (!/[0-9]/.test(formData.password)) { setError('Password needs a number'); return false; }
    if (!agreed) { setError('Please agree to the Terms & Conditions'); return false; }
    return true;
  };

  const handleSubmit = async e => {
    e.preventDefault(); setError('');
    if (!validate()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: formData.name, email: formData.email, password: formData.password, phone: formData.phone, role: formData.role })
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || 'Registration failed'); return; }
      setToast({ message: 'Account created! Please login.', type: 'success' });
      setTimeout(() => navigate('/login'), 1500);
    } catch { setError('Connection error. Is the backend running?'); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-container register-container">
        {/* LEFT PANEL - Branding */}
        <div className="auth-left register-left-panel">
          <div className="auth-brand">
            <div className="auth-logo">
              <div className="logo-shield">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L3 7V12C3 17.55 6.84 22.74 12 24C17.16 22.74 21 17.55 21 12V7L12 2Z" fill="url(#shield-gradient-reg)"/>
                  <circle cx="12" cy="12" r="4" fill="#1a1a2e"/>
                  <circle cx="12" cy="12" r="2" fill="#4f46e5"/>
                  <defs>
                    <linearGradient id="shield-gradient-reg" x1="3" y1="2" x2="21" y2="24">
                      <stop stopColor="#3b82f6"/>
                      <stop offset="1" stopColor="#8b5cf6"/>
                    </linearGradient>
                  </defs>
                </svg>
                <div className="logo-graduation-cap">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M12 3L1 9L5 11.18V17.18L12 21L19 17.18V11.18L21 10.09V17H23V9L12 3ZM18.82 9L12 12.72L5.18 9L12 5.28L18.82 9ZM17 15.99L12 18.72L7 15.99V12.27L12 15L17 12.27V15.99Z"/>
                  </svg>
                </div>
              </div>
            </div>
            <h1 className="brand-title light">Create Your Account</h1>
            <p className="brand-tagline light">Join us & start your secure exam journey</p>
          </div>

          <div className="register-illustration">
            <div className="register-icons">
              <div className="reg-icon-item">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="#10b981">
                  <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
                </svg>
              </div>
              <div className="reg-icon-item">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="#f59e0b">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                </svg>
              </div>
              <div className="reg-icon-item lock">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="#1e293b">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </div>
            </div>
          </div>

          <div className="register-security-note">
            <div className="security-shield">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" fill="#3b82f6"/>
                <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z" fill="white"/>
              </svg>
            </div>
            <div>
              <strong>Your security is our priority</strong>
              <span>We ensure a fair and cheating-free environment.</span>
            </div>
          </div>

          <div className="auth-page-footer light">
            &copy; 2024 TI Online Examination System Pro<br/>
            A Product of <a href="#">Trakus Infotek</a>
          </div>
        </div>

        {/* RIGHT PANEL - Register Form */}
        <div className="auth-right">
          <div className="auth-form-header">
            <h2>Create Your Account</h2>
            <p>Join our exam platform and get started</p>
          </div>

          {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
          {error && <div className="error-alert">{error}</div>}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </span>
              <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Full Name" required />
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </span>
              <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email Address" required />
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5 19.79 19.79 0 0 1 1.61 4.9 2 2 0 0 1 3.6 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.73 17.5z"/>
                </svg>
              </span>
              <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone (Optional)" />
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input type={showPwd ? 'text' : 'password'} name="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
              <button type="button" className="toggle-pwd" onClick={() => setShowPwd(!showPwd)}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  {showPwd ? (
                    <>
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </>
                  ) : (
                    <>
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </>
                  )}
                </svg>
              </button>
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input type={showConfirmPwd ? 'text' : 'password'} name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} placeholder="Confirm Password" required />
              <button type="button" className="toggle-pwd" onClick={() => setShowConfirmPwd(!showConfirmPwd)}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  {showConfirmPwd ? (
                    <>
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </>
                  ) : (
                    <>
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </>
                  )}
                </svg>
              </button>
            </div>

            <div className="form-group">
              <span className="form-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </span>
              <select name="role" value={formData.role} onChange={handleChange}>
                <option value="student">Student</option>
                <option value="examiner">Examiner</option>
              </select>
              <span className="select-arrow">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </span>
            </div>

            <div className="terms-row">
              <input type="checkbox" id="terms" checked={agreed} onChange={e => setAgreed(e.target.checked)} />
              <label htmlFor="terms">
                I agree to the <a href="#">Terms & Conditions</a> and <a href="#">Privacy Policy</a>
              </label>
            </div>

            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? (
                <span className="btn-loading">Creating Account...</span>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Register
                  <span className="btn-arrow">&rarr;</span>
                </>
              )}
            </button>
          </form>

          <div className="bottom-text">
            Already have an account? <Link to="/login">Login</Link>
          </div>

          <div className="auth-trust-badges">
            <div className="trust-badge">
              <span className="badge-icon green">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
              </span>
              <div>
                <strong>Encrypted & Secure</strong>
                <span>Your data is 100% safe</span>
              </div>
            </div>
            <div className="trust-badge">
              <span className="badge-icon blue">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </span>
              <div>
                <strong>24/7 Support</strong>
                <span>We are here to help</span>
              </div>
            </div>
            <div className="trust-badge">
              <span className="badge-icon purple">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l4.59-4.59L18 11l-6 6z"/>
                </svg>
              </span>
              <div>
                <strong>Trusted Platform</strong>
                <span>Used by 1000+ institutions</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
