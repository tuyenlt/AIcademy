from sqlalchemy import Column, String, Boolean
from app.infrastructure.entities.base_entity import BaseEntity


class UserEntity(BaseEntity):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    hashed_refresh_token = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
