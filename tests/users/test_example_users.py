import pytest
from app.models.user import User
from app.models.language import Language
from app.models.user_role import UserRole
from app.utils.security import get_password_hash


@pytest.fixture
def insert_example_users(db):
    """
    Insert static users into the test database for the /users/examples endpoint.
    """
    # Crear lenguajes
    langs = {
        "en": Language(code="en", name="English"),
        "es": Language(code="es", name="Spanish"),
        "fr": Language(code="fr", name="French")
    }
    for lang in langs.values():
        if not db.query(Language).filter_by(code=lang.code).first():
            db.add(lang)

    # Crear roles
    roles = {
        "User": UserRole(name="User", description="Standard user"),
        "Admin": UserRole(name="Admin", description="Administrator"),
        "SuperAdmin": UserRole(name="SuperAdmin", description="Super administrator")
    }
    for role in roles.values():
        if not db.query(UserRole).filter_by(name=role.name).first():
            db.add(role)

    db.commit()

    # Crear usuarios
    users_data = [
        ("user@example.net", "user", "es", "User"),
        ("admin@example.net", "admin", "en", "Admin"),
        ("superadmin@example.net", "superadmin", "fr", "SuperAdmin")
    ]

    for email, password, lang_code, role_name in users_data:
        if not db.query(User).filter_by(email=email).first():
            user = User(
                name=email.split("@")[0],
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                language_id=db.query(Language).filter_by(code=lang_code).first().id,
                role_id=db.query(UserRole).filter_by(name=role_name).first().id
            )
            db.add(user)

    db.commit()


def test_get_example_users_success(client, db, insert_example_users):
    """
    Test retrieval of static example users from the database.
    """
    response = client.get("/users/examples")
    assert response.status_code == 200

    json = response.json()
    assert json["success"] is True
    assert json["message"] == "Example users retrieved successfully"
    assert isinstance(json["data"], list)
    assert len(json["data"]) == 3

    expected_passwords = {
        "user@example.net": "user",
        "admin@example.net": "admin",
        "superadmin@example.net": "superadmin",
    }

    expected_roles = {"User", "Admin", "SuperAdmin"}
    expected_languages = {"en", "es", "fr"}

    for user_data in json["data"]:
        email = user_data["name"]
        assert email in expected_passwords
        assert user_data["password"] == expected_passwords[email]
        assert user_data["role"] in expected_roles
        assert user_data["language"] in expected_languages
