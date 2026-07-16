from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, users
from app.core.config import settings
from app.db.database import Base, engine

# Create the FastAPI application.
# Metadata (title, version, description) appears in Swagger (/docs).
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    User Management System API

    ## Features
    - JWT Authentication
    - User CRUD Operations
    - Protected Routes
    - Input Validation with Pydantic

    ## Authentication
    1. Register or login
    2. Copy the returned JWT token
    3. Click "Authorize" in Swagger
    4. Enter: Bearer <token>
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable Cross-Origin Resource Sharing (CORS)
# Allows frontend applications (React/Vite) to communicate
# with this backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """
    Runs once when the application starts.

    Creates database tables from SQLAlchemy models if they
    do not already exist.

    Note:
    In production, Alembic is typically used instead of
    create_all() for database migrations.
    """
    Base.metadata.create_all(bind=engine)


# Register routers.
# Each router groups related endpoints (authentication, users, etc.).
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def health_check():
    """
    Simple endpoint used to verify that the API is running.
    Useful for monitoring, load balancers, and quick testing.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
