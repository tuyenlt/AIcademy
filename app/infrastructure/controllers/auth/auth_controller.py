from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.infrastructure.controllers.auth.dto.login_dto import LoginDto
from app.infrastructure.dependencies.use_case_dependencies import get_auth_use_cases
from app.usecases.auth.auth_use_cases import AuthUseCases
from app.infrastructure.controllers.auth.dto.auth_response_dto import AuthResponseDto
from infrastructure.common.exceptions.http_exceptions import UnauthorizedException
from infrastructure.controllers.auth.dto.register_dto import RegisterDto

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponseDto)
async def login(
    body: LoginDto,
    res: Response,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    result = await auth_use_cases.login(body.email, body.password)
    res.set_cookie(**result["cookie"])
    return result["response"]


@router.post("/register", response_model=AuthResponseDto)
async def register(
    body: RegisterDto,
    res: Response,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    result = await auth_use_cases.register(body)
    res.set_cookie(**result["cookie"])
    return result["response"]


@router.post("/refresh-token", response_model=AuthResponseDto)
async def refresh_token(
    request: Request,
    res: Response,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    refresh_token = request.cookies.get("refresh_token")
    result = await auth_use_cases.refresh_token(refresh_token)
    res.set_cookie(**result["cookie"])
    return result["response"]


@router.delete(
    "/logout",
    summary="Logout user",
    description="Logout the currently authenticated user and invalidate refresh token",
)
async def logout(
    res: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    result = await auth_use_cases.logout(request.state.user["id"])
    res.set_cookie(**result["cookie"])
    return result["response"]


@router.get("/is-authenticated", summary="Check authentication status")
async def is_authenticated(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    user = request.state.user
    if not user:
        raise UnauthorizedException("User not authenticated")
    return user
