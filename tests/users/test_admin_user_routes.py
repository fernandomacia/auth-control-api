# tests/users/test_admin_user_routes.py

"""Test suite for admin-only endpoint to toggle user active status."""

import uuid
import pytest
from app.models.user import User
from app.models.user_role import UserRole
from app.models.language import Language
from app.utils.security import get_password_hash, create_access_token


@pytest.fixture
def regular_user(db):
    """
    Create and return a regular user (non-admin) for testing purposes.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        User: The created regular user.
    """
    role = db.query(UserRole).filter_by(name="user").first()
    if not role:
        role = UserRole(name="user")
        db.add(role)
        db.commit()

    lang = db.query(Language).filter_by(code="en").first()
    if not lang:
        lang = Language(code="en", name="English")
        db.add(lang)
        db.commit()

    user = User(
        name="Regular",
        email=f"{uuid.uuid4().hex}@example.net",
        hashed_password=get_password_hash("password"),
        role_id=role.id,
        language_id=lang.id,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_update_user_active_status_success(client, db, regular_user):
    """
    Ensure an admin can successfully toggle another user's active status.

    Expects:
        - 200 OK
        - success = True
        - is_active = False
    """
    admin = db.query(User).filter_by(email="testadmin@example.net").first()
    token = create_access_token(data={"sub": str(admin.id)})

    response = client.put(
        f"/users/{regular_user.id}/active",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_active"] is False


def test_update_user_active_status_user_not_found(client, db):
    """
    Ensure a 404 response is returned when the user does not exist.

    Expects:
        - 404 Not Found
        - success = False
        - message = "User not found"
    """
    admin = db.query(User).filter_by(email="testadmin@example.net").first()
    token = create_access_token(data={"sub": str(admin.id)})

    response = client.put(
        "/users/9999/active",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": True},
    )

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "User not found"


def test_update_user_active_status_invalid_value(client, db, regular_user):
    """
    Ensure a 422 response is returned when is_active is not a boolean.

    Expects:
        - 422 Unprocessable Entity
    """
    admin = db.query(User).filter_by(email="testadmin@example.net").first()
    token = create_access_token(data={"sub": str(admin.id)})

    response = client.put(
        f"/users/{regular_user.id}/active",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": "invalid"},
    )

    assert response.status_code == 422


def test_update_user_active_status_unauthorized(client, db, regular_user):
    """
    Ensure a regular user cannot toggle another user's active status.

    Expects:
        - 403 Forbidden
        - detail = "Admin or Superadmin privileges required"
    """
    token = create_access_token(data={"sub": str(regular_user.id)})

    response = client.put(
        f"/users/{regular_user.id}/active",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Admin or Superadmin privileges required"
