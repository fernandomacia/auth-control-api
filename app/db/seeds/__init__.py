"""
Public seeding API.

- Exposes `run_seeds(db, include_examples=True)` to seed dictionaries and example data.
- Must be idempotent; safe to run multiple times.
"""

from sqlalchemy.orm import Session

from .seed_user_roles import seed_user_roles
from .seed_languages import seed_languages
from .seed_example_users import seed_example_users

__all__ = ["run_seeds", "seed_user_roles", "seed_languages", "seed_example_users"]


def run_seeds(db: Session, *, include_examples: bool = True) -> None:
    """
    Executes seed steps in a controlled order with transactions.

    - Commits after core dictionaries (roles, languages).
    - Optionally seeds example users and commits again.
    - Rolls back on failure to avoid partial writes.

    :param db: SQLAlchemy Session bound to your engine.
    :param include_examples: Whether to include example users.
    """
    try:
        # Dictionaries (idempotent)
        seed_user_roles(db)
        seed_languages(db)
        db.commit()

        # Example/sample data (idempotent)
        if include_examples:
            seed_example_users(db)
            db.commit()
    except Exception:
        db.rollback()
        raise