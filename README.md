# User Management System

A full-stack user management project with a React frontend and FastAPI backend. The frontend and backend can be run separately for local development, and the backend API can be tested directly in Swagger UI.

## Project Structure

```bash
user-management-system/
├── backend/
│   ├── simple_server.py
│   ├── requirements.txt
│   ├── .env
│   └── ...
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
└── docker-compose.yml
```

## Run the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=sqlite:///./demo.db
SECRET_KEY=supersecretkey
```

Start the FastAPI server:

```bash
uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload
```

Backend URLs:
- API: `http://localhost:9000`
- Swagger Docs: `http://localhost:9000/docs`

## Run the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend URL:
- App: `http://localhost:3000`

## Frontend and Backend

Run both apps separately in two terminals:
- Terminal 1: backend on port `9000`
- Terminal 2: frontend on port `3000`

The frontend works when it points to the backend API running at `http://localhost:9000`.

## Swagger API Testing

Open:

```text
http://localhost:9000/docs
```

### Main Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/users` | List users |
| GET | `/api/users/{user_id}` | Get one user |
| DELETE | `/api/users/{user_id}` | Delete user |

### Quick Test Flow

1. Test `GET /`
2. Register with `POST /api/auth/register`
3. Login with `POST /api/auth/login`
4. Test `GET /api/users`
5. Test `GET /api/users/{user_id}`
6. Test `DELETE /api/users/{user_id}`

### Example Test Inputs

#### Register user

Good:
```json
{
  "username": "demo_user",
  "email": "demo@example.com",
  "password": "Demo1234!"
}
```

Bad:
```json
{
  "username": "demo_user",
  "password": "Demo1234!"
}
```

#### Login user

Good:
```json
{
  "username": "demo_user",
  "password": "Demo1234!"
}
```

Bad:
```json
{
  "username": "demo_user",
  "password": "wrongpass"
}
```

#### Get user by ID

Good:
```text
1
```

Bad:
```text
abc
```

#### Delete user

Good:
```text
2
```

Bad:
```text
9999
```

## Notes

- The current README  documents the backend routes used for register, login, list, get-by-id, and delete testing.
