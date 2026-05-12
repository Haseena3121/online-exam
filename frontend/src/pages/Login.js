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
    <div className="login-page">

      {/* ── LEFT PANEL ── */}
      <div className="login-left">
        <div className="login-left-logo">
          <img src={require('../assets/shield-logo.jpg')} alt="logo" />
          <h1>ONLINE <span>PROCTORING</span></h1>
          <div className="login-left-tagline">Secure • Smart • Reliable</div>
        </div>

        {/* Illustration placeholder — replace with real image if available */}
        <div className="login-illustration-placeholder">🖥️</div>

        <div className="login-left-footer">
          © 2024 TI Online Examination System Pro<br />
          A Product of <a href="#">Trakus Infotek</a>
        </div>
      </div>

      {/* ── RIGHT PANEL ── */}
      <div className="login-right">
        <h2>Welcome Back!</h2>
        <p className="login-subtitle">Login to continue your exam journey</p>

        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Email */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
            </span>
            <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email Address" required />
          </div>

          {/* Password */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <input type={showPwd ? 'text' : 'password'} name="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
          </div>

          {/* Remember / Forgot */}
          <div className="form-row-between">
            <label className="check-label">
              <input type="checkbox" checked={remember} onChange={e => setRemember(e.target.checked)} />
              Remember Me
            </label>
            <a href="#" className="link-blue">Forgot Password?</a>
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Logging in…' : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
                Login
              </>
            )}
          </button>

          <div className="auth-divider">OR</div>

          {/* Google */}
          <button type="button" className="btn-social">
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>

          {/* Microsoft */}
          <button type="button" className="btn-social">
            <svg width="18" height="18" viewBox="0 0 21 21">
              <rect x="1" y="1" width="9" height="9" fill="#f25022"/>
              <rect x="11" y="1" width="9" height="9" fill="#7fba00"/>
              <rect x="1" y="11" width="9" height="9" fill="#00a4ef"/>
              <rect x="11" y="11" width="9" height="9" fill="#ffb900"/>
            </svg>
            Continue with Microsoft
          </button>
        </form>

        <div className="bottom-text">
          Don't have an account? <Link to="/register">Register Now</Link>
        </div>

        <div className="page-footer">
          © 2024 TI Online Examination System Pro<br />
          A Product of <a href="#">Trakus Infotek</a>
        </div>
      </div>
    </div>
  );
}
