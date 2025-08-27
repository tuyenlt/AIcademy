from app.infrastructure.services.hash_service import HashService
from app.infrastructure.services.jwt_service import JWTService


def get_hash_service():
    return HashService()


def get_jwt_service():
    return JWTService()
