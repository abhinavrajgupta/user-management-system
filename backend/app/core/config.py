# config.py
# PURPOSE: Centralized configuration management for the entire application.
# LAYER: Core (cross-cutting concern used by every layer)
# CALLED BY: database.py, security.py, main.py
# CALLS: Nothing — it just reads from the .env file
#
# WHY THIS EXISTS:
# Every app has settings that change between environments (dev vs production):
# database URLs, secret keys, token expiry times.
# Instead of hardcoding these values (which is a security risk and bad practice),
# we store them in a .env file and read them here.
# pydantic-settings reads .env automatically and validates the types.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class reads variables from the .env file automatically.
    Each attribute name must exactly match the variable name in .env.
    Pydantic validates the types — if DATABASE_URL is missing, it raises an error immediately.
    """

    # Application metadata
    APP_NAME: str = "User Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database — loaded from .env
    DATABASE_URL: str

    # JWT (JSON Web Token) configuration
    # SECRET_KEY: the key used to sign tokens (keep this secret!)
    # ALGORITHM: the signing algorithm — HS256 is industry standard
    # ACCESS_TOKEN_EXPIRE_MINUTES: how long before a token expires
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """
        Tells pydantic-settings WHERE to find the .env file.
        env_file = ".env" means look in the current working directory.
        """
        env_file = ".env"


# Create a single shared instance of Settings.
# Every other file imports this `settings` object.
# This is the Singleton pattern — one source of truth for all config.
settings = Settings()
