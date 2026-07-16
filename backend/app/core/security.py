# security.py
# PURPOSE: All security-related logic - password hashing and JWT token operations.
# LAYER: Core (used by auth router and user service)
# CALLED BY: app/api/routers/auth.py, app/services/user_service.py
# CALLS: passlib, python-jose, config.py

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# PASSWORD HASHING
# CryptContext manages hashing schemes.
# bcrypt is intentionally slow to resist brute force attacks.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored bcrypt hash.
    bcrypt is NOT deterministic - same password hashes differently each time.
    It embeds a random salt inside the hash, then re-uses it for verification.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    Called at registration before saving to DB.
    Output example: $2b$12$eImiTXuWVxfM37uY4JANjQ...
    """
    return pwd_context.hash(password)


# JWT TOKEN OPERATIONS

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT access token.

    JWT Structure: header.payload.signature
    - Header: algorithm (HS256)
    - Payload: claims embedded (sub, exp) - base64 encoded, NOT encrypted
    - Signature: HMAC of header+payload using SECRET_KEY

    Anyone can decode the payload. Only we can verify the signature.
    Never store sensitive data (passwords) in JWT payload.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 'exp' is a standard JWT registered claim for expiration
    to_encode.update({"exp": expire})

    # jwt.encode signs the payload with SECRET_KEY using HS256
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and verify a JWT token.
    Returns the user email (sub claim) if valid, None if invalid or expired.
    Called on every protected endpoint request.
    """
    try:
        # jwt.decode verifies signature AND checks expiry automatically
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # 'sub' (subject) stores the user's email
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        # Any failure (tampered token, expired) returns None -> caller raises 401
        return None
