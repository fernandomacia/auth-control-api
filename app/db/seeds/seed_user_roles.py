# app/db/seeds/seed_user_roles.py

from sqlalchemy.orm import Session
from app.models.user_role import UserRole


def seed_user_roles(session: Session) -> None:
    roles = [
        {"name": "user", "description": "Standard user"},
        {"name": "admin", "description": "Administrator"},
        {"name": "superadmin", "description": "Super administrator"},
    ]
    for role in roles:
        exists = session.query(UserRole).filter_by(name=role["name"]).first()
        if not exists:
            session.add(UserRole(**role))
