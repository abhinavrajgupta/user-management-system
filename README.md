# User Management System

A full-stack user management project with a FastAPI backend, a React frontend, JWT authentication, and Swagger docs for API testing.[cite:1]

## Tech stack

- Backend: FastAPI, SQLAlchemy, bcrypt, python-jose.[cite:1]
- Database: SQLite stored locally as `demo.db` in the `backend/` folder.[cite:1]
- Frontend: React app in the `frontend/` directory.[cite:1]
- API docs: Swagger UI is available at `/docs` when the backend is running.[cite:1]

## Project structure

```text
user-management-system/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

The repository contains separate `backend/` and `frontend/` folders, so the API and UI should be started separately during local development unless Docker is used to orchestrate both.[cite:1]

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
pip install fastapi uvicorn sqlalchemy bcrypt python-jose[cryptography] pydantic python-dotenv
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

- The backend runs on `http://localhost:9000`.[cite:1]
- Swagger UI is available at `http://localhost:9000/docs`.[cite:1]
- This step starts the API only; it does **not** render the React frontend.[cite:1]

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
- Open `http://localhost:9000/docs` to test the API in Swagger UI.[cite:1]

## Important note about the old instructions

The previous README flow entered `backend/`, created a Python environment, and ran `uvicorn simple_server:app --host 0.0.0.0 --port 9000`.[cite:1]
That flow correctly launches the FastAPI API and Swagger docs, but it does not include any step to install or start the React frontend even though the repository includes a `frontend/` directory.[cite:1]

## Option 2: Run with Docker Compose

The repository also includes a `docker-compose.yml` file, which indicates there is a containerized way to orchestrate services together.[cite:1]
A typical usage pattern is:

```bash
docker compose up --build
```

If Docker Compose is configured correctly for both services, it should bring up the backend and frontend together using the repository's compose file.[cite:1]

## Backend API endpoints

Once the backend is running, Swagger shows these routes:[cite:1]

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` [cite:1] | Health check [cite:1] |
| POST | `/api/auth/register` [cite:1] | Register a user [cite:1] |
| POST | `/api/auth/login` [cite:1] | Log in and receive a JWT token [cite:1] |
| GET | `/api/users` [cite:1] | List all users [cite:1] |
| GET | `/api/users/{user_id}` [cite:1] | Get a user by ID [cite:1] |
| DELETE | `/api/users/{user_id}` [cite:1] | Delete a user by ID [cite:1] |

## Troubleshooting

### Backend works but no UI appears

If `http://localhost:9000` or `http://localhost:9000/docs` works but no frontend page is rendered, the backend is running but the frontend has not been started yet.[cite:1]
Start the React app from the `frontend/` directory in a separate terminal.[cite:1]

### Frontend starts but cannot reach the API

Make sure the backend is running on port `9000` and confirm the frontend is configured to call the backend at `http://localhost:9000` or the matching API base URL for your environment.

### SQLite database file

The SQLite database file `demo.db` is created automatically in `backend/` on first run.[cite:1]
No separate external database setup is required for the documented local backend flow.[cite:1]
