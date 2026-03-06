import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Auth.css';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Login failed');
        return;
      }

      login(data.user, data.access_token);

      if (data.user.role === "examiner") {
        navigate("/examiner-dashboard");
      } else {
        navigate("/dashboard");
      }

    } catch (err) {
      setError('Network error. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container-box">
        <div className="auth-header-title">
          <div className="auth-logo-small auth-logo-login">
            <img 
              src={require('../assets/shield-logo.jpg')} 
              alt="Shield Logo" 
              className="shield-logo-small shield-logo-login-img"
            />
          </div>
          <h1>ONLINE PROCTORING</h1>
          <p className="auth-subtitle">Secure Online Examinations</p>
        </div>

        <div className="login-tab">Login</div>

        <div className="auth-logo-center">
          <img 
            src={require('../assets/shield-logo.jpg')} 
            alt="Shield Logo" 
            className="shield-logo-img"
            onError={(e) => {
              console.log('Shield logo failed to load, showing fallback');
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
          <div className="logo-icon" style={{display: 'none'}}>
            <div className="icon-graduation">🎓</div>
          </div>
        </div>

        {error && (
          <div className="error-alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <span className="input-icon">✉</span>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email"
              required
            />
          </div>

          <div className="input-group">
            <span className="input-icon">🔒</span>
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Password"
              required
            />
          </div>

          <div className="checkbox-group">
            <input
              type="checkbox"
              id="showPassword"
              checked={showPassword}
              onChange={(e) => setShowPassword(e.target.checked)}
            />
            <label htmlFor="showPassword">Show Password?</label>
          </div>

          <button type="submit" disabled={loading} className="btn-login-full">
            {loading ? 'Loading...' : 'Login'}
          </button>

          <Link to="/register" className="btn-register">
            Student Registration
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

export default Login;