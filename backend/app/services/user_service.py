from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


# Business logic for user management.
# Routers call these functions instead of interacting with the database directly.
# This separation keeps HTTP handling and business logic independent.


# ---------- Read Operations ----------

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Return a user by ID, or None if not found."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return a user by email, or None if not found."""
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Return a paginated list of users.

    Pagination prevents loading every record into memory,
    which improves performance on large datasets.
    """
    return db.query(User).offset(skip).limit(limit).all()


# ---------- Write Operations ----------

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user.

    Passwords are hashed before storage so plain-text passwords
    are never saved in the database.
    """
    hashed_password = get_password_hash(user_data.password)

    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)   # Reload generated fields such as id and timestamps.

    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """
    Update only the fields provided by the client.

    If the password is updated, it is re-hashed before saving.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(
            update_data.pop("password")
        )

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user. Returns True if successful, otherwise False."""
    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return False

    db.delete(db_user)
    db.commit()

    return True


# ---------- Authentication ----------

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user using email and password.

    Returns the User object if authentication succeeds,
    otherwise returns None.

    The same failure response is used for both invalid emails
    and incorrect passwords to avoid leaking account information.
    """
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
