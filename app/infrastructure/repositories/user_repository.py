from app.infrastructure.entities.user_entity import UserEntity
from app.infrastructure.repositories.base_crud_repository import BaseCrudRepository


class UserRepository(BaseCrudRepository):
    """User repository for managing user-related database operations."""

    def __init__(self):
        super().__init__(UserEntity)
