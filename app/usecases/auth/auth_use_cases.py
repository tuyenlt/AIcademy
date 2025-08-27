from app.domain.adapters.hashing import IHashService
from app.domain.adapters.jwt import IJWTService
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.common.exceptions.http_exceptions import (
    NotFoundException,
    BadRequestException,
)
from app.infrastructure.entities.user_entity import UserEntity


class AuthUseCases:
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_service: IJWTService,
        hash_service: IHashService,
    ) -> None:

        self.userRepo = user_repository
        self.jwt_service = jwt_service
        self.hash_service = hash_service

    async def login(self, email: str, password: str) -> bool:
        user = await self.userRepo.find_one_by_filter({"email": email})
        if not user:
            raise NotFoundException("User not found")

        if not self.hash_service.verify(password, user.hashed_password):
            raise BadRequestException("Invalid credentials")

        token_payload = self._create_user_payload(user)
        access_token = self.jwt_service.generate_access_token(token_payload)
        refresh_token = self.jwt_service.generate_refresh_token(token_payload)
        cookie = self._create_cookie_with_refresh_token(refresh_token)
        return {
            "response": {
                "access_token": access_token,
            },
            "cookie": cookie,
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = self.jwt_service.verify_refresh_token(refresh_token)
        if not payload:
            raise BadRequestException("Invalid refresh token")
        user = await self.userRepo.find_one_by_filter({"id": payload["id"]})
        if not user:
            raise NotFoundException("User not found")
        token_payload = self._create_user_payload(user)
        access_token = self.jwt_service.generate_access_token(token_payload)
        return {
            "response": {
                "access_token": access_token,
            },
            "cookie": self._create_cookie_with_refresh_token(refresh_token),
        }

    def _create_user_payload(self, user: UserEntity) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
        }

    def _create_cookie_with_refresh_token(self, refresh_token: str) -> dict:
        return {
            "key": "refresh_token",
            "value": refresh_token,
            "httponly": True,
            "secure": True,
            "samesite": "Strict",
        }
