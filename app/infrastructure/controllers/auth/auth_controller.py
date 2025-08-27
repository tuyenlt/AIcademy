from fastapi import APIRouter, Depends, Response

from app.infrastructure.controllers.auth.dto.login_dto import LoginDto
from app.infrastructure.dependencies.use_case_dependencies import get_auth_use_cases
from app.usecases.auth.auth_use_cases import AuthUseCases
from app.infrastructure.controllers.auth.dto.auth_response_dto import AuthResponseDto

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponseDto)
async def login(
    body: LoginDto,
    res: Response,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    result = await auth_use_cases.login(body.email, body.password)
    print(result["cookie"])
    res.set_cookie(**result["cookie"])
    return result["response"]
