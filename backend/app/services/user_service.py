# services/user_service.py
# PURPOSE: All business logic and database operations for users.
# LAYER: Service (business logic layer)
# CALLED BY: api/routers/auth.py, api/routers/users.py
# CALLS: models/user.py, schemas/user.py, core/security.py
#
# WHY A SERVICE LAYER?
# Routers should only handle HTTP concerns (parsing requests, returning responses).
# Business logic ("does this email already exist?", "hash this password") lives here.
# This separation means:
# - Easy to test services without HTTP
# - Easy to reuse logic across multiple endpoints
# - Easy to swap database without touching routes
#
# WHAT IS AN ORM QUERY?
# Instead of:  SELECT * FROM users WHERE email = 'x@y.com'
# We write:    db.query(User).filter(User.email == email).first()
# SQLAlchemy converts the Python into SQL automatically.

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


# ─── READ OPERATIONS ─────────────────────────────────────────────────────────────

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Fetch a single user by their primary key (id).

    db.query(User)           -> SELECT * FROM users
    .filter(User.id == ...)  -> WHERE id = user_id
    .first()                 -> LIMIT 1 (returns None if not found)

    Returns User object or None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Fetch a user by email address.
    Used during login to look up the user before verifying password.
    Email has an index, so this query is very fast.
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Fetch a paginated list of all users.

    PAGINATION with skip/limit:
    - skip=0, limit=10  -> first 10 users
    - skip=10, limit=10 -> next 10 users (page 2)

    SQL equivalent:
    SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0

    WHY PAGINATION?
    Never return ALL rows from a table - it could be millions.
    Always paginate large datasets for performance.
    """
    return db.query(User).offset(skip).limit(limit).all()


# ─── WRITE OPERATIONS ────────────────────────────────────────────────────────────

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user in the database.

    STEP BY STEP:
    1. Hash the plain-text password (NEVER store plain passwords)
    2. Create a User SQLAlchemy model object
    3. Add it to the session (stages the INSERT)
    4. Commit (executes the INSERT in the database)
    5. Refresh (re-loads the object from DB to get auto-generated id, timestamps)

    WHAT IS db.commit()?
    It sends the pending SQL to the database and makes it permanent.
    Like pressing Save.

    WHAT IS db.refresh()?
    After commit, the Python object doesn't automatically know its
    auto-generated id or server-set timestamps. refresh() re-queries
    the database to populate those fields.
    """
    # Hash password - CRITICAL security step
    hashed_password = get_password_hash(user_data.password)

    # Create SQLAlchemy model instance (not yet in DB)
    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    # Stage the INSERT
    db.add(db_user)

    # Execute the INSERT (write to database)
    db.commit()

    # Re-load to get DB-generated values (id, created_at)
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """
    Update an existing user's fields.
    Only updates fields that were actually provided (partial update).

    user_data.model_dump(exclude_unset=True) returns only fields
    that were explicitly set in the request, not Optional fields that
    defaulted to None. This enables PATCH-like behavior.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    # Get only the fields the client actually sent
    update_data = user_data.model_dump(exclude_unset=True)

    # If password is being changed, hash it before saving
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Apply each field update to the model object
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user by ID.
    Returns True if deleted, False if user not found.
    SQL: DELETE FROM users WHERE id = user_id
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


# ─── AUTHENTICATION ────────────────────────────────────────────────────────────────

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify email + password combination.
    Returns the User object if credentials are valid, None otherwise.

    LOGIN FLOW:
    1. Look up user by email
    2. If not found -> return None (don't reveal if email exists)
    3. Verify the plain password against the stored bcrypt hash
    4. If match -> return User (login succeeds)
    5. If no match -> return None (login fails)

    SECURITY NOTE:
    We return None for both 'email not found' and 'wrong password'.
    If we returned different errors, attackers could enumerate valid emails.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
