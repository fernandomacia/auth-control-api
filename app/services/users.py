# app/services/user.py

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.database import get_db
from app.models.user import User

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
    Extracts the authenticated user from the JWT token.

    - Decodes the JWT and retrieves the user by ID.
    - Verifies that the user exists and is active.
    - Raises 401 if the token is invalid or the user is inactive.

    Args:
        token (str): Bearer token from the Authorization header.
        db (Session): SQLAlchemy database session.

    Returns:
        User: Authenticated and active user.
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


def get_current_admin_or_superadmin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Grants access only to users with 'admin' or 'superadmin' roles.

    - Requires the user to be authenticated and active.
    - Raises 403 if the user role is not allowed.

    Args:
        current_user (User): Authenticated user.

    Returns:
        User: Authenticated user with admin or superadmin role.
    """
    if current_user.role.name not in ("admin", "superadmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Superadmin privileges required"
        )

    return current_user

