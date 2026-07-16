# api/routers/auth.py
# PURPOSE: HTTP endpoints for registration and login.
# LAYER: API / Router (HTTP layer)
# CALLED BY: main.py (mounts this router)
# CALLS: services/user_service.py, core/security.py, db/database.py
#
# WHY A ROUTER?
# FastAPI Routers are like mini-apps. They group related endpoints together.
# We mount routers in main.py, which keeps main.py clean and small.
# This is exactly how large codebases organize hundreds of endpoints.
#
# DEPENDENCY INJECTION IN FASTAPI:
# When you write `db: Session = Depends(get_db)`, FastAPI:
# 1. Sees the Depends() call
# 2. Calls get_db() automatically
# 3. Injects the result as `db` into your function
# This is Inversion of Control - you don't manage dependencies, FastAPI does.

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.db.database import get_db
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse
from app.services import user_service

# APIRouter is a FastAPI class for grouping routes.
# prefix='/auth' means all routes here start with /auth
# tags=['Authentication'] groups them in Swagger docs
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    POST /auth/register
    Register a new user account.

    REQUEST BODY (validated by UserCreate Pydantic schema):
    {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "securepassword123"
    }

    RESPONSE (shaped by UserResponse schema - no hashed_password):
    {
        "id": 1,
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "is_active": true,
        "is_admin": false,
        "created_at": "2024-01-01T00:00:00"
    }

    STATUS CODES:
    201 Created     - user successfully registered
    400 Bad Request - email already exists
    422 Unprocessable Entity - Pydantic validation failed (auto)

    REGISTRATION FLOW:
    Request -> Pydantic validates -> check duplicate email
    -> hash password -> save to DB -> return user (no password)
    """
    # Check if email is already taken
    existing_user = user_service.get_user_by_email(db, email=user_data.email)
    if existing_user:
        # 400 Bad Request - don't use 409 Conflict to avoid email enumeration
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # Create user (password will be hashed inside create_user)
    new_user = user_service.create_user(db, user_data)
    return new_user


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    POST /auth/login
    Authenticate user and return a JWT access token.

    REQUEST BODY:
    {
        "email": "jane@example.com",
        "password": "securepassword123"
    }

    RESPONSE:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }

    STATUS CODES:
    200 OK           - login successful, token returned
    401 Unauthorized - wrong email or password

    LOGIN FLOW:
    Request -> Pydantic validates -> look up user by email
    -> bcrypt verify password -> create JWT -> return token

    The client must store this token and send it as:
    Authorization: Bearer <access_token>
    on every protected request.
    """
    # Verify credentials (returns User or None)
    user = user_service.authenticate_user(db, login_data.email, login_data.password)

    if not user:
        # Always return the same error for wrong email OR wrong password
        # This prevents attackers from knowing which field was wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            # WWW-Authenticate header is required by HTTP spec for 401 responses
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account has been deactivated.",
        )

    # Create JWT token with user's email as the subject claim
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ─── DEPENDENCY: get_current_user ─────────────────────────────────────────────────
# This function is NOT an endpoint. It's a DEPENDENCY used by protected routes.
# Any route that declares `current_user = Depends(get_current_user)` will:
# 1. Require an Authorization header
# 2. Validate the JWT
# 3. Look up the user
# 4. Either inject the user or return 401

from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer tells FastAPI where to find the token.
# tokenUrl is the login endpoint (used by Swagger UI's Authorize button).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency that validates JWT and returns the authenticated user.
    Inject this into any route to make it protected.

    HOW IT WORKS:
    FastAPI reads the Authorization: Bearer <token> header automatically.
    We decode the JWT, extract the email, look up the user.
    If anything fails, we raise HTTP 401.

    USAGE IN A ROUTE:
    @router.get('/profile')
    def get_profile(current_user: User = Depends(get_current_user)):
        return current_user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode and verify the JWT
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    # Look up the user
    user = user_service.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    """
    GET /auth/profile
    Returns the currently authenticated user's profile.
    PROTECTED: requires valid JWT in Authorization header.

    This demonstrates how dependency injection protects an endpoint:
    If the JWT is missing/invalid, get_current_user raises 401
    and this function never even runs.
    """
    return current_user
