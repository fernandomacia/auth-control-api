# tests/users/test_example_users.py

"""Test suite for the /users/examples endpoint."""

import pytest
from app.models.user import User
from app.models.language import Language
from app.models.user_role import UserRole
from app.utils.security import get_password_hash


@pytest.fixture
def insert_example_users(db):
    """
    Seed the database with example users, roles, and languages for testing.

    Args:
        db (Session): SQLAlchemy test database session.
    """
    # Seed languages
    languages = {
        "en": Language(code="en", name="English"),
        "es": Language(code="es", name="Spanish"),
        "fr": Language(code="fr", name="French"),
    }
    for lang in languages.values():
        if not db.query(Language).filter_by(code=lang.code).first():
            db.add(lang)

    # Seed roles
    roles = {
        "User": UserRole(name="User", description="Standard user"),
        "Admin": UserRole(name="Admin", description="Administrator"),
        "SuperAdmin": UserRole(name="SuperAdmin", description="Super administrator"),
    }
    for role in roles.values():
        if not db.query(UserRole).filter_by(name=role.name).first():
            db.add(role)

    db.commit()

    # Seed users
    users_data = [
        ("user@example.net", "user", "es", "User"),
        ("admin@example.net", "admin", "en", "Admin"),
        ("superadmin@example.net", "superadmin", "fr", "SuperAdmin"),
    ]
    for email, password, lang_code, role_name in users_data:
        if not db.query(User).filter_by(email=email).first():
            user = User(
                name=email.split("@")[0],
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                language_id=db.query(Language).filter_by(code=lang_code).first().id,
                role_id=db.query(UserRole).filter_by(name=role_name).first().id,
            )
            db.add(user)

    db.commit()


def test_get_example_users_success(client, db, insert_example_users):
    """
    Verify that the /users/examples endpoint returns correct data.

    Asserts:
        - HTTP 200 response
        - Response payload includes 3 static users
        - User attributes match expected values
    """
    response = client.get("/users/examples")
    assert response.status_code == 200

    json = response.json()
    assert json["success"] is True
    assert json["message"] == "Example users retrieved successfully"
    assert isinstance(json["data"], list)
    assert len(json["data"]) == 3

    expected_passwords = {
        "user": "userPassword",
        "admin": "adminPassword",
        "superadmin": "superadminPassword",
    }
    expected_roles = {"User", "Admin", "SuperAdmin"}
    expected_languages = {"en", "es", "fr"}

    for user_data in json["data"]:
        user_name = user_data["user_name"]
        assert user_name in expected_passwords
        assert user_data["user_email"] == f"{user_name}@example.net"
        assert user_data["user_password"] == expected_passwords[user_name]
        assert user_data["user_role"] in expected_roles
        assert user_data["user_language"] in expected_languages
