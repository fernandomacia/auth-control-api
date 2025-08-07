import token
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status
from app.models.user import User
from app.services.users import get_current_user, JWT_SECRET_KEY, JWT_ALGORITHM

# Reuse from your code or define directly


def generate_expired_token(user_id: int) -> str:
    """
    Creates a JWT token that is already expired for testing purposes.
    """
    expire = datetime.now(timezone.utc) - timedelta(minutes=1)
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp())
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def test_expired_token_returns_token_expired(client, db):
    """
    Verifies that using an expired token returns a 401 with 'Token expired'.
    """
    # Get an active user from the test database
    user: User = db.query(User).filter(User.email == "testadmin@example.net").first()
    expired_token = generate_expired_token(user.id)

    response = client.put(
        "/users/me", 
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token expired"
