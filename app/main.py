from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn
from infrastructure.common.middlewares.jwt_middleware import JWTMiddleware
from infrastructure.common.middlewares.response_interceptor import (
    ResponseInterceptorMiddleware,
)
from infrastructure.controllers.controllers import api_router
from infrastructure.configs.app_config import app_settings
from infrastructure.common.exceptions.validation_exception_handler import (
    validation_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.app_name,
        description="A FastAPI application following Clean Architecture principles",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_version="3.1.0",
    )

    app.openapi_tags = [
        {
            "name": "auth",
            "description": "Authentication operations",
        },
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=app_settings.cors_credentials,
        allow_methods=app_settings.cors_methods,
        allow_headers=app_settings.cors_headers,
    )
    app.add_middleware(JWTMiddleware)
    app.add_middleware(ResponseInterceptorMiddleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.include_router(api_router)

    return app


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app_settings.app_name,
        version="1.0.0",
        description="A FastAPI application following Clean Architecture principles",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = create_app()
app.openapi = custom_openapi


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {app_settings.app_name}",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1",
    }


if __name__ == "__main__":
    if app_settings.app_environment == "production":
        uvicorn.run(
            "main:app",
            host=app_settings.server_host,
            port=app_settings.server_port,
            reload=False,
            log_level=app_settings.server_log_level,
        )
    else:
        uvicorn.run(
            "main:app",
            host=app_settings.server_host,
            port=app_settings.server_port,
            reload=True,
            log_level=app_settings.server_log_level,
            reload_dirs=["."],
        )
