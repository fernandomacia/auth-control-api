# app/core/database.py

"""Database configuration with lazy engine/session initialization."""

import os
from typing import Generator, Optional

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- Lazy-initialized globals (private) ---
_ENGINE: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None

# Declarative base for ORM models
Base = declarative_base()


def _get_database_url() -> str:
    """
    Get DATABASE_URL from environment.
    Raise 503 instead of ImportError to avoid crashing at import time.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not configured (missing DATABASE_URL)."
        )
    return url


def _init_engine() -> None:
    """
    Initialize SQLAlchemy engine and sessionmaker once (idempotent).
    """
    global _ENGINE, _SessionLocal
    if _ENGINE is not None and _SessionLocal is not None:
        return

    database_url = _get_database_url()
    _ENGINE = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        future=True,
    )
    _SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_ENGINE,
        future=True,
    )


class _SessionFactory:
    """
    Public, callable session factory compatible with `db = SessionLocal()`.
    Lazily ensures the underlying sessionmaker is initialized.
    """
    def __call__(self) -> Session:
        _init_engine()
        assert _SessionLocal is not None  # for type-checkers
        return _SessionLocal()


# Public callable compatible with `sessionmaker` usage pattern.
SessionLocal = _SessionFactory()


def get_engine() -> Engine:
    """
    Return the initialized SQLAlchemy engine (lazy).
    """
    _init_engine()
    assert _ENGINE is not None
    return _ENGINE


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a DB session with proper cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "SessionLocal", "get_engine", "get_db"]
