from fastapi import Depends

from app.infrastructure.dependencies.repository_dependencies import get_user_repository
from app.infrastructure.dependencies.service_dependencies import (
    get_hash_service,
    get_jwt_service,
)
from app.usecases.auth.auth_use_cases import AuthUseCases


def get_auth_use_cases(
    user_repository=Depends(get_user_repository),
    jwt_service=Depends(get_jwt_service),
    hash_service=Depends(get_hash_service),
):
    return AuthUseCases(user_repository, jwt_service, hash_service)
