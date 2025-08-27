from pydantic import BaseModel, EmailStr, Field


class LoginDto(BaseModel):
    email: EmailStr = Field(..., examples=["admin@aicademy.com"])
    password: str = Field(..., min_length=6, examples=["admin123"])
