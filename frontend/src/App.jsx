import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

// App.jsx is the ROOT component of our React application.
// It defines the URL routing structure using React Router.
//
// Route breakdown:
//   /           -> Redirect to /login (default landing)
//   /login      -> Login page (public)
//   /register   -> Register page (public)
//   /dashboard  -> Dashboard page (PROTECTED - requires JWT)
//
// ProtectedRoute wraps /dashboard so that only authenticated
// users with a valid token can access it.

function App() {
  return (
    <Router>
      <Routes>
        {/* Default route: redirect root URL to /login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Public routes: accessible without authentication */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected route: only accessible if JWT token exists */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
