from pydantic import BaseModel, EmailStr, Field

from infrastructure.common.constant.validation_constant import (
    MAX_FULL_NAME,
    MAX_PASSWORD_LENGTH,
    MIN_FULL_NAME,
    MIN_PASSWORD_LENGTH,
)


class RegisterDto(BaseModel):
    email: EmailStr = Field(
        ..., description="User's email address", examples=["john.doe@example.com"]
    )
    full_name: str = Field(
        ...,
        min_length=MIN_FULL_NAME,
        max_length=MAX_FULL_NAME,
        description="User's full name",
        examples=["John Doe"],
    )
    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        description="User's password",
        examples=["SecurePassword123!"],
    )
