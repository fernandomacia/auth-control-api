# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.user_role import UserRole
from app.models.language import Language


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    role = relationship("UserRole", back_populates="users")
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    language = relationship("Language", back_populates="users")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
