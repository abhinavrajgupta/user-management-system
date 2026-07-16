# database.py
# PURPOSE: Database connection and session management.
# LAYER: Database layer
# CALLED BY: main.py (to create tables), all routers (via get_db dependency)
# CALLS: SQLAlchemy, config.py
#
# WHY THIS EXISTS:
# Every database operation needs a "session" - a unit of work that tracks
# changes and can commit or rollback. This file creates sessions and
# provides them to route handlers via dependency injection.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# create_engine establishes the connection pool to MySQL.
# The DATABASE_URL tells SQLAlchemy:
#   - Which database type (mysql+pymysql)
#   - Credentials (username:password)
#   - Host and port
#   - Database name
# A connection pool keeps connections open and reuses them for performance.
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True tests connections before using them.
    # This handles cases where the DB server closes idle connections.
    pool_pre_ping=True,
    # echo=True prints SQL statements to console (useful for debugging).
    # Set to False in production.
    echo=settings.DEBUG,
)

# SessionLocal is a factory class that creates new database sessions.
# Each request gets its own session (created and closed per-request).
# autocommit=False: changes are NOT saved until we call session.commit()
# autoflush=False: changes are NOT sent to DB until commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all SQLAlchemy models inherit from.
# When you define a class that inherits Base, SQLAlchemy knows
# it represents a database table.
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session to route handlers.

    HOW DEPENDENCY INJECTION WORKS IN FASTAPI:
    When a route declares `db: Session = Depends(get_db)`, FastAPI:
    1. Calls get_db() before the route function runs
    2. Passes the session to the route function
    3. After the route returns, resumes execution after `yield`
    4. Closes the session

    This is the context manager pattern using `yield`.
    The `finally` block ALWAYS runs, even if an exception occurs,
    ensuring connections are never leaked.

    INTERVIEW ANSWER: "We use a generator function with yield so that
    the session lifecycle (open/close) is managed automatically by
    FastAPI's dependency injection system, preventing connection leaks."
    """
    db = SessionLocal()  # Open a new session
    try:
        yield db          # Provide it to the route handler
    finally:
        db.close()        # Always close, even if the route raised an exception
