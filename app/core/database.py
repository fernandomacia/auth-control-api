# app/core/database.py

"""Database configuration and session management utilities."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Raise error if DATABASE_URL is not defined
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL environment variable is not set.")

# Initialize SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a SQLAlchemy session.

    Yields:
        Session: Active database session.
    
    Ensures the session is properly closed after usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()