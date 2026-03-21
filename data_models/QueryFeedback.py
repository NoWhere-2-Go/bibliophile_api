from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from data_models.BaseModel import BaseModel


class QueryFeedback(BaseModel):
    __tablename__ = "query_feedback"

    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)

    # relationships
    query = relationship("UserQuery", back_populates="feedback")
