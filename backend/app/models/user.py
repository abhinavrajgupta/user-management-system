# models/user.py
# PURPOSE: SQLAlchemy ORM model representing the `users` table in MySQL.
# LAYER: Database (model layer)
# CALLED BY: services/user_service.py (queries), db/database.py (table creation)
# CALLS: db/database.py (Base)
#
# WHY THIS EXISTS:
# Instead of writing raw SQL like `CREATE TABLE users (...)`,
# we define a Python class. SQLAlchemy translates this class into SQL.
# This is called ORM - Object Relational Mapping.
# You work with Python objects; SQLAlchemy handles the SQL.
#
# HOW SQLAlchemy MODEL -> SQL WORKS:
# class User(Base)               -> CREATE TABLE users (
#   __tablename__ = 'users'      ->   (table name)
#   id = Column(Integer, ...)    ->   id INT AUTO_INCREMENT PRIMARY KEY,
#   email = Column(String, ...)  ->   email VARCHAR(255) UNIQUE NOT NULL
#                                -> );

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    """
    SQLAlchemy model for the users table.

    WHAT IS A PRIMARY KEY?
    A unique identifier for each row. No two rows can have the same id.
    AUTO_INCREMENT means the DB assigns it automatically (1, 2, 3...).

    WHAT IS UNIQUE?
    A UNIQUE constraint means no two rows can have the same value in that column.
    Perfect for email - you can't have two accounts with the same email.

    WHAT IS INDEX?
    An index is like a book's index - it makes lookups by that column much faster.
    Without an index, MySQL scans every row to find matching emails.
    With an index, it jumps directly to the right rows.
    Trade-off: indexes speed up reads but slow down writes.
    """

    # __tablename__ tells SQLAlchemy what to call the table in MySQL
    __tablename__ = "users"

    # Primary key - auto-incrementing integer
    # index=True adds a B-tree index on this column (it's automatic for PKs)
    id = Column(Integer, primary_key=True, index=True)

    # Full name of the user
    # nullable=False means this column CANNOT be empty (NOT NULL in SQL)
    full_name = Column(String(255), nullable=False)

    # Email - must be unique across all users
    # unique=True adds a UNIQUE constraint
    # index=True adds an index for fast lookup by email (we query by email often)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # We NEVER store plain passwords. Only bcrypt hashes.
    # A bcrypt hash is always 60 characters long.
    hashed_password = Column(String(255), nullable=False)

    # Account status flag
    # default=True means new users are active by default
    is_active = Column(Boolean, default=True)

    # Admin flag - most users are not admins
    is_admin = Column(Boolean, default=False)

    # Automatic timestamps
    # server_default=func.now() tells MySQL to set this to NOW() automatically
    # We don't have to set these manually in Python
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # onupdate=func.now() updates this timestamp whenever the row is modified
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        """String representation for debugging. Shown when you print(user)."""
        return f"<User id={self.id} email={self.email}>"
