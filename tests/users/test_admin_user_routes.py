# tests/users/test_admin_user_routes.py

"""Test suite for admin-only partial updates via PATCH /users/{user_id}."""

import uuid
import pytest
from app.models.user import User
from app.models.user_role import UserRole
from app.models.language import Language
from app.utils.security import get_password_hash, create_access_token


@pytest.fixture
def regular_user(db):
    """
    Create and return a regular (non-admin) user.
    Ensures baseline 'user' role and 'en' language exist.
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


def _admin_token(db):
    """Helper: return a valid admin bearer token."""
    admin = db.query(User).filter_by(email="testadmin@example.net").first()
    return create_access_token(data={"sub": str(admin.id)})


def test_patch_user_is_active_success(client, db, regular_user):
    """
    Admin can toggle target user's active status.
    Expects:
      - 200 OK
      - success = True
      - data.is_active = False
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["is_active"] is False
    assert "updated_fields" in body["data"]
    assert "is_active" in body["data"]["updated_fields"]


def test_patch_user_not_found(client, db):
    """
    Returns 404 when target user does not exist.
    """
    token = _admin_token(db)

    response = client.patch(
        "/users/999999",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": True},
    )

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "User not found"


def test_patch_user_invalid_is_active_type_422(client, db, regular_user):
    """
    Returns 422 when is_active is not boolean (Pydantic type error).
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": "invalid"},
    )

    assert response.status_code == 422


def test_patch_user_forbidden_for_regular_user(client, db, regular_user):
    """
    Regular users cannot access admin-only endpoint.
    Expects:
      - 403 Forbidden
      - detail = "Admin or Superadmin privileges required"
    """
    token = create_access_token(data={"sub": str(regular_user.id)})

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False},
    )

    assert response.status_code == 403
    body = response.json()
    assert body["detail"] == "Admin or Superadmin privileges required"


def test_patch_user_language_success_case_insensitive(client, db, regular_user):
    """
    Updates language using case-insensitive code (e.g., 'ES' or 'es').
    """
    # Ensure ES language exists
    lang_es = db.query(Language).filter_by(code="es").first()
    if not lang_es:
        lang_es = Language(code="es", name="Spanish")
        db.add(lang_es)
        db.commit()

    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"language": "ES"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user_language"] == "es"
    assert "language" in body["data"]["updated_fields"]


def test_patch_user_language_not_found_404(client, db, regular_user):
    """
    Returns 404 when provided language does not exist.
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"language": "xx"},
    )

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Language not found"


def test_patch_user_role_success_case_insensitive(client, db, regular_user):
    """
    Updates role using case-insensitive name (e.g., 'Admin' / 'admin').
    """
    # Ensure 'admin' role exists
    admin_role = db.query(UserRole).filter_by(name="admin").first()
    if not admin_role:
        admin_role = UserRole(name="admin")
        db.add(admin_role)
        db.commit()

    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"role": "Admin"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user_role"].lower() == "admin"
    assert "role" in body["data"]["updated_fields"]


def test_patch_user_role_not_found_404(client, db, regular_user):
    """
    Returns 404 when provided role does not exist.
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"role": "does-not-exist"},
    )

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Role not found"


def test_patch_user_empty_payload_400(client, db, regular_user):
    """
    Returns 400 when payload is empty (no fields provided).
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Empty payload not allowed"


def test_patch_user_unknown_field_422(client, db, regular_user):
    """
    Returns 422 when payload contains unknown/forbidden keys (pydantic extra='forbid').
    """
    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"unknown": True},
    )

    assert response.status_code == 422


def test_patch_user_multiple_fields_success(client, db, regular_user):
    """
    Updates multiple fields in a single PATCH call.
    Verifies response snapshot with updated_fields aggregation.
    """
    # Ensure 'fr' language and 'user' role exist
    lang_fr = db.query(Language).filter_by(code="fr").first()
    if not lang_fr:
        lang_fr = Language(code="fr", name="French")
        db.add(lang_fr)
        db.commit()

    role_user = db.query(UserRole).filter_by(name="user").first()
    if not role_user:
        role_user = UserRole(name="user")
        db.add(role_user)
        db.commit()

    token = _admin_token(db)

    response = client.patch(
        f"/users/{regular_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False, "language": "FR", "role": "user"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["is_active"] is False
    assert body["data"]["user_language"] == "fr"
    assert body["data"]["user_role"] == "user"
    # Ensure updated_fields contains all three keys (order not guaranteed)
    fields = set(body["data"]["updated_fields"])
    assert {"is_active", "language", "role"} <= fields
