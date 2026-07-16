# main.py
# PURPOSE: FastAPI application entry point. Creates the app, mounts routers, configures middleware.
# LAYER: Application bootstrap
# CALLED BY: uvicorn (the server) when you run: uvicorn app.main:app --reload
# CALLS: All routers, database (for table creation)
#
# APPLICATION LIFECYCLE:
# 1. Python imports this file
# 2. FastAPI() app object is created
# 3. CORS middleware is added
# 4. startup event fires -> creates DB tables
# 5. Routers are registered
# 6. Uvicorn starts listening for HTTP requests
# 7. Requests flow: uvicorn -> FastAPI -> Router -> Service -> Database

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, users
from app.core.config import settings
from app.db.database import Base, engine

# Create the FastAPI application instance.
# title and version appear in the auto-generated Swagger docs.
# docs_url='/docs' -> Swagger UI (interactive API explorer)
# redoc_url='/redoc' -> ReDoc (cleaner API docs)
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    User Management System API

    ## Features
    - **Authentication**: Register, Login with JWT tokens
    - **User CRUD**: Create, Read, Update, Delete users
    - **Protected Routes**: JWT-based authorization
    - **Input Validation**: Pydantic schemas

    ## How to authenticate in Swagger:
    1. POST /auth/register to create account
    2. POST /auth/login to get JWT token
    3. Click 'Authorize' button at top right
    4. Enter: Bearer <your_token>
    5. All protected endpoints now work!
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS MIDDLEWARE ──────────────────────────────────────────────────────────
# WHAT IS CORS?
# Cross-Origin Resource Sharing. A browser security feature.
# By default, browsers block JavaScript from making API calls to a DIFFERENT
# domain than the page is loaded from.
#
# WHY WE NEED IT:
# React runs on http://localhost:3000
# FastAPI runs on http://localhost:8000
# Without CORS, the browser blocks React's requests to FastAPI.
# We explicitly allow our React app's origin.
#
# allow_origins: list of allowed origins (domains)
# allow_credentials: allow cookies/auth headers
# allow_methods: which HTTP methods are allowed
# allow_headers: which headers are allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server (alternative)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allow Authorization, Content-Type, etc.
)


# ─── APPLICATION STARTUP EVENT ───────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    """
    Runs once when the application starts.
    Creates all database tables that don't exist yet.

    Base.metadata.create_all(bind=engine) tells SQLAlchemy:
    'Look at all classes that inherit from Base (our User model),
    and create their corresponding tables in the database if they don't exist.'

    This is NOT a migration tool (that's Alembic).
    It simply creates missing tables - safe to run on every startup.

    INTERVIEW ANSWER: 'In production, we'd use Alembic for database migrations
    to track schema changes with version history, similar to Git for the database.'
    """
    Base.metadata.create_all(bind=engine)


# ─── ROUTER REGISTRATION ───────────────────────────────────────────────────────────
# include_router mounts a router's endpoints onto the main app.
# All routes in auth.router (prefixed /auth) are now available.
# All routes in users.router (prefixed /users) are now available.
app.include_router(auth.router)
app.include_router(users.router)


# ─── ROOT HEALTH CHECK ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def health_check():
    """
    GET /
    Health check endpoint.
    Used by load balancers and monitoring tools to check if the app is running.
    Returns 200 OK if the service is up.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


# ─── FINAL ROUTE MAP ──────────────────────────────────────────────────────────────
# GET  /                   -> health check
# POST /auth/register      -> create account
# POST /auth/login         -> get JWT token
# GET  /auth/profile       -> get my profile (protected)
# GET  /users              -> list all users (protected)
# GET  /users/{id}         -> get user by ID (protected)
# POST /users              -> create user (protected)
# PUT  /users/{id}         -> update user (protected)
# DELETE /users/{id}       -> delete user (protected)
# GET  /docs               -> Swagger UI
# GET  /redoc              -> ReDoc
