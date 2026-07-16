// Dashboard.jsx
// PURPOSE: Main dashboard after login. Shows profile + stats.
// PROTECTED: If not logged in, redirects to /login.
//
// useEffect: runs side effects (like API calls) after component renders.
// This is how React fetches data when a page loads.

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, tokenUtils } from '../api/api';

function Dashboard() {
  // user: holds the logged-in user's profile data from the API
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // useEffect runs after the component first renders.
  // The [] dependency array means: run this effect ONCE (on mount).
  // This is where we fetch the current user's profile from the API.
  useEffect(() => {
    // If no token exists, redirect to login immediately
    if (!tokenUtils.isLoggedIn()) {
      navigate('/login');
      return;
    }

    // Fetch profile from protected endpoint
    const fetchProfile = async () => {
      try {
        const profile = await authAPI.getProfile();
        setUser(profile);
      } catch (err) {
        // If token is expired/invalid, the API returns 401
        // We clear the token and send them to login
        if (err.message.includes('validate credentials')) {
          tokenUtils.removeToken();
          navigate('/login');
        } else {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []); // [] = run once on mount

  const handleLogout = () => {
    // Logout = just remove the token
    // There's no server-side logout call because JWT is stateless.
    // The token expires on its own after ACCESS_TOKEN_EXPIRE_MINUTES.
    // INTERVIEW NOTE: "In production, we'd maintain a token blacklist
    // in Redis for immediate revocation."
    tokenUtils.removeToken();
    navigate('/login');
  };

  if (loading) return <div style={styles.loading}>Loading your dashboard...</div>;
  if (error) return <div style={styles.error}>{error}</div>;

  return (
    <div style={styles.container}>
      {/* Navigation Bar */}
      <nav style={styles.nav}>
        <h2 style={styles.navBrand}>User Management System</h2>
        <div style={styles.navLinks}>
          <Link to="/dashboard" style={styles.navLink}>Dashboard</Link>
          <Link to="/users" style={styles.navLink}>Users</Link>
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </nav>

      {/* Main Content */}
      <div style={styles.content}>
        <h1 style={styles.title}>Welcome, {user?.full_name}!</h1>

        {/* Profile Card */}
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Your Profile</h2>
          <div style={styles.profileGrid}>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Full Name</span>
              <span style={styles.profileValue}>{user?.full_name}</span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Email</span>
              <span style={styles.profileValue}>{user?.email}</span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Account Status</span>
              <span style={{ ...styles.profileValue, color: user?.is_active ? '#16a34a' : '#dc2626' }}>
                {user?.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Role</span>
              <span style={styles.profileValue}>{user?.is_admin ? 'Administrator' : 'User'}</span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Member Since</span>
              <span style={styles.profileValue}>
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>User ID</span>
              <span style={styles.profileValue}>#{user?.id}</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Quick Actions</h2>
          <div style={styles.actions}>
            <Link to="/users" style={styles.actionBtn}>View All Users</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', backgroundColor: '#f0f2f5' },
  nav: {
    backgroundColor: '#1a1a2e', color: 'white',
    padding: '1rem 2rem', display: 'flex',
    justifyContent: 'space-between', alignItems: 'center',
  },
  navBrand: { margin: 0, fontSize: '1.2rem' },
  navLinks: { display: 'flex', alignItems: 'center', gap: '1rem' },
  navLink: { color: 'white', textDecoration: 'none' },
  logoutBtn: {
    backgroundColor: '#dc2626', color: 'white', border: 'none',
    padding: '0.5rem 1rem', borderRadius: '4px', cursor: 'pointer',
  },
  content: { maxWidth: '900px', margin: '2rem auto', padding: '0 1rem' },
  title: { color: '#1a1a2e', marginBottom: '1.5rem' },
  card: {
    backgroundColor: 'white', padding: '1.5rem',
    borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: '1.5rem',
  },
  cardTitle: { color: '#1a1a2e', marginTop: 0, marginBottom: '1rem' },
  profileGrid: {
    display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem',
  },
  profileItem: { display: 'flex', flexDirection: 'column', gap: '0.25rem' },
  profileLabel: { fontSize: '0.8rem', color: '#666', textTransform: 'uppercase' },
  profileValue: { fontSize: '1rem', color: '#333', fontWeight: '500' },
  actions: { display: 'flex', gap: '1rem' },
  actionBtn: {
    backgroundColor: '#4f46e5', color: 'white', padding: '0.75rem 1.5rem',
    borderRadius: '4px', textDecoration: 'none', fontWeight: '500',
  },
  loading: { textAlign: 'center', padding: '2rem', color: '#666' },
  error: { textAlign: 'center', padding: '2rem', color: '#dc2626' },
};

export default Dashboard;
