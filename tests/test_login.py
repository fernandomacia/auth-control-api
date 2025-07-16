# tests/test_login.py

import pytest


def test_login_success(client):
    """Test successful login with valid credentials."""
    response = client.post("/login", json={
        "email": "testadmin@example.net",
        "password": "testpassword"
    })

    assert response.status_code == 200
    json = response.json()

    assert json["success"] is True
    assert json["message"] == "Login successful"
    assert "data" in json

    data = json["data"]
    assert "access_token" in data
    assert isinstance(data["access_token"], str) and data["access_token"]
    assert data["user_name"] == "Test Admin"
    assert data["user_role"] == "admin"
    assert data["user_language"] == "en"


@pytest.mark.parametrize("email,password", [
    ("testadmin@example.net", "wrongpassword"),  # incorrect password
    ("nonexistent@example.com", "testpassword"),  # nonexistent user
])
def test_login_failure_cases(client, email, password):
    """Test login failure for incorrect password or non-existent user."""
    response = client.post("/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 401
    json = response.json()

    assert json["success"] is False
    assert json["message"] == "Invalid credentials"
    assert "data" in json
    assert json["data"] == {}


def test_login_inactive_user(client, db):
    """Test login fails if user is inactive."""
    from app.models.user import User

    user = db.query(User).filter(User.email == "testadmin@example.net").first()
    user.is_active = False
    db.commit()

    response = client.post("/login", json={
        "email": "testadmin@example.net",
        "password": "testpassword"
    })

    assert response.status_code == 403
    json = response.json()

    assert json["success"] is False
    assert json["message"] == "Inactive user"
    assert "data" in json
    assert json["data"] == {}

    # Restore user to active state for other tests
    user.is_active = True
    db.commit()
