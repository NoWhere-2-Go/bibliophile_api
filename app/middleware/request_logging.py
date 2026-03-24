import logging
import sys
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # prevent double-logging via root logger

if not logger.handlers:
    _file_handler = logging.FileHandler("app.log")
    _file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    logger.addHandler(_file_handler)

    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    logger.addHandler(_stream_handler)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def _get_route_path(request: Request) -> str:
        route = request.scope.get("route")

        if route is not None and getattr(route, "path", None):
            return route.path

        return request.url.path

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            request_id = getattr(request.state, "request_id", None)
            route_path = self._get_route_path(request)

            logger.exception(
                "request failed | request_id=%s method=%s path=%s status_code=%s duration_ms=%.2f client_ip=%s user_agent=%s",
                request_id or "-",
                request.method,
                route_path,
                500,
                duration_ms,
                client_ip or "-",
                user_agent or "-",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": route_path,
                    "status_code": 500,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": client_ip,
                    "user_agent": user_agent,
                },
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        request_id = getattr(request.state, "request_id", None)
        route_path = self._get_route_path(request)

        logger.info(
            "request completed | request_id=%s method=%s path=%s status_code=%s duration_ms=%.2f client_ip=%s user_agent=%s",
            request_id or "-",
            request.method,
            route_path,
            response.status_code,
            duration_ms,
            client_ip or "-",
            user_agent or "-",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": route_path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": client_ip,
                "user_agent": user_agent,
            },
        )

        return response
