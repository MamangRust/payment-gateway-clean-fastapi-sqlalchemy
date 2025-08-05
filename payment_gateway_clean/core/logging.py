import logging
import structlog
from structlog.typing import EventDict, Processor
from core.config import get_app_settings

__all__ = ["configure_logger"]

DEFAULT_LOGGER_NAME = "payment-gateway-api"


def rename_event_key(_: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
    """Rename 'event' key to 'message' for consistency in JSON logs."""
    event_dict["message"] = event_dict.pop("event", "")
    return event_dict


def drop_color_message_key(_: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
    """Drop unnecessary 'color_message' key from uvicorn logs."""
    event_dict.pop("color_message", None)
    return event_dict


def configure_logger(json_logs: bool = False) -> None:
    """
    Configure the root logger using structlog with support for structured JSON logs.
    """
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        timestamper,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        shared_processors += [
            rename_event_key,
            structlog.processors.format_exc_info,
        ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    log_renderer = (
        structlog.processors.JSONRenderer()
        if json_logs
        else structlog.dev.ConsoleRenderer()
    )

    _configure_root_logger(shared_processors, log_renderer)


def _configure_root_logger(
    shared_processors: list[Processor], log_renderer: structlog.types.Processor
) -> None:
    """
    Sets up the root Python logger with structlog formatting.
    """
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(handler)

    settings = get_app_settings()
    root_logger.setLevel(settings.logging_level)

    logging.getLogger("asyncio").setLevel(logging.WARNING)

    for log_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(log_name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
