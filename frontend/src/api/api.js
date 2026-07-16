// api/api.js
// PURPOSE: Centralized API communication layer.
// All HTTP calls to the FastAPI backend live here.
// React components call these functions - they never make fetch() calls directly.
//
// FIXES APPLIED:
// - BASE_URL corrected from localhost:8000 to localhost:9000 (backend runs on 9000)
// - All auth routes prefixed with /api/auth/ to match backend
// - All users routes prefixed with /api/users to match backend
// - Removed non-existent /auth/profile endpoint
// - Added getMe() which decodes the JWT sub claim instead of hitting a missing profile route
// - Removed PUT/POST usersAPI methods that have no matching backend route

const BASE_URL = 'http://localhost:9000';

// ─── TOKEN MANAGEMENT ───────────────────────────────────────────────────────────
// localStorage stores data persistently in the browser.
// Unlike sessionStorage, it survives page refreshes and tab closes.
// The JWT token is stored here after login and sent with every request.

export const tokenUtils = {
  getToken: () => localStorage.getItem('access_token'),
  setToken: (token) => localStorage.setItem('access_token', token),
  removeToken: () => localStorage.removeItem('access_token'),
  isLoggedIn: () => !!localStorage.getItem('access_token'),

  // Decode the JWT payload (base64) to extract username and user id.
  // The backend encodes { sub: username, id: user_id } inside the token.
  // This avoids needing a /auth/profile endpoint that does not exist.
  decodeToken: () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = token.split('.')[1];
      return JSON.parse(atob(payload));
    } catch {
      return null;
    }
  },
};

// ─── HTTP HELPER ────────────────────────────────────────────────────────────────
// Internal helper that adds auth headers and handles errors.
// All API functions below use this instead of calling fetch() directly.

const apiRequest = async (endpoint, options = {}) => {
  const token = tokenUtils.getToken();

  const config = {
    headers: {
      'Content-Type': 'application/json',
      // If a token exists, add it to every request.
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);

  // Handle 204 No Content (DELETE responses have no body)
  if (response.status === 204) {
    return null;
  }

  const data = await response.json();

  // If the response is not OK (2xx), throw the error detail
  if (!response.ok) {
    throw new Error(data.detail || 'An error occurred');
  }

  return data;
};

// ─── AUTH ENDPOINTS ─────────────────────────────────────────────────────────────
// Routes match backend simple_server.py exactly:
//   POST /api/auth/register  -> expects { username, email, password }
//   POST /api/auth/login     -> expects { username, password }
//   No /auth/profile route exists in the backend.

export const authAPI = {
  // POST /api/auth/register
  // Backend UserCreate model: username (str), email (str), password (str)
  // Returns: { access_token, token_type }
  register: (userData) =>
    apiRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),

  // POST /api/auth/login
  // Backend UserLogin model: username (str), password (str)
  // Returns: { access_token, token_type }
  login: (credentials) =>
    apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),
};

// ─── USERS ENDPOINTS ────────────────────────────────────────────────────────────
// Routes match backend simple_server.py exactly:
//   GET    /api/users            -> returns array of { id, username, email, is_active, created_at }
//   GET    /api/users/{id}       -> returns single user object
//   DELETE /api/users/{id}       -> returns { message: 'User deleted successfully' }
//
// NOTE: Backend has NO POST /api/users, NO PUT /api/users/{id}.
// Those were removed from the API layer to avoid confusion.

export const usersAPI = {
  // GET /api/users
  getAll: () => apiRequest('/api/users'),

  // GET /api/users/{id}
  getById: (id) => apiRequest(`/api/users/${id}`),

  // DELETE /api/users/{id}
  delete: (id) =>
    apiRequest(`/api/users/${id}`, {
      method: 'DELETE',
    }),
};
