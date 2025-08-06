# tests/users/test_user_routes.py

"""Test suite for user self-update routes (/users/me)."""

import pytest
from app.models.user import User
from app.models.language import Language
from app.utils.security import create_access_token


def ensure_language_exists(db, code: str, name: str):
    """
    Ensure a language exists in the database.

    Prevents unique constraint violations on repeated test runs.

    Args:
        db (Session): SQLAlchemy test database session.
        code (str): Language code (e.g., "es").
        name (str): Language name (e.g., "Español").
    """
    if not db.query(Language).filter_by(code=code).first():
        db.add(Language(code=code, name=name))
        db.commit()


def test_update_language_success(client, db):
    """
    Verify successful update of user language.

    Asserts:
        - 200 OK
        - Updated language code in DB and response
    """
    user = db.query(User).filter(User.email == "testadmin@example.net").first()
    ensure_language_exists(db, "es", "Español")

    token = create_access_token(data={"sub": str(user.id)})

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"language_code": "es"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User updated successfully"
    assert data["data"]["user_language"] == "es"

    db.refresh(user)
    assert user.language.code == "es"


def test_update_language_not_found(client, db):
    """
    Verify that an unknown language code returns 400.

    Asserts:
        - 400 Bad Request
        - Proper error message and empty data object
    """
    user = db.query(User).filter(User.email == "testadmin@example.net").first()
    token = create_access_token(data={"sub": str(user.id)})

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"language_code": "zz"}
    )

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Language not found"
    assert data["data"] == {}


def test_update_language_inactive_user(client, db):
    """
    Ensure language update is blocked for inactive users.

    Asserts:
        - 401 Unauthorized
        - Error message indicating inactive or invalid user
    """
    user = db.query(User).filter(User.email == "testadmin@example.net").first()
    ensure_language_exists(db, "es", "Español")

    user.is_active = False
    db.commit()

    token = create_access_token(data={"sub": str(user.id)})

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"language_code": "es"}
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Inactive or invalid user"

    # Restore user for future tests
    user.is_active = True
    db.commit()


def test_update_language_user_not_found(client):
    """
    Ensure 401 is returned if the user ID does not exist.

    Asserts:
        - 401 Unauthorized
        - Error message indicating inactive or invalid user
    """
    token = create_access_token(data={"sub": "99999"})  # Non-existent user ID

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"language_code": "es"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Inactive or invalid user"

