import abc
from typing import List, Optional, Any, Union
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.transfer import TransferResponse
from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest


class ITransferService(abc.ABC):
    """
    Abstract base class defining the interface for TransferService.
    """

    @abc.abstractmethod
    async def get_transfers(self) -> Union[ApiResponse[List[TransferResponse]], ErrorResponse]:
        """
        Retrieve a list of all transfers.
        """
        pass

    @abc.abstractmethod
    async def get_transfer(self, id: int) -> Union[ApiResponse[Optional[TransferResponse]], ErrorResponse]:
        """
        Retrieve a single transfer by its ID.
        """
        pass

    @abc.abstractmethod
    async def get_transfer_users(self, id: int) -> Union[ApiResponse[Optional[List[TransferResponse]]], ErrorResponse]:
        """
        Retrieve all transfers associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def get_transfer_user(self, id: int) -> Union[ApiResponse[Optional[TransferResponse]], ErrorResponse]:
        """
        Retrieve a single transfer associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def create_transfer(self, input: CreateTransferRequest) -> Union[ApiResponse[TransferResponse], ErrorResponse]:
        """
        Create a new transfer from the given request.
        """
        pass

    @abc.abstractmethod
    async def update_transfer(self, input: UpdateTransferRequest) -> Union[ApiResponse[TransferResponse], ErrorResponse]:
        """
        Update an existing transfer with the given request data.
        """
        pass

    @abc.abstractmethod
    async def delete_transfer(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        """
        Delete a transfer by its ID.
        """
        pass
