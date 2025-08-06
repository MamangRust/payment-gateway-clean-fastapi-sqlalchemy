import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog import get_logger

logger = get_logger()

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "Unknown")

        ip_address = (
            request.headers.get("x-forwarded-for")
            or request.headers.get("x-real-ip")
            or (request.client.host if request.client else "127.0.0.1")
        )

        current_user = getattr(request.state, "current_user", None)
        user_id = getattr(current_user, "user_id", None)
        username = getattr(current_user, "username", None)

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        status_code = response.status_code

        logger.info(
            "📝 HTTP Request",
            method=method,
            path=path,
            status=status_code,
            duration=f"{process_time:.2f}ms",
            ip=ip_address,
            user_agent=user_agent,
            user_id=user_id,
            username=username,
        )

        return response
