from sqlalchemy import Column, DateTime, Enum, Text
from sqlalchemy.orm import relationship

from app.enums.role import RoleEnum
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(Text, nullable=False, unique=True)
    username = Column(Text, unique=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    modified_at = Column(DateTime(timezone=True), nullable=False)
    role = Column(Enum(RoleEnum, values_callable=lambda x: [e.name.lower() for e in x]), nullable=False, default=RoleEnum.USER)

    # relationships
    queries = relationship("UserQuery", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

