// Login.jsx
// PURPOSE: Login page component.
// HOW IT WORKS:
// 1. User fills username + password form
// 2. On submit, calls authAPI.login()
// 3. On success, stores JWT in localStorage, redirects to dashboard
// 4. On error, displays error message
//
// FIX: Backend UserLogin model expects { username, password } NOT { email, password }.
// Changed email field to username to match simple_server.py exactly.

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, tokenUtils } from '../api/api';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Call the login API endpoint
      // Sends { username, password } to POST /api/auth/login
      const response = await authAPI.login(formData);

      // Store the JWT token in localStorage
      tokenUtils.setToken(response.access_token);

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      // Backend returns 401 with detail: 'Invalid credentials'
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Welcome Back</h1>
        <p style={styles.subtitle}>Sign in to your account</p>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Your username"
              required
              style={styles.input}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Your password"
              required
              style={styles.input}
            />
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={styles.link}>
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f0f2f5',
  },
  card: {
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '400px',
  },
  title: { textAlign: 'center', color: '#1a1a2e', marginBottom: '0.5rem' },
  subtitle: { textAlign: 'center', color: '#666', marginBottom: '1.5rem' },
  error: {
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    padding: '0.75rem',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  field: { marginBottom: '1rem' },
  label: { display: 'block', marginBottom: '0.5rem', color: '#333', fontWeight: '500' },
  input: {
    width: '100%',
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    boxSizing: 'border-box',
  },
  button: {
    width: '100%',
    padding: '0.75rem',
    backgroundColor: '#4f46e5',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    cursor: 'pointer',
    marginTop: '0.5rem',
  },
  link: { textAlign: 'center', marginTop: '1rem', color: '#666' },
};

export default Login;
