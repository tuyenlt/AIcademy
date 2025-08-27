# app/infrastructure/middlewares/response_interceptor.py
import json
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request


class ResponseInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = int((time.perf_counter() - start) * 1000)

        # Only wrap JSON responses
        if response.headers.get("content-type") == "application/json":
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            try:
                parsed_body = json.loads(body.decode())
            except Exception:
                parsed_body = body.decode()

            return JSONResponse(
                {
                    "success": response.status_code < 400,
                    "status_code": response.status_code,
                    "data": parsed_body,
                    "duration": f"{duration}ms",
                },
                status_code=response.status_code,
            )

        return response
