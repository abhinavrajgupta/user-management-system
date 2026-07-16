# User Management System

> Full-stack user management application built with FastAPI, React, SQLAlchemy, and JWT Authentication.

## Project Overview

This project demonstrates a complete full-stack application with:

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** React + React Router
- **Authentication:** JWT + bcrypt password hashing
- **Database:** SQLite (can be switched to PostgreSQL)

## User Flow

1. User creates an account through the registration page.
2. Backend validates user information.
3. Password is securely hashed and stored.
4. User logs in and receives a JWT token.
5. Frontend stores the token for authentication.
6. Dashboard displays user information and user records.

---

# Architecture

```
React Frontend
       |
       | HTTP Requests
       |
FastAPI Backend
       |
       |
SQLAlchemy ORM
       |
       |
SQLite Database
```

---

# Backend

## Technology Choices

### FastAPI

Chosen because it provides:

- Automatic API documentation
- Built-in request validation
- Type-based data handling

### SQLAlchemy ORM

Chosen because it allows database operations using Python objects instead of writing raw SQL queries.

### JWT Authentication

Chosen because it provides stateless authentication between frontend and backend.

### bcrypt

Chosen because passwords should never be stored as plain text.

### Environment Variables

Chosen because configuration values and secrets should not be hardcoded.

---

# Backend Components

## Database Setup

SQLAlchemy manages communication between the application and database.

Example:

```python
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()
```

---

## User Model

The User model represents the database users table.

Main fields:

| Field | Description |
|---|---|
| id | Primary key |
| username | Unique username |
| email | Unique email address |
| hashed_password | Secure password hash |
| created_at | Account creation timestamp |

---

## Database Dependency

Each API request receives a database session which is automatically closed after completion.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

# Authentication

## Password Hashing

Passwords are hashed using bcrypt before storing them.

Flow:

```
Plain Password
       |
       |
     bcrypt
       |
       |
Hashed Password
       |
       |
Database
```

---

## JWT Authentication

After successful login, the backend creates a JWT token containing:

- User ID
- Username
- Expiration time

The frontend sends this token with future requests.

---

# API Endpoints

## Health Check

```
GET /
```

Checks whether the backend server is running.

---

## Register User

```
POST /api/auth/register
```

Flow:

1. Receive user information.
2. Check if user already exists.
3. Hash password.
4. Save user to database.
5. Return JWT token.

---

## Login User

```
POST /api/auth/login
```

Flow:

1. Find user by username.
2. Verify password.
3. Generate JWT token.
4. Return authentication token.

---

## User APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users` | Retrieve all users |
| GET | `/api/users/{id}` | Retrieve specific user |
| DELETE | `/api/users/{id}` | Delete user |

---

# Frontend

## API Layer

`api.js` handles all communication with the backend.

Responsibilities:

- Sending API requests
- Adding authentication headers
- Handling API responses

Reason:

> Centralizes API communication and avoids duplicate request logic.

---

# React Components

## Login Component

Responsibilities:

- Handle login form
- Send credentials to backend
- Store JWT token
- Redirect user to dashboard

---

## Register Component

Responsibilities:

- Handle registration form
- Submit user information
- Create new account

---

## Dashboard Component

Responsibilities:

- Fetch logged-in user information
- Display user list
- Delete users

---

## Protected Routes

ProtectedRoute checks whether a valid authentication token exists before showing protected pages.

Reason:

> Prevents unauthorized access to application pages.

---

# Project Structure

```
user-management-system/

├── backend/
│   ├── simple_server.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   │
│   └── package.json
│
└── README.md
```

---

# Running Locally

## Backend Setup

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn simple_server:app --reload --port 9000
```

Backend runs at:

```
http://localhost:9000
```

Swagger documentation:

```
http://localhost:9000/docs
```

---

## Frontend Setup

Install dependencies:

```bash
npm install
```

Run React application:

```bash
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# Future Improvements

Possible improvements:

- PostgreSQL database
- Alembic database migrations
- Refresh token authentication
- Role-based access control
- Automated backend tests
- CI/CD pipeline
- Production deployment

---

# Summary

This project demonstrates:

✅ REST API development using FastAPI  
✅ Database operations using SQLAlchemy ORM  
✅ JWT-based authentication  
✅ Password security using bcrypt  
✅ React frontend integration  
✅ Full-stack application architecture  
