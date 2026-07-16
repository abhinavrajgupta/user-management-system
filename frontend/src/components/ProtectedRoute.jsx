import { Navigate } from 'react-router-dom';

// ProtectedRoute is a wrapper component that guards private pages.
// If a JWT token exists in localStorage, the user is considered logged in.
// If not, we redirect them to the /login page automatically.
// This prevents unauthenticated users from accessing the dashboard.

const ProtectedRoute = ({ children }) => {
  // Retrieve the token that was stored during login
  // NOTE: authAPI.login() stores under 'access_token' via tokenUtils
  const token = localStorage.getItem('access_token');

  // If no token found, redirect to login page
  // <Navigate> is React Router's way of doing a programmatic redirect
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // If token exists, render the actual child component (e.g., Dashboard)
  return children;
};

export default ProtectedRoute;
