from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_role import UserRole
from app.models.language import Language
from app.utils.security import get_password_hash

def seed_example_users(session: Session) -> None:
    examples = [
        {"name": "Admin", "email": "admin@example.net", "role": "admin", "language": "en", "password": "admin"},
        {"name": "Superadmin", "email": "superadmin@example.net", "role": "superadmin", "language": "es", "password": "superadmin"},
        {"name": "User", "email": "user@example.net", "role": "user", "language": "fr", "password": "user"},
    ]

    for user_data in examples:
        if session.query(User).filter_by(email=user_data["email"]).first():
            continue

        role = session.query(UserRole).filter_by(name=user_data["role"]).first()
        if not role:
            raise ValueError(f"Role '{user_data['role']}' not found. Run seed_user_roles first.")

        lang = session.query(Language).filter_by(code=user_data["language"]).first()
        if not lang:
            raise ValueError(f"Language '{user_data['language']}' not found. Run seed_languages first.")

        hashed = get_password_hash(user_data["password"])

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hashed,
            role_id=role.id,
            language_id=lang.id,
            is_active=True
        )

        session.add(user)

