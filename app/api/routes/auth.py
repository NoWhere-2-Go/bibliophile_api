from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.user import UserResponse
from app.services.auth import create_session

router = APIRouter(tags=["session"], prefix="/auth")


@router.post("/session", response_model=SessionResponse, status_code=200)
async def create_session_endpoint(
    request: Request,
    session_in: SessionCreate,
    db: Session = Depends(get_db),
) -> SessionResponse:
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    user, token, expires_at = create_session(db, session_in, ip_address, user_agent)
    return SessionResponse(
        token=token,
        expires_at=expires_at,
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            username=user.username,
            role=user.role.name,
        ),
    )
