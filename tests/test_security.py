# tests/test_security.py

import os
import pytest
from datetime import datetime, timezone, timedelta
from jose import jwt
from unittest.mock import patch
from app.utils import security

@pytest.fixture
def password():
    return "securepassword123"

@pytest.fixture
def fake_env():
    return {
        "JWT_SECRET_KEY": "testsecret",
        "JWT_ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
    }

def test_get_password_hash_and_verify():
    """
    Test that a password is hashed correctly and that the verification returns True.
    """
    raw_password = "securepassword123"
    hashed_password = security.get_password_hash(raw_password)

    # Ensure the hash is not equal to the raw password
    assert hashed_password != raw_password
    assert isinstance(hashed_password, str)
    assert len(hashed_password) > 0

    # Verify the password
    assert security.verify_password(raw_password, hashed_password) is True

    # Verify fails with incorrect password
    assert security.verify_password("wrongpassword", hashed_password) is False

def test_create_access_token(fake_env):
    """
    Test token creation with fake env variables and ensure payload is correctly encoded.
    """
    with patch.dict(os.environ, fake_env):
        user_data = {"sub": "123"}
        token = security.create_access_token(user_data)

        # Decode the token to check contents
        decoded = jwt.decode(token, fake_env["JWT_SECRET_KEY"], algorithms=[fake_env["JWT_ALGORITHM"]])

        assert decoded["sub"] == "123"
        assert "exp" in decoded

        # Optional: check that expiration is within expected range
        now = datetime.now(timezone.utc)
        expire_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        assert timedelta(minutes=0) < (expire_time - now) <= timedelta(minutes=60)

def test_create_access_token_with_custom_expiry(fake_env):
    """
    Test token creation using a custom expiration time and verify its validity.
    """
    with patch.dict(os.environ, fake_env):
        user_data = {"sub": "456"}
        expires = timedelta(minutes=5)
        now = datetime.now(timezone.utc)
        token = security.create_access_token(user_data, expires_delta=expires)

        decoded = jwt.decode(token, fake_env["JWT_SECRET_KEY"], algorithms=[fake_env["JWT_ALGORITHM"]])

        assert decoded["sub"] == "456"
        assert "exp" in decoded

        expire_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        # Check that expiry is within a few seconds of now + 5 minutes
        expected_expiry = now + expires
        assert abs((expire_time - expected_expiry).total_seconds()) < 5
