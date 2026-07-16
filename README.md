# User Management System

A full-stack web application demonstrating modern software engineering practices.
Built with **FastAPI** (Python backend), **React** (frontend), and **MySQL** (database).

---

## Architecture Overview

```
user-management-system/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/routers/      # HTTP route handlers (auth, users)
│   │   ├── core/             # Config and JWT security utilities
│   │   ├── db/               # SQLAlchemy database connection
│   │   ├── models/           # ORM models (database table definitions)
│   │   ├── schemas/          # Pydantic schemas (request/response validation)
│   │   ├── services/         # Business logic layer
│   │   └── main.py           # FastAPI app entry point
│   ├── requirements.txt
│   └── .env.example
└── frontend/                 # React frontend
    └── src/
        ├── api/              # Axios API client
        ├── components/       # Reusable components (ProtectedRoute)
        ├── pages/            # Page components (Login, Register, Dashboard)
        ├── App.jsx           # Root component with routing
        └── index.js          # React entry point
```

---

## Tech Stack

| Layer    | Technology           | Purpose                              |
|----------|----------------------|--------------------------------------|
| Backend  | FastAPI (Python)     | REST API framework                   |
| Database | MySQL + SQLAlchemy   | Persistent storage + ORM             |
| Auth     | JWT + bcrypt         | Stateless auth + password hashing    |
| Frontend | React 18             | Single-page application              |
| Routing  | React Router v6      | Client-side navigation               |
| HTTP     | Axios                | API calls from frontend to backend   |

---

## Features

- User registration with email/password
- Secure login with JWT token generation
- Password hashing with bcrypt (never stored plain text)
- Protected dashboard route (requires valid JWT)
- Full CRUD: list, view, update, delete users
- Auto-redirect: unauthenticated users sent to login page
- Interactive API docs at `/docs` (Swagger UI)

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm start
```

App runs at: http://localhost:3000

### Database

```sql
CREATE DATABASE user_management_db;
```

SQLAlchemy will auto-create tables on first startup.

---

## API Endpoints

| Method | Endpoint           | Auth Required | Description              |
|--------|--------------------|---------------|--------------------------|
| POST   | /api/auth/register | No            | Register new user        |
| POST   | /api/auth/login    | No            | Login and get JWT token  |
| GET    | /api/users/me      | Yes (JWT)     | Get current user profile |
| GET    | /api/users/        | Yes (JWT)     | List all users           |
| PUT    | /api/users/{id}    | Yes (JWT)     | Update a user            |
| DELETE | /api/users/{id}    | Yes (JWT)     | Delete a user            |

---

## Key Concepts Demonstrated

- **Separation of Concerns**: Routes, services, models, and schemas are separate layers
- **JWT Authentication**: Stateless token-based auth — no sessions stored on server
- **Password Security**: bcrypt hashing with salt — brute-force resistant
- **Pydantic Validation**: All API inputs validated before touching the database
- **ORM**: SQLAlchemy maps Python classes to SQL tables
- **Protected Routes**: Frontend guards private pages using token check
- **CORS**: Backend configured to accept requests from the React dev server

---

## Interview Questions This Project Covers

1. What is REST and how does your API follow REST principles?
2. How does JWT authentication work? What is in the token payload?
3. Why do we hash passwords instead of encrypting them?
4. What is the difference between a Pydantic schema and a SQLAlchemy model?
5. What is CORS and why is it needed?
6. How does React Router protect private routes?
7. What happens if the JWT token expires?
8. What is the purpose of a service layer vs. a router layer?

---

## Author

Abhinav Raj Gupta — Built for software engineering interview preparation.
