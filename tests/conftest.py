# tests/conftest.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.main import app
from fastapi.testclient import TestClient
from app.models.user import User
from app.models.user_role import UserRole
from app.models.language import Language
from app.utils.security import get_password_hash
from app.core.database import get_db

# Ensure the test database directory exists
os.makedirs("tests/databases", exist_ok=True)

# Temporary SQLite test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/databases/test.db"  # You can switch to ":memory:" if you want
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed required data
    role = UserRole(name="admin")
    lang = Language(code="en", name="English")
    db.add_all([role, lang])
    db.commit()

    # Create a test user
    user = User(
        name="Test Admin",
        email="testadmin@example.net",
        hashed_password=get_password_hash("testpassword"),
        role_id=role.id,
        language_id=lang.id,
        is_active=True
    )
    db.add(user)
    db.commit()

    yield db
    db.close()


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)