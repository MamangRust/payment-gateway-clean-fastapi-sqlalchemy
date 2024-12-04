import abc
from typing import List, Optional, Any
from domain.dtos.record.user import UserRecordDTO
from domain.dtos.request.user import CreateUserRequest, UpdateUserRequest


class IUserRepository(abc.ABC):
    """
    User Repository interface defining operations for user management.
    """

    @abc.abstractmethod
    async def create_user(self, user: CreateUserRequest) -> UserRecordDTO:
        """
        Add a new user record to the repository.
        """
        pass

    @abc.abstractmethod
    async def find_all(self) -> List[UserRecordDTO]:
        """
        Find all user records in the repository.
        """
        pass

    @abc.abstractmethod
    def find_by_email_exists(self, email: str) -> bool:
        """
        Check if a user with the given email exists in the repository.
        """
        pass

    @abc.abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserRecordDTO]:
        """
        Find a user by their email.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[UserRecordDTO]:
        """
        Find a user by their ID.
        """
        pass

    @abc.abstractmethod
    async def update_user(self, user: UpdateUserRequest) -> UserRecordDTO:
        """
        Update an existing user record.
        """
        pass

    @abc.abstractmethod
    async def delete_user(self, user_id: int) -> None:
        """
        Delete a user by their ID.
        """
        pass

