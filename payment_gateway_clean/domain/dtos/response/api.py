from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T]

    def __init__(self, status: str = "success", message: str = "", data: Optional[T] = None, **kwargs):
        """
        Custom initializer for ApiResponse.

        :param status: The status of the response (default: "success").
        :param message: The message to include in the response.
        :param data: The data payload of the response.
        :param kwargs: Additional keyword arguments for BaseModel.
        """
        super().__init__(status=status, message=message, data=data, **kwargs)


class ErrorResponse(BaseModel):
    status: str
    message: str