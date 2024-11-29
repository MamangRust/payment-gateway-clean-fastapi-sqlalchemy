from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger
from typing import Union, List

from domain.repository.user import IUserRepository
from domain.service.user import IUserService

from core.security.hashpassword import Hashing

from domain.dtos.request.user import (
    CreateUserRequest,
    UpdateUserRequest,
)
from domain.dtos.response.api import ApiResponse, ErrorResponse
from core.errors import AppError
from domain.dtos.response.user import UserResponse


logger = get_logger()


class UserService(IUserService):
    def __init__(self, repository: IUserRepository, hashing: Hashing) -> None:
        self.repository = repository
        self.hashing = hashing

    async def get_users(self) -> Union[ApiResponse[List[UserResponse]], ErrorResponse]:
        try:
            users = await self.repository.find_all()
            user_responses = [UserResponse.from_dto(user) for user in users]
            return ApiResponse(
                status="success",
                message="Successfully retrieved users.",
                data=user_responses,
            )
        except Exception as e:
            logger.error("Error retrieving users", error=str(e))
            return ErrorResponse(
                status="error",
                message="Internal Server Error.",
            )

    async def find_by_id(
        self, id: int
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        try:
            user = await self.repository.find_by_id(id)
            if not user:
                return ErrorResponse(
                    status="error",
                    message="User with the specified ID does not exist.",
                )
            return ApiResponse(
                status="success",
                message="Successfully retrieved user.",
                data=UserResponse.from_dto(user),
            )
        except Exception as e:
            logger.error("Error retrieving user by ID", user_id=id, error=str(e))
            return ErrorResponse(
                status="error",
                message="Internal Server Error.",
            )

    async def create_user(
        self, input: CreateUserRequest
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        try:
            exists = await self.repository.find_by_email_exists(
                email=input.email
            ) 
            if exists:
                logger.error("Email already exists", email=input.email)
                return ErrorResponse(
                    status="error",
                    message="Email already exists.",
                )

            hashed_password = await self.hashing.hash_password(input.password)
            input.password = hashed_password

            user = await self.repository.create_user(input)
            return ApiResponse(
                status="success",
                message="User created successfully.",
                data=UserResponse.from_dtos(user),
            )
        except Exception as e:
            logger.error("Error creating user", error=str(e))
            return ErrorResponse(
                status="error",
                message="Internal Server Error.",
            )

    async def update_user(
        self, input: UpdateUserRequest
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        try:
            user = await self.repository.find_by_id(input.user_id)
            if not user:
                return ErrorResponse(
                    status="error",
                    message="User with the specified ID does not exist.",
                )

            updated_user = await self.repository.update_user(input)
            return ApiResponse(
                status="success",
                message="User updated successfully.",
                data=UserResponse.from_dto(updated_user),
            )
        except Exception as e:
            logger.error("Error updating user", user_id=input.user_id, error=str(e))
            return ErrorResponse(
                status="error",
                message="Internal Server Error.",
            )

    async def delete_user(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        try:
            user = await self.repository.find_by_id(id)
            if not user:
                return ErrorResponse(
                    status="error",
                    message="User with the specified ID does not exist.",
                )

            await self.repository.delete_user(id)
            return ApiResponse(
                status="success",
                message="User deleted successfully.",
                data=None,
            )
        except Exception as e:
            logger.error("Error deleting user", user_id=id, error=str(e))
            return ErrorResponse(
                status="error",
                message="Internal Server Error.",
            )
