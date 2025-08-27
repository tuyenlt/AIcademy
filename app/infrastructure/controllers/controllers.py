"""
Base Router Module

This module serves as the main entry point for all API routes.
It imports and registers all route modules in the application.
"""

from fastapi import APIRouter

# Import other route modules here as you create them

from app.infrastructure.controllers.auth.auth_controller import router as auth_router

# from app.interfaces.product_controller import router as product_router


def create_api_router() -> APIRouter:
    # Create the main API router
    api_router = APIRouter(prefix="/api/v1")

    # Register all route modules
    api_router.include_router(auth_router)
    return api_router


# Create the main router instance
api_router = create_api_router()
