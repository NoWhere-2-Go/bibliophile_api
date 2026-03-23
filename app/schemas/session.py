from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


class SessionCreate(BaseModel):
	email: EmailStr
	password: str


class SessionResponse(BaseModel):
	token: str
	expires_at: datetime
	user: UserResponse


