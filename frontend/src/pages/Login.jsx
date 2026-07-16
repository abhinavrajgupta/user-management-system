// Login.jsx
// PURPOSE: Login page component.
// HOW IT WORKS:
// 1. User fills email + password form
// 2. On submit, calls authAPI.login()
// 3. On success, stores JWT in localStorage, redirects to dashboard
// 4. On error, displays error message
//
// REACT CONCEPTS USED:
// useState: manages form data and loading/error state
// useNavigate: programmatic navigation (redirect after login)
// Controlled inputs: form state lives in React, not the DOM

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, tokenUtils } from '../api/api';

function Login() {
  // useState creates reactive state variables.
  // When state changes, React re-renders the component automatically.
  // formData holds the current form field values.
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  // loading: true while API call is in progress (disables button, shows spinner)
  const [loading, setLoading] = useState(false);

  // error: stores error message from failed login attempt
  const [error, setError] = useState('');

  // useNavigate gives us a function to redirect programmatically
  const navigate = useNavigate();

  // handleChange updates formData whenever the user types in a field.
  // e.target.name identifies which field changed (email or password).
  // e.target.value is the new value.
  // Spread operator (...formData) copies all existing fields, then overrides the changed one.
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // handleSubmit is called when the form is submitted.
  // e.preventDefault() stops the default browser behavior of reloading the page.
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Call the login API endpoint
      const response = await authAPI.login(formData);

      // Store the JWT token in localStorage
      // After this, every API request will include the Authorization header
      tokenUtils.setToken(response.access_token);

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      // Show the error message from the API (e.g., "Incorrect email or password")
      setError(err.message);
    } finally {
      // Always stop loading, whether success or error
      setLoading(false);
    }
  };

  // JSX: HTML-like syntax that React compiles to JavaScript.
  // className instead of class (class is a reserved JS keyword).
  // onChange={handleChange} is an event listener - called on every keystroke.
  // value={formData.email} makes it a controlled input - React controls the value.
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Welcome Back</h1>
        <p style={styles.subtitle}>Sign in to your account</p>

        {/* Conditional rendering: only show error div if error is not empty */}
        {error && (
          <div style={styles.error}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Email Address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
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

          <button
            type="submit"
            disabled={loading}
            style={{ ...styles.button, opacity: loading ? 0.7 : 1 }}
          >
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

// Inline styles object - keeps styles co-located with the component.
// In production you'd use CSS modules, Tailwind, or styled-components.
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
