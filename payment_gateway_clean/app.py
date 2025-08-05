import uvicorn

from fastapi import FastAPI
from structlog import get_logger
from starlette.middleware.cors import CORSMiddleware

from api.middleware.ratelimiter import RateLimitMiddleware
from api.router import router as api_router
from core.logging import configure_logger

from core.config import get_app_settings


def create_app() -> FastAPI:
    settings = get_app_settings()

    logger = get_logger()

    logger.info(f"Starting app with environment: {settings.app_env}")

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RateLimitMiddleware)

    application.include_router(api_router, prefix="/api")

    configure_logger()

    return application


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)