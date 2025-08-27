import time
from typing import Any, Dict

from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

from app.domain.adapters.jwt import IJWTService
from app.infrastructure.common.exceptions.http_exceptions import UnauthorizedException
from app.infrastructure.configs import app_config


class JWTService(IJWTService):
    def __init__(self) -> None:
        self.settings = app_config.app_settings
        self.alg = "HS256"

    def _now_ts(self) -> int:
        return int(time.time())

    def generate_access_token(self, payload: Dict[str, Any]) -> str:
        now = self._now_ts()
        exp = now + int(self.settings.jwt_access_expires_seconds)
        data = {**payload, "exp": exp, "iat": now, "type": "access"}
        token = jwt.encode(data, self.settings.jwt_access_secret, algorithm=self.alg)
        return token

    def generate_refresh_token(self, payload: Dict[str, Any]) -> str:
        now = self._now_ts()
        exp = now + int(self.settings.jwt_refresh_expires_seconds)
        data = {**payload, "exp": exp, "iat": now, "type": "refresh"}
        token = jwt.encode(data, self.settings.jwt_refresh_secret, algorithm=self.alg)
        return token

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_access_secret,
                algorithms=[self.alg],
            )
            return payload
        except ExpiredSignatureError:
            raise UnauthorizedException("access token expired")
        except JWTError as exc:
            raise UnauthorizedException(f"invalid access token: {exc}")

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_refresh_secret,
                algorithms=[self.alg],
            )
            return payload
        except ExpiredSignatureError:
            raise UnauthorizedException("refresh token expired")
        except JWTError as exc:
            raise UnauthorizedException(f"invalid refresh token: {exc}")
