from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Optional

from infrastructure.common.exceptions.http_exceptions import UnauthorizedException
from infrastructure.services.jwt_service import JWTService


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        jwt_service: Optional[JWTService] = None,
        excluded_paths: Optional[List[str]] = None,
    ):
        super().__init__(app)
        self.jwt_service = jwt_service or JWTService()
        self.excluded_paths = excluded_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/",
            "/api/v1/health",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh-token",
        ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        token = self.extract_token(request.headers.get("Authorization"))
        if not token:
            raise UnauthorizedException("Missing token")

        payload = self.jwt_service.verify_access_token(token)

        request.state.user = payload.get("user")
        if not request.state.user:
            raise UnauthorizedException("Invalid token payload")

        response = await call_next(request)
        return response

    def extract_token(self, auth_header: str) -> str:
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedException("Invalid or missing Authorization header")
        return auth_header.split(" ")[1]
