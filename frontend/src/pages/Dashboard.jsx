// Dashboard.jsx
// PURPOSE: Main dashboard after login. Shows logged-in user info + full users table.
// PROTECTED: ProtectedRoute component redirects to /login if no token exists.
//
// FIXES APPLIED:
// 1. Removed authAPI.getProfile() call - that endpoint does NOT exist in the backend.
// 2. Used tokenUtils.decodeToken() to read username + id from the JWT payload directly.
// 3. Fetched the current user's full record from GET /api/users/{id} using the decoded id.
// 4. Replaced user.full_name with user.username (backend User model has no full_name field).
// 5. Removed user.is_admin reference (backend User model has no is_admin field).
// 6. Added full users table using usersAPI.getAll() with working delete.
// 7. Imported usersAPI from api.js.

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usersAPI, tokenUtils } from '../api/api';

function Dashboard() {
  // currentUser: the logged-in user's own record fetched from GET /api/users/{id}
  const [currentUser, setCurrentUser] = useState(null);
  // users: full list from GET /api/users for the users table
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteMsg, setDeleteMsg] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // If no token exists, redirect to login immediately
    if (!tokenUtils.isLoggedIn()) {
      navigate('/login');
      return;
    }

    // Decode the JWT to get { sub: username, id: user_id }
    // The backend encodes these two claims when creating the token.
    const decoded = tokenUtils.decodeToken();
    if (!decoded || !decoded.id) {
      tokenUtils.removeToken();
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      try {
        // Fetch the current user's own record from GET /api/users/{id}
        const userRecord = await usersAPI.getById(decoded.id);
        setCurrentUser(userRecord);

        // Fetch all users for the table
        const allUsers = await usersAPI.getAll();
        setUsers(allUsers);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    tokenUtils.removeToken();
    navigate('/login');
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await usersAPI.delete(userId);
      setDeleteMsg(`User #${userId} deleted successfully.`);
      // Refresh users list after delete
      const updated = await usersAPI.getAll();
      setUsers(updated);
      // If the deleted user was the logged-in user, log out
      if (currentUser && userId === currentUser.id) {
        tokenUtils.removeToken();
        navigate('/login');
      }
    } catch (err) {
      setDeleteMsg(`Error: ${err.message}`);
    }
  };

  if (loading) return <div style={styles.loading}>Loading your dashboard...</div>;
  if (error) return <div style={styles.error}>{error}</div>;

  return (
    <div style={styles.container}>
      {/* Navigation Bar */}
      <nav style={styles.nav}>
        <h2 style={styles.navBrand}>User Management System</h2>
        <div style={styles.navLinks}>
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </nav>

      {/* Main Content */}
      <div style={styles.content}>
        <h1 style={styles.title}>Welcome, {currentUser?.username}!</h1>

        {/* Profile Card */}
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Your Profile</h2>
          <div style={styles.profileGrid}>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Username</span>
              <span style={styles.profileValue}>{currentUser?.username}</span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Email</span>
              <span style={styles.profileValue}>{currentUser?.email}</span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Account Status</span>
              <span style={styles.profileValue}>
                {currentUser?.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>Member Since</span>
              <span style={styles.profileValue}>
                {currentUser?.created_at
                  ? new Date(currentUser.created_at).toLocaleDateString()
                  : 'N/A'}
              </span>
            </div>
            <div style={styles.profileItem}>
              <span style={styles.profileLabel}>User ID</span>
              <span style={styles.profileValue}>#{currentUser?.id}</span>
            </div>
          </div>
        </div>

        {/* All Users Table */}
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>All Users ({users.length})</h2>
          {deleteMsg && (
            <div style={deleteMsg.startsWith('Error') ? styles.errorMsg : styles.successMsg}>
              {deleteMsg}
            </div>
          )}
          <table style={styles.table}>
            <thead>
              <tr style={styles.tableHeaderRow}>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Username</th>
                <th style={styles.th}>Email</th>
                <th style={styles.th}>Status</th>
                <th style={styles.th}>Created At</th>
                <th style={styles.th}>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} style={styles.tableRow}>
                  <td style={styles.td}>#{u.id}</td>
                  <td style={styles.td}>{u.username}</td>
                  <td style={styles.td}>{u.email}</td>
                  <td style={styles.td}>
                    <span style={u.is_active ? styles.badgeActive : styles.badgeInactive}>
                      {u.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td style={styles.td}>
                    {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}
                  </td>
                  <td style={styles.td}>
                    <button
                      onClick={() => handleDelete(u.id)}
                      style={styles.deleteBtn}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {users.length === 0 && (
            <p style={styles.emptyMsg}>No users found.</p>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', backgroundColor: '#f0f2f5' },
  nav: {
    backgroundColor: '#1a1a2e',
    color: 'white',
    padding: '1rem 2rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  navBrand: { margin: 0, fontSize: '1.2rem', color: 'white' },
  navLinks: { display: 'flex', alignItems: 'center', gap: '1rem' },
  logoutBtn: {
    backgroundColor: '#dc2626',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  content: { maxWidth: '1000px', margin: '2rem auto', padding: '0 1rem' },
  title: { color: '#1a1a2e', marginBottom: '1.5rem' },
  card: {
    backgroundColor: 'white',
    padding: '1.5rem',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    marginBottom: '1.5rem',
  },
  cardTitle: { color: '#1a1a2e', marginTop: 0, marginBottom: '1rem' },
  profileGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '1rem',
  },
  profileItem: { display: 'flex', flexDirection: 'column', gap: '0.25rem' },
  profileLabel: { fontSize: '0.8rem', color: '#666', textTransform: 'uppercase' },
  profileValue: { fontSize: '1rem', color: '#333', fontWeight: '500' },
  table: { width: '100%', borderCollapse: 'collapse' },
  tableHeaderRow: { backgroundColor: '#f8f9fa' },
  tableRow: { borderBottom: '1px solid #e5e7eb' },
  th: {
    textAlign: 'left',
    padding: '0.75rem',
    fontSize: '0.85rem',
    color: '#374151',
    fontWeight: '600',
    borderBottom: '2px solid #e5e7eb',
  },
  td: { padding: '0.75rem', fontSize: '0.9rem', color: '#374151' },
  badgeActive: {
    backgroundColor: '#dcfce7',
    color: '#16a34a',
    padding: '0.2rem 0.5rem',
    borderRadius: '9999px',
    fontSize: '0.75rem',
  },
  badgeInactive: {
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    padding: '0.2rem 0.5rem',
    borderRadius: '9999px',
    fontSize: '0.75rem',
  },
  deleteBtn: {
    backgroundColor: '#dc2626',
    color: 'white',
    border: 'none',
    padding: '0.3rem 0.75rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  errorMsg: {
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    padding: '0.75rem',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  successMsg: {
    backgroundColor: '#dcfce7',
    color: '#16a34a',
    padding: '0.75rem',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  emptyMsg: { color: '#666', textAlign: 'center', padding: '1rem' },
  loading: { textAlign: 'center', padding: '2rem', color: '#666' },
  error: { textAlign: 'center', padding: '2rem', color: '#dc2626' },
};

export default Dashboard;
