# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

