import abc
from typing import List, Optional, Any, Union
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.topup import TopupResponse
from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest


class ITopupService(abc.ABC):
    """
    Abstract base class defining the interface for TopupService.
    """

    @abc.abstractmethod
    async def get_topups(self) -> Union[ApiResponse[List[TopupResponse]], ErrorResponse]:
        """
        Retrieve a list of all topups.
        """
        pass

    @abc.abstractmethod
    async def get_topup(self, id: int) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        """
        Retrieve a single topup by ID.
        """
        pass

    @abc.abstractmethod
    async def get_topup_users(self, id: int) -> Union[ApiResponse[Optional[List[TopupResponse]]], ErrorResponse]:
        """
        Retrieve all topups associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def get_topup_user(self, id: int) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        """
        Retrieve a single topup associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def create_topup(self, input: CreateTopupRequest) -> Union[ApiResponse[TopupResponse], ErrorResponse]:
        """
        Create a new topup from the given request.
        """
        pass

    @abc.abstractmethod
    async def update_topup(self, input: UpdateTopupRequest) -> Union[ApiResponse[TopupResponse], ErrorResponse]:
        """
        Update an existing topup with the given request data.
        """
        pass

    @abc.abstractmethod
    async def delete_topup(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        """
        Delete a topup by its ID.
        """
        pass
