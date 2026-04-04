import API_BASE from '../config';
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/Auth.css';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    role: 'student'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }
    if (!/[A-Z]/.test(formData.password)) {
      setError('Password must contain at least one uppercase letter');
      return false;
    }
    if (!/[0-9]/.test(formData.password)) {
      setError('Password must contain at least one number');
      return false;
    }
    if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(formData.password)) {
      setError('Password must contain at least one special character');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!validateForm()) return;
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          phone: formData.phone,
          role: formData.role
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Registration failed');
        return;
      }

      alert('✓ Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      setError(`Connection error: ${err.message}. Is the backend running on port 5000?`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container-box register-box">
        <div className="auth-header-title">
          <div className="auth-logo-small">
            <img
              src={require('../assets/shield-logo.jpg')}
              alt="Shield Logo"
              className="shield-logo-small"
            />
          </div>
          <h1>CREATE ACCOUNT</h1>
          <p className="auth-subtitle">Join Our Exam Platform</p>
        </div>

        <div className="login-tab">Register</div>

        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form register-form">
          <div className="input-group">
            <span className="input-icon">👤</span>
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Full Name" required />
          </div>

          <div className="input-group">
            <span className="input-icon">✉</span>
            <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email" required />
          </div>

          <div className="input-group">
            <span className="input-icon">📱</span>
            <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone (Optional)" />
          </div>

          <div className="input-group">
            <span className="input-icon">🔒</span>
            <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" required />
          </div>

          <div className="input-group">
            <span className="input-icon">🔒</span>
            <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} placeholder="Confirm Password" required />
          </div>

          <div className="input-group">
            <span className="input-icon">👨‍💼</span>
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="student">Student</option>
              <option value="examiner">Examiner</option>
            </select>
          </div>

          <button type="submit" disabled={loading} className="btn-login-full">
            {loading ? 'Creating Account...' : 'Register'}
          </button>

          <Link to="/login" className="btn-register">
            Already have an account? Login
          </Link>
        </form>

        <div className="auth-footer-text">
          <p>© 2021 Ti Online Examination System Pro</p>
          <p>A Product of Trakus Infotek</p>
        </div>
      </div>
    </div>
  );
}

export default Register;
