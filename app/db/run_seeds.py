from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.db.seeds import seed_user_roles, seed_languages, seed_example_users


def main():
    db: Session = SessionLocal()
    seed_user_roles(db)
    seed_languages(db)
    db.commit()

    seed_example_users(db)
    db.commit()

    db.close()


if __name__ == "__main__":
    main()
