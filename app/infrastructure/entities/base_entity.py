from datetime import datetime
from sqlalchemy import Column, String, DateTime, text
from app.infrastructure.configs.db_config import Base


class BaseEntity(Base):
    __abstract__ = True

    id = Column(String(36), primary_key=True, server_default=text("UUID()"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    deleted_at = Column(DateTime, nullable=True)
