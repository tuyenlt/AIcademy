from pydantic import BaseModel


class AuthResponseDto(BaseModel):
    access_token: str
