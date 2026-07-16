// Register.jsx
// PURPOSE: User registration page.
// Very similar to Login but with more fields and calls /auth/register.
// After successful registration, redirects to login page.

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../api/api';

function Register() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await authAPI.register(formData);
      // Show success message
      setSuccess('Account created! Redirecting to login...');
      // Redirect to login after 2 seconds
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Create Account</h1>
        <p style={styles.subtitle}>Join the User Management System</p>

        {error && <div style={styles.error}>{error}</div>}
        {success && <div style={styles.success}>{success}</div>}

        <form onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Full Name</label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="Jane Doe"
              required
              minLength={2}
              style={styles.input}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Email Address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="jane@example.com"
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
              placeholder="Minimum 8 characters"
              required
              minLength={8}
              style={styles.input}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{ ...styles.button, opacity: loading ? 0.7 : 1 }}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p style={styles.link}>
          Already have an account? <Link to="/login">Sign in</Link>
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
    backgroundColor: '#fee2e2', color: '#dc2626',
    padding: '0.75rem', borderRadius: '4px', marginBottom: '1rem',
  },
  success: {
    backgroundColor: '#dcfce7', color: '#16a34a',
    padding: '0.75rem', borderRadius: '4px', marginBottom: '1rem',
  },
  field: { marginBottom: '1rem' },
  label: { display: 'block', marginBottom: '0.5rem', color: '#333', fontWeight: '500' },
  input: {
    width: '100%', padding: '0.75rem', border: '1px solid #ddd',
    borderRadius: '4px', fontSize: '1rem', boxSizing: 'border-box',
  },
  button: {
    width: '100%', padding: '0.75rem', backgroundColor: '#059669',
    color: 'white', border: 'none', borderRadius: '4px',
    fontSize: '1rem', cursor: 'pointer', marginTop: '0.5rem',
  },
  link: { textAlign: 'center', marginTop: '1rem', color: '#666' },
};

export default Register;
