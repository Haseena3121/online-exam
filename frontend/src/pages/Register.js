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
    <div className="register-page">

      {/* ── LEFT PANEL ── */}
      <div className="register-left">
        <div className="register-left-logo">
          <img src={require('../assets/shield-logo.jpg')} alt="logo" />
          <h1>ONLINE PROCTORING</h1>
          <div className="register-left-tagline">Secure • Smart • Reliable</div>
        </div>

        <div className="register-illustration-placeholder">📋</div>

        <div className="register-left-note">
          🛡️ Your security is our priority. We ensure a fair and cheating-free environment.
        </div>

        <div className="register-left-footer">
          © 2024 TI Online Examination System Pro<br />
          A Product of <a href="#">Trakus Infotek</a>
        </div>
      </div>

      {/* ── RIGHT PANEL ── */}
      <div className="register-right">
        <h2>Create Your Account</h2>
        <p className="register-subtitle">Join us &amp; start your secure exam journey</p>

        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Full Name */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
            </span>
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Full Name" required />
          </div>

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

          {/* Phone */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5 19.79 19.79 0 0 1 1.61 4.9 2 2 0 0 1 3.6 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.73 17.5z"/>
              </svg>
            </span>
            <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone Number" />
          </div>

          {/* Password */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
          </div>

          {/* Confirm Password */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </span>
            <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} placeholder="Confirm Password" required />
          </div>

          {/* Role */}
          <div className="form-group">
            <span className="form-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </span>
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="student">Student</option>
              <option value="examiner">Examiner</option>
            </select>
          </div>

          {/* Terms */}
          <div className="terms-row">
            <input type="checkbox" id="terms" checked={agreed} onChange={e => setAgreed(e.target.checked)} />
            <label htmlFor="terms">
              I agree to the <a href="#">Terms &amp; Conditions</a> and <a href="#">Privacy Policy</a>
            </label>
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Creating Account…' : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
                Create Account
              </>
            )}
          </button>

          <div className="auth-divider">OR</div>

          <button type="button" className="btn-social">
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Register with Google
          </button>
        </form>

        <div className="bottom-text">
          Already have an account? <Link to="/login">Login Here</Link>
        </div>

        <div className="page-footer">
          © 2024 TI Online Examination System Pro<br />
          A Product of <a href="#">Trakus Infotek</a>
        </div>
      </div>
    </div>
  );
}
