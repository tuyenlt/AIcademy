from app.infrastructure.repositories.user_repository import UserRepository


def get_user_repository():
    return UserRepository()
