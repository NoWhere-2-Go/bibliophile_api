from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True)
