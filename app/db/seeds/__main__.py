"""
CLI runner for seeding.

Usage:
  python -m app.db.seeds
"""

import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.db.seeds import run_seeds


def main() -> None:
    """
    Opens a DB session, runs seeds, and closes the session.
    Controlled via `SEED_INCLUDE_EXAMPLES` env var (default: true).
    """
    include_examples = os.getenv("SEED_INCLUDE_EXAMPLES", "true").lower() in {"1", "true", "yes"}

    db: Session = SessionLocal()
    try:
        run_seeds(db, include_examples=include_examples)
    finally:
        db.close()


if __name__ == "__main__":
    main()
