import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.enums.role import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        # password must follow these rules:
        # between 8-16 characters
        # minimum one upper case character
        # minimum one digit
        if len(value) > 16 or len(value) < 8:
            raise ValueError("Password must be between 8 and 16 characters.")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        return value


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

