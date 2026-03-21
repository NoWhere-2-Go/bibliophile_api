import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from enums.role import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_max_length(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be 72 bytes or fewer (bcrypt limit).")
        return v


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    role: RoleEnum
    created_at: datetime

    model_config = {"from_attributes": True}

