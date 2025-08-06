import uvicorn
from fastapi import FastAPI
from structlog import get_logger
from starlette.middleware.cors import CORSMiddleware

# Middleware & Router
from api.middleware.ratelimiter import RateLimitMiddleware
from api.middleware.logger import LoggerMiddleware
from api.router import router as api_router

# Core configuration & logging
from core.logging import configure_logger
from core.config import get_app_settings


def create_app() -> FastAPI:
    # Load application settings
    settings = get_app_settings()

    # Init logger
    logger = get_logger()
    logger.info(f"Starting app with environment: {settings.app_env}")

    # Initialize FastAPI instance
    application = FastAPI(**settings.fastapi_kwargs)

    # Enable CORS for frontend access
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middlewares
    application.add_middleware(RateLimitMiddleware)
    application.add_middleware(LoggerMiddleware)

    # Register API routes
    application.include_router(api_router, prefix="/api")

    # Configure structured logging
    configure_logger()

    return application


app = create_app()

# Run the app (development entrypoint)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
