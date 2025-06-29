# app/models/language.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)  # e.g. 'en', 'es', 'fr'
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="language")
