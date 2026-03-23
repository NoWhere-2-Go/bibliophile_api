from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users import create_user

router = APIRouter(tags=["users"])


@router.post("/user", response_model=UserResponse, status_code=201)
async def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return create_user(db, user_in)

