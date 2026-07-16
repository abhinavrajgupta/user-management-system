// api/api.js
// PURPOSE: Centralized API communication layer.
// All HTTP calls to the FastAPI backend live here.
// React components call these functions - they never make fetch() calls directly.
//
// WHY CENTRALIZE API CALLS?
// - If the base URL changes, you change it in ONE place
// - Easy to add global headers (Authorization token) in one place
// - Consistent error handling
// - Easy to mock during testing

const BASE_URL = 'http://localhost:8000';

// ─── TOKEN MANAGEMENT ─────────────────────────────────────────────────────────
// localStorage stores data persistently in the browser.
// Unlike sessionStorage, it survives page refreshes and tab closes.
// The JWT token is stored here after login and sent with every request.
//
// WHY localStorage?
// Simple and works for demo/interview projects.
// In production apps, httpOnly cookies are more secure (prevent XSS).
// This is a common interview discussion point.

export const tokenUtils = {
  getToken: () => localStorage.getItem('access_token'),
  setToken: (token) => localStorage.setItem('access_token', token),
  removeToken: () => localStorage.removeItem('access_token'),
  isLoggedIn: () => !!localStorage.getItem('access_token'),
};

// ─── HTTP HELPER ─────────────────────────────────────────────────────────────────
// Internal helper that adds auth headers and handles errors.
// All API functions below use this instead of calling fetch() directly.

const apiRequest = async (endpoint, options = {}) => {
  const token = tokenUtils.getToken();

  const config = {
    headers: {
      'Content-Type': 'application/json',
      // If a token exists, add it to every request.
      // This is the Bearer token pattern - required by our protected endpoints.
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

// ─── AUTH ENDPOINTS ───────────────────────────────────────────────────────────────

export const authAPI = {
  // POST /auth/register
  register: (userData) => apiRequest('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  // POST /auth/login - returns { access_token, token_type }
  login: (credentials) => apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),

  // GET /auth/profile - returns current user (protected)
  getProfile: () => apiRequest('/auth/profile'),
};

// ─── USERS ENDPOINTS ──────────────────────────────────────────────────────────────

export const usersAPI = {
  // GET /users - returns array of users
  getAll: (skip = 0, limit = 10) =>
    apiRequest(`/users/?skip=${skip}&limit=${limit}`),

  // GET /users/{id}
  getById: (id) => apiRequest(`/users/${id}`),

  // POST /users
  create: (userData) => apiRequest('/users/', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  // PUT /users/{id}
  update: (id, userData) => apiRequest(`/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  }),

  // DELETE /users/{id}
  delete: (id) => apiRequest(`/users/${id}`, {
    method: 'DELETE',
  }),
};
