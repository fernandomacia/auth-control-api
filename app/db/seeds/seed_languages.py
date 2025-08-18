# app/db/seeds/seed_languages.py

from sqlalchemy.orm import Session
from app.models.language import Language


def seed_languages(session: Session) -> None:
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Español"},
        {"code": "fr", "name": "Français"},
    ]
    for lang in languages:
        exists = session.query(Language).filter_by(code=lang["code"]).first()
        if not exists:
            session.add(Language(**lang))