from sqlalchemy import Column, DateTime, Float, ForeignKey, SmallInteger, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class UserQuery(BaseModel):
    __tablename__ = "user_queries"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    query_text = Column(Text, nullable=False)
    retrieved_books = Column(JSONB, nullable=False)
    top_score = Column(Float, nullable=False)
    result_count = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    response_ms = Column(Float)

    # relationships
    user = relationship("User", back_populates="queries")
    feedback = relationship("QueryFeedback", back_populates="query", cascade="all, delete-orphan")

