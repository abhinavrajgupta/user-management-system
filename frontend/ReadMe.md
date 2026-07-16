Browser opens → index.html loads → index.js mounts <App />
       ↓
App.jsx Router kicks in
       ↓
User visits / → redirected to /login
       ↓
Login.jsx → user enters credentials
       → authAPI.login() → POST /api/auth/login (FastAPI @ port 9000)
       → JWT returned → stored in localStorage
       → navigate('/dashboard')
       ↓
ProtectedRoute checks localStorage for token → found → renders Dashboard
       ↓
Dashboard.jsx:
  - decodes JWT to get user ID
  - fetches own profile via GET /api/users/:id
  - fetches all users via GET /api/users
  - displays user table with Delete buttons
  - Logout clears token → back to /login
