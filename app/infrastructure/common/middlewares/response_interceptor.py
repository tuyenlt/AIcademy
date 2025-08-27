import json
import time
import logging
import traceback
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, StreamingResponse


logger = logging.getLogger("app.middleware")


class ResponseInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        try:
            response = await call_next(request)
        except HTTPException as exc:
            duration = int((time.perf_counter() - start) * 1000)
            return JSONResponse(
                {
                    "success": False,
                    "status_code": exc.status_code,
                    "error": exc.detail,
                    "duration": f"{duration}ms",
                },
                status_code=exc.status_code,
            )
        except RequestValidationError as exc:
            duration = int((time.perf_counter() - start) * 1000)
            return JSONResponse(
                {
                    "success": False,
                    "status_code": 400,
                    "error": exc.errors(),
                    "duration": f"{duration}ms",
                },
                status_code=400,
            )
        except Exception:
            duration = int((time.perf_counter() - start) * 1000)
            logger.error(
                f"Unhandled server error in {request.method} {request.url} "
                f"duration={duration}ms\n{traceback.format_exc()}"
            )
            return JSONResponse(
                {
                    "success": False,
                    "status_code": 500,
                    "error": "Internal server error",
                    "duration": f"{duration}ms",
                },
                status_code=500,
            )

        duration = int((time.perf_counter() - start) * 1000)

        # Bỏ qua docs & streaming response
        if isinstance(response, StreamingResponse) or request.url.path in [
            "/docs",
            "/redoc",
            "/openapi.json",
        ]:
            return response

        # Xử lý JSON body
        try:
            body = [chunk async for chunk in response.body_iterator]
            raw_body = b"".join(body)

            try:
                parsed_body = json.loads(raw_body.decode()) if raw_body else {}
            except json.JSONDecodeError:
                parsed_body = {"message": raw_body.decode()}

            new_response = JSONResponse(
                {
                    "success": response.status_code < 400,
                    "status_code": (
                        400 if response.status_code == 422 else response.status_code
                    ),
                    "data": parsed_body,
                    "duration": f"{duration}ms",
                },
                status_code=(
                    400 if response.status_code == 422 else response.status_code
                ),
            )

            # Copy headers (trừ content-length)
            for k, v in response.headers.items():
                if k.lower() != "content-length":
                    new_response.headers[k] = v

            logger.info(
                f"{request.method} {request.url.path} "
                f"completed_in={duration}ms status={response.status_code}"
            )
            return new_response

        except Exception as e:
            logger.error(f"Response interceptor error: {e}")
            return response
