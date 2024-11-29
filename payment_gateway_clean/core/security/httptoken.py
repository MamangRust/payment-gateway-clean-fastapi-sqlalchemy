from typing import Any, Union
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

class HTTPTokenHeader(APIKeyHeader):
    def __init__(self, raise_error: bool = True, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.raise_error = raise_error

    async def __call__(self, request: Request) -> Union[str, None]:
        # Get the token from the Authorization header
        authorization_header = request.headers.get(self.model.name)
        if not authorization_header:
            if not self.raise_error:
                return None
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Missing authorization credentials",
            )

        # Split the header value to get the token type and token
        try:
            token_prefix, token = authorization_header.split(" ")
        except ValueError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token schema"
            )

        # Check if the token type is 'Bearer'
        if token_prefix.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token schema"
            )

        return token
