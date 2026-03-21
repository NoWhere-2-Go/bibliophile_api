import uuid
from datetime import datetime, timezone

import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from setuptools.command.py36compat import sdist_add_defaults
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import data_models  # noqa: F401 – registers all models with SQLAlchemy
from data_models.User import User
from database import get_db
from schemas.user import UserCreate, UserResponse

app = FastAPI()


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/health/db")
async def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc


@app.post("/user", response_model=UserResponse, status_code=201)
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=409, detail="Username already taken")

    now = datetime.now(timezone.utc)
    new_user = User(
        id=uuid.uuid4(),
        email=user_in.email,
        username=user_in.username,
        password_hash=hash_password(user_in.password),
        created_at=now,
        modified_at=now,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists")

    return new_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


