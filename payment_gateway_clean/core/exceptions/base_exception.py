from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

class BaseInternalException(Exception):
    _status_code = 0
    _message = ""


    def __init__(
        self,
        status_code: int | None = None,
        message: str | None = None,
        errors: list[str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors

    def get_status_code(self) -> int:
        return self.status_code or self._status_code

    def get_message(self) -> str:
        return self.message or self._message

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls._status_code,
            content={
                "status": "error",
                "status_code": cls._status_code,
                "type": cls.__name__,
                "message": cls._message,
            },
        )