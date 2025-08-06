# app/utils/security.py

"""Security utilities for password hashing and JWT token generation."""

import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password (str): The raw password.

    Returns:
        str: Bcrypt-hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its hashed version.

    Args:
        plain_password (str): The raw password.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a JWT access token from the given payload.

    Args:
        data (dict): Payload to encode in the token.
        expires_delta (timedelta | None): Optional custom expiration.

    Returns:
        str: Encoded JWT token.

    Raises:
        EnvironmentError: If required environment variables are missing or invalid.
    """
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
        raise EnvironmentError("Missing critical JWT environment variables.")

    try:
        expire_minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES)
    except ValueError as exc:
        raise EnvironmentError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer.") from exc
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=expire_minutes))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
