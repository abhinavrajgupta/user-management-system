# User Management System

A full-stack user management API built with **FastAPI** (Python), **SQLite** (database), and **JWT** authentication. This README covers every step to run the project end-to-end with real example values and outputs.

---

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy + bcrypt + python-jose
- **Database:** SQLite (file-based, zero config)
- **Auth:** JWT Bearer Tokens
- **Docs:** Auto-generated Swagger UI at `/docs`

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/abhinavrajgupta/user-management-system.git
cd user-management-system/backend
```

---

## Step 2 — Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows use: `venv\Scripts\activate`

---

## Step 3 — Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy bcrypt python-jose[cryptography] pydantic python-dotenv
```

---

## Step 4 — Create the `.env` File

Create a `.env` file inside the `backend/` folder:

```env
DATABASE_URL=sqlite:///./demo.db
SECRET_KEY=supersecretkey
```

> The SQLite database file (`demo.db`) will be auto-created when the server starts.

---

## Step 5 — Run the Server

```bash
uvicorn simple_server:app --host 0.0.0.0 --port 9000
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

---

## Step 6 — Open Swagger UI

Navigate to: **http://localhost:9000/docs**

You will see all available endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/users` | List all users |
| GET | `/api/users/{user_id}` | Get a user by ID |
| DELETE | `/api/users/{user_id}` | Delete a user by ID |

---

## Step 7 — Register a User

**Click:** `POST /api/auth/register` → `Try it out` → paste the body below → `Execute`

**Request body:**
```json
{
  "username": "demouser1",
  "email": "demouser1@test.com",
  "password": "Demo1234"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vdXNlcjEiLCJpZCI6MSwi...",
  "token_type": "bearer"
}
```

> Save the `access_token` — you'll need it to authenticate protected requests.

---

## Step 8 — Login

**Click:** `POST /api/auth/login` → `Try it out` → paste the body below → `Execute`

**Request body:**
```json
{
  "username": "demouser1",
  "password": "Demo1234"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vdXNlcjEiLCJpZCI6MSwi...",
  "token_type": "bearer"
}
```

> Wrong password returns `401 Unauthorized: Invalid credentials`

---

## Step 9 — List All Users

**Click:** `GET /api/users` → `Try it out` → `Execute`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "demouser1",
    "email": "demouser1@test.com",
    "is_active": true,
    "created_at": "2026-07-16 04:56:49"
  }
]
```

> Each user shows their `id`, `username`, `email`, `is_active` status, and `created_at` timestamp.

---

## Step 10 — Get a User by ID

**Click:** `GET /api/users/{user_id}` → `Try it out` → set `user_id = 1` → `Execute`

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "demouser1",
  "email": "demouser1@test.com",
  "is_active": true,
  "created_at": "2026-07-16 04:56:49"
}
```

> If the user doesn't exist: `404 Not Found: User not found`

---

## Step 11 — Register a Second User (Optional)

Register another user to see the list grow:

**Request body for** `POST /api/auth/register`:
```json
{
  "username": "demouser2",
  "email": "demouser2@test.com",
  "password": "Demo5678"
}
```

**List all users again** (`GET /api/users`) — now shows both:
```json
[
  {
    "id": 1,
    "username": "demouser1",
    "email": "demouser1@test.com",
    "is_active": true,
    "created_at": "2026-07-16 04:56:49"
  },
  {
    "id": 2,
    "username": "demouser2",
    "email": "demouser2@test.com",
    "is_active": true,
    "created_at": "2026-07-16 05:01:12"
  }
]
```

---

## Step 12 — Delete a User

**Click:** `DELETE /api/users/{user_id}` → `Try it out` → set `user_id = 2` → `Execute`

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

**List users again** (`GET /api/users`) — user 2 is gone:
```json
[
  {
    "id": 1,
    "username": "demouser1",
    "email": "demouser1@test.com",
    "is_active": true,
    "created_at": "2026-07-16 04:56:49"
  }
]
```

> Deleting a non-existent user returns `404 Not Found: User not found`

---

## API Error Reference

| Status Code | Meaning | Example Scenario |
|-------------|---------|------------------|
| 200 | Success | Any successful request |
| 400 | Bad Request | Registering with a username/email already taken |
| 401 | Unauthorized | Wrong password on login |
| 404 | Not Found | Getting/deleting a user ID that doesn't exist |
| 422 | Validation Error | Missing required fields in request body |
| 500 | Server Error | Unexpected internal error |

---

## Running with curl (Alternative to Swagger UI)

**Register:**
```bash
curl -X POST http://localhost:9000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "demouser1", "email": "demouser1@test.com", "password": "Demo1234"}'
```

**Login:**
```bash
curl -X POST http://localhost:9000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demouser1", "password": "Demo1234"}'
```

**List users:**
```bash
curl http://localhost:9000/api/users
```

**Get user by ID:**
```bash
curl http://localhost:9000/api/users/1
```

**Delete user:**
```bash
curl -X DELETE http://localhost:9000/api/users/1
```

---

## Notes

- The SQLite database (`demo.db`) is created automatically in the `backend/` folder on first run.
- No external database setup required — everything works out of the box.
- The JWT token expires after **30 minutes** by default.
- Passwords are hashed with **bcrypt** before storage — never stored in plain text.
- Duplicate usernames or emails on registration return `400 Bad Request`.
