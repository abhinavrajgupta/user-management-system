# schemas/user.py
# PURPOSE: Pydantic schemas for API request/response validation and serialization.
# LAYER: API (validation layer between HTTP and business logic)
# CALLED BY: api/routers/auth.py, api/routers/users.py
# CALLS: Nothing - pure data definitions
#
# WHY SCHEMAS ARE DIFFERENT FROM MODELS:
# SQLAlchemy Model (user.py in models/) = What the DATABASE stores
#   - Has hashed_password, created_at, updated_at
#   - Represents a TABLE ROW
#
# Pydantic Schema (this file) = What the API accepts and returns
#   - UserCreate has plain password (for registration input)
#   - UserResponse NEVER has hashed_password (security!)
#   - Represents JSON data in HTTP requests/responses
#
# WHY PYDANTIC?
# Pydantic validates data automatically. If someone sends:
#   {"email": "not-an-email"} -> Pydantic raises 422 Unprocessable Entity
#   {"email": 12345}          -> Pydantic raises 422 (not a string)
# You get free validation, type coercion, and error messages.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ─── BASE SCHEMA ─────────────────────────────────────────────────────────────
# UserBase contains fields shared by multiple schemas.
# We use inheritance to avoid repeating ourselves (DRY principle).

class UserBase(BaseModel):
    """
    Shared fields used across multiple user schemas.
    EmailStr is a special Pydantic type that validates email format.
    """
    full_name: str = Field(..., min_length=2, max_length=100,
                          description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")


# ─── REQUEST SCHEMAS (what clients SEND to us) ───────────────────────────────

class UserCreate(UserBase):
    """
    Schema for POST /register - creating a new user.
    Extends UserBase and adds password.

    Field(...) means the field is REQUIRED (... is Python's Ellipsis).
    min_length=8 enforces minimum password length at the API layer.
    The password is NEVER stored - we hash it before saving.
    """
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")


class UserUpdate(BaseModel):
    """
    Schema for PUT /users/{id} - updating an existing user.
    ALL fields are Optional because partial updates are allowed.
    A client can send just {"full_name": "New Name"} and only that changes.
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


# ─── RESPONSE SCHEMAS (what we SEND back to clients) ─────────────────────────

class UserResponse(UserBase):
    """
    Schema for API responses - what the client receives.

    CRITICAL SECURITY NOTE:
    hashed_password is NOT here. Clients NEVER see password hashes.
    This is the whole point of separating models from schemas.

    model_config with from_attributes=True tells Pydantic:
    "You can create this schema from a SQLAlchemy model object."
    Without this, Pydantic can't read SQLAlchemy model attributes.
    """
    id: int
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── AUTHENTICATION SCHEMAS ───────────────────────────────────────────────────

class LoginRequest(BaseModel):
    """Schema for POST /login request body."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Schema for POST /login response.
    access_token: the JWT string the client stores and sends with requests.
    token_type: always 'bearer' per OAuth2 standard.

    HOW THE CLIENT USES THIS:
    After login, store access_token.
    For protected requests, add header: Authorization: Bearer <access_token>
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Internal schema for decoded JWT payload.
    Used by the get_current_user dependency.
    """
    email: Optional[str] = None
