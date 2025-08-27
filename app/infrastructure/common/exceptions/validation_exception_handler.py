from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def extract_validation_errors(exc: RequestValidationError):
    return [
        {
            "field": error["loc"][-1],
            "message": error["msg"],
        }
        for error in exc.errors()
    ]


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": extract_validation_errors(exc),
        },
    )
