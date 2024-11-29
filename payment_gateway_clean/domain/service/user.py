import abc
from typing import List, Optional, Any, Union, List
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.user import UserResponse
from domain.dtos.request.user import CreateUserRequest, UpdateUserRequest


class IUserService(abc.ABC):
    """
    Abstract base class defining the interface for UserService.
    """

    @abc.abstractmethod
    async def get_users(self) -> Union[ApiResponse[List[UserResponse]], ErrorResponse]:
        """
        Retrieve a list of all users.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, id: int) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        """
        Retrieve a user by their ID.
        """
        pass

    @abc.abstractmethod
    async def create_user(self, input: CreateUserRequest) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        """
        Create a new user from the given request.
        """
        pass

    @abc.abstractmethod
    async def update_user(self, input: UpdateUserRequest) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        """
        Update an existing user's information.
        """
        pass

    @abc.abstractmethod
    async def delete_user(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        """
        Delete a user by their ID.
        """
        pass
