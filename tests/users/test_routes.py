# tests/users/test_update_user.py

import pytest
from app.models.user import User
from app.models.language import Language
from app.utils.security import create_access_token


def ensure_language_exists(db, code: str, name: str):
    """
    Ensure the language with the given code exists in the database.

    Prevents duplicate insertions that violate the UNIQUE constraint.
    """
    if not db.query(Language).filter_by(code=code).first():
        db.add(Language(code=code, name=name))
        db.commit()


def test_update_language_success(client, db):
    """
    Test successful language update for an active user.

    Verifies that the user language is updated and stored correctly in the database.
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
    Test language update fails if language code does not exist.

    Expects a 400 response with appropriate error message.
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
    Test language update fails if user is inactive.

    Expects a 401 response and does not perform the update.
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

    # Restore user state after test
    user.is_active = True
    db.commit()


def test_update_language_user_not_found(client):
    """
    Test language update fails if user does not exist.

    Expects a 401 response with error message.
    """
    token = create_access_token(data={"sub": "99999"})  # non-existent user

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"language_code": "es"}
    )

    assert response.status_code == 401
    data = response.json()

    assert data["detail"] == "Inactive or invalid user"
