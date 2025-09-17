from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application settings
    app_environment: str = "development"
    app_url: str = "http://localhost:8000"
    app_name: str = "Clean Architecture FastAPI Template"
    api_key: str = "default-api-key"

    # JWT settings
    jwt_access_secret: str = "default-access-secret"
    jwt_refresh_secret: str = "default-refresh-secret"
    jwt_access_expires_seconds: int = 3600
    jwt_refresh_expires_seconds: int = 604800

    # Database settings
    database_name: str = "aicademy_db"
    database_user: str = "admin"
    database_password: str = "password"
    database_host: str = "localhost"
    database_port: int = 3306
    database_schema: str = "public"

    # CORS settings
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    cors_credentials: bool = True

    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_reload: bool = True
    server_log_level: str = "info"

    class Config:
        env_file = ".env"


app_settings = Settings()
