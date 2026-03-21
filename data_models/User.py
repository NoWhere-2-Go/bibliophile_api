from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import relationship

from data_models.BaseModel import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(Text, nullable=False, unique=True)
    username = Column(Text, unique=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    modified_at = Column(DateTime(timezone=True), nullable=False)
    role = Column(String(50), nullable=False, default="user")

    # relationships
    queries = relationship("UserQuery", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
