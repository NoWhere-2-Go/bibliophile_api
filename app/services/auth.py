import os
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import generate_session_token, hash_session_token, verify_password
from app.models.session import Session as UserSession
from app.models.user import User
from app.schemas.session import SessionCreate


def create_session(
    db: Session,
    session_in: SessionCreate,
    ip_address: str,
    user_agent: str,
) -> tuple[type[User], str, datetime]:
    user = db.query(User).filter(User.email == session_in.email).first()
    if not user or not verify_password(session_in.password, str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=int(os.getenv("SESSION_TTL_HOURS", "1")))

    # rotate active sessions: any non-expired token is ended now.
    db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.expires_at > now,
    ).update({UserSession.expires_at: now}, synchronize_session=False)

    token = generate_session_token()
    new_session = UserSession(
        id=uuid.uuid4(),
        user_id=user.id,
        token_hash=hash_session_token(token),
        created_at=now,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(new_session)
    db.commit()

    return user, token, expires_at

