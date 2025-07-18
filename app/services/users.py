# app/services/user.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.database import get_db
from app.models.user import User
import os

# OAuth2 scheme to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT configuration from environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Extracts the current authenticated user from the access token.

    Decodes the JWT, retrieves the user from the database, and validates
    their existence and active status.

    Args:
        token (str): Bearer token from the Authorization header.
        db (Session): Database session dependency.

    Returns:
        User: The authenticated and active user.

    Raises:
        HTTPException: 401 if token is invalid, user not found, or inactive.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter_by(id=user_id).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or invalid user",
        )

    return user

