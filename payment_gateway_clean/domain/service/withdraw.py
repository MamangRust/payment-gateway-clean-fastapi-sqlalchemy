import abc
from typing import List, Optional, Any, Union
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.withdraw import WithdrawResponse
from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest


class IWithdrawService(abc.ABC):
    """
    Abstract base class defining the interface for WithdrawService.
    """

    @abc.abstractmethod
    async def get_withdraws(self) -> Union[ApiResponse[List[WithdrawResponse]], ErrorResponse]:
        """
        Retrieve a list of all withdrawal records.
        """
        pass

    @abc.abstractmethod
    async def get_withdraw(self, id: int) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        """
        Retrieve a specific withdrawal record by ID.
        """
        pass

    @abc.abstractmethod
    async def get_withdraw_users(self, user_id: int) -> Union[ApiResponse[Optional[List[WithdrawResponse]]], ErrorResponse]:
        """
        Retrieve all withdrawal records associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def get_withdraw_user(self, user_id: int) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        """
        Retrieve a specific withdrawal record for a user by user ID.
        """
        pass

    @abc.abstractmethod
    async def create_withdraw(self, input: CreateWithdrawRequest) -> Union[ApiResponse[WithdrawResponse], ErrorResponse]:
        """
        Create a new withdrawal record from the given request.
        """
        pass

    @abc.abstractmethod
    async def update_withdraw(self, input: UpdateWithdrawRequest) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        """
        Update an existing withdrawal record based on the given request.
        """
        pass

    @abc.abstractmethod
    async def delete_withdraw(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        """
        Delete a withdrawal record by its ID.
        """
        pass
