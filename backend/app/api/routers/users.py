# api/routers/users.py
# PURPOSE: HTTP endpoints for user CRUD operations.
# LAYER: API / Router (HTTP layer)
# CALLED BY: main.py (mounts this router)
# CALLS: services/user_service.py, api/routers/auth.py (get_current_user)
#
# All endpoints here are PROTECTED - you must be logged in.
# We demonstrate all 5 CRUD operations:
# CREATE  -> POST   /users
# READ    -> GET    /users      (list)
# READ    -> GET    /users/{id} (single)
# UPDATE  -> PUT    /users/{id}
# DELETE  -> DELETE /users/{id}

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.routers.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip (for pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # PROTECTED
):
    """
    GET /users
    List all users with pagination.
    PROTECTED: requires JWT.

    QUERY PARAMETERS:
    - skip: offset for pagination (default 0)
    - limit: max results (default 10, max 100)

    EXAMPLE: GET /users?skip=0&limit=10

    Query(...) is a FastAPI class for query parameter validation.
    ge=0 means 'greater than or equal to 0' (no negative skip).
    le=100 means 'less than or equal to 100' (max page size enforced).
    """
    users = user_service.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # PROTECTED
):
    """
    GET /users/{user_id}
    Get a single user by ID.
    PROTECTED: requires JWT.

    PATH PARAMETER:
    user_id: integer in the URL path (e.g., /users/42)
    FastAPI automatically parses the integer from the URL.

    STATUS CODES:
    200 OK        - user found and returned
    404 Not Found - no user with that ID
    """
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return db_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # PROTECTED
):
    """
    POST /users
    Admin endpoint to create a user.
    PROTECTED: requires JWT.

    This is separate from /auth/register because in real apps,
    admins might create users directly without them self-registering.

    STATUS CODES:
    201 Created     - user created
    400 Bad Request - email already taken
    """
    existing = user_service.get_user_by_email(db, email=user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )
    return user_service.create_user(db, user_data)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # PROTECTED
):
    """
    PUT /users/{user_id}
    Update a user's information.
    PROTECTED: requires JWT.

    PARTIAL UPDATE:
    You don't have to send all fields - only the ones you want to change.
    {"full_name": "New Name"} is valid even though email is not included.
    This works because UserUpdate has all Optional fields.

    STATUS CODES:
    200 OK        - user updated
    404 Not Found - user doesn't exist
    """
    updated_user = user_service.update_user(db, user_id=user_id, user_data=user_data)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # PROTECTED
):
    """
    DELETE /users/{user_id}
    Delete a user.
    PROTECTED: requires JWT.

    STATUS CODES:
    204 No Content - user deleted (no response body)
    404 Not Found  - user doesn't exist

    WHY 204 NO CONTENT?
    After deletion, there's nothing to return.
    204 means 'success but no body' - it's the standard for DELETE.
    """
    deleted = user_service.delete_user(db, user_id=user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    # No return needed - 204 sends empty response body
