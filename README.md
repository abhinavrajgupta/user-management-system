# User Management System

A full-stack user management project with a FastAPI backend, a React frontend, JWT authentication, and Swagger docs for API testing.

## Tech stack

- Backend: FastAPI, SQLAlchemy, bcrypt, python-jose.
- Database: SQLite stored locally as `demo.db` in the `backend/` folder.
- Frontend: React app in the `frontend/` directory.
- API docs: Swagger UI is available at `/docs` when the backend is running.

## Project structure

```text
user-management-system/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

The repository contains separate `backend/` and `frontend/` folders, so the API and UI should be started separately during local development unless Docker is used to orchestrate both.

## Option 1: Run locally

### 1. Clone the repository

```bash
git clone https://github.com/abhinavrajgupta/user-management-system.git
cd user-management-system
```

### 2. Start the backend

Open a terminal and run:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

On Windows, use:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy bcrypt python-jose[cryptography] pydantic python-dotenv pymysql
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=sqlite:///./demo.db
SECRET_KEY=supersecretkey
```

Then start the API server:

```bash
uvicorn simple_server:app --host 0.0.0.0 --port 9000
```

Expected result:

- The backend runs on `http://localhost:9000`.
- Swagger UI is available at `http://localhost:9000/docs`.
- This step starts the API only; it does **not** render the React frontend.

### 3. Start the frontend

Open a **second terminal** from the project root and run:

```bash
cd frontend
npm install
npm run dev
```

If `npm run dev` does not exist, check `frontend/package.json` and use the defined start script, such as:

```bash
npm start
```

Expected result:

- The frontend should start on the local port printed by the terminal, commonly `http://localhost:3000` or `http://localhost:5173`.
- Keep the backend running on port `9000` in one terminal and the frontend running in another terminal.

### 4. Open the app

- Open the frontend URL printed by the frontend dev server to use the React UI.
- Open `http://localhost:9000/docs` to test the API in Swagger UI.

## Important note about the old instructions

The previous README flow entered `backend/`, created a Python environment, and ran `uvicorn simple_server:app --host 0.0.0.0 --port 9000`.
That flow correctly launches the FastAPI API and Swagger docs, but it does not include any step to install or start the React frontend even though the repository includes a `frontend/` directory.

## Option 2: Run with Docker Compose

The repository also includes a `docker-compose.yml` file, which indicates there is a containerized way to orchestrate services together.
A typical usage pattern is:

```bash
docker compose up --build
```

If Docker Compose is configured correctly for both services, it should bring up the backend and frontend together using the repository's compose file.

## Backend API endpoints

Once the backend is running, Swagger shows these routes:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/`  | Health check  |
| POST | `/api/auth/register`  | Register a user  |
| POST | `/api/auth/login`  | Log in and receive a JWT token  |
| GET | `/api/users`  | List all users  |
| GET | `/api/users/{user_id}`  | Get a user by ID  |
| DELETE | `/api/users/{user_id}`  | Delete a user by ID  |

## Troubleshooting

### Backend works but no UI appears

If `http://localhost:9000` or `http://localhost:9000/docs` works but no frontend page is rendered, the backend is running but the frontend has not been started yet.
Start the React app from the `frontend/` directory in a separate terminal.

### Frontend starts but cannot reach the API

Make sure the backend is running on port `9000` and confirm the frontend is configured to call the backend at `http://localhost:9000` or the matching API base URL for your environment.

### SQLite database file

The SQLite database file `demo.db` is created automatically in `backend/` on first run.
No separate external database setup is required for the documented local backend flow.
