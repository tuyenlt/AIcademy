from app.domain.adapters.hashing import IHashService
from app.domain.adapters.jwt import IJWTService
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.common.exceptions.http_exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
)
from app.infrastructure.entities.user_entity import UserEntity
from infrastructure.controllers.auth.dto.register_dto import RegisterDto


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
        refresh_token = await self._gen_user_refresh_token(token_payload)
        cookie = self._create_cookie_with_refresh_token(refresh_token)
        return {
            "response": {
                "access_token": access_token,
            },
            "cookie": cookie,
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        if not refresh_token:
            raise UnauthorizedException("Missing refresh token")
        payload = self.jwt_service.verify_refresh_token(refresh_token)
        if not payload:
            raise BadRequestException("Invalid refresh token")
        user = await self.userRepo.find_one_by_filter({"id": payload["user"]["id"]})
        if not user:
            raise NotFoundException("User not found")
        is_refresh_token_valid = self.hash_service.verify(
            refresh_token, user.hashed_refresh_token
        )
        if not is_refresh_token_valid:
            raise BadRequestException("Invalid refresh token")
        token_payload = self._create_user_payload(user)
        new_access_token = self.jwt_service.generate_access_token(token_payload)
        new_refresh_token = await self._gen_user_refresh_token(token_payload)
        return {
            "response": {
                "access_token": new_access_token,
            },
            "cookie": self._create_cookie_with_refresh_token(new_refresh_token),
        }

    async def logout(self, userId: str) -> dict:
        await self._remove_user_refresh_token(userId)
        cookie = {
            "key": "refresh_token",
            "value": "",
            "httponly": True,
            "secure": True,
            "samesite": "Strict",
            "max_age": 0,
        }
        return {
            "response": {
                "message": "Logged out successfully",
            },
            "cookie": cookie,
        }

    async def register(self, body: RegisterDto):
        existing_user = await self.userRepo.find_one_by_filter({"email": body.email})
        if existing_user:
            raise BadRequestException("Email already in use")
        hashed_password = self.hash_service.hash(body.password)
        user_data = {
            "email": body.email,
            "full_name": body.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_admin": False,
        }
        user = await self.userRepo.create(user_data)
        token_payload = self._create_user_payload(user)
        access_token = self.jwt_service.generate_access_token(token_payload)
        refresh_token = await self._gen_user_refresh_token(token_payload)
        cookie = self._create_cookie_with_refresh_token(refresh_token)
        return {
            "response": {
                "access_token": access_token,
            },
            "cookie": cookie,
        }

    async def _remove_user_refresh_token(self, userId: str) -> None:
        await self.userRepo.update(userId, {"hashed_refresh_token": None})

    async def _gen_user_refresh_token(self, payload: dict) -> None:
        refresh_token = self.jwt_service.generate_refresh_token(payload)
        await self.userRepo.update(
            payload["user"]["id"],
            {"hashed_refresh_token": self.hash_service.hash(refresh_token)},
        )
        return refresh_token

    def _create_user_payload(self, user: UserEntity) -> dict:
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "avatar_url": user.avatar_url,
                "is_admin": user.is_admin,
            }
        }

    def _create_cookie_with_refresh_token(self, refresh_token: str) -> dict:
        return {
            "key": "refresh_token",
            "value": refresh_token,
            "httponly": True,
            "secure": True,
            "samesite": "Strict",
        }
