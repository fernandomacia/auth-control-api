# app/models/user_role.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", back_populates="role")