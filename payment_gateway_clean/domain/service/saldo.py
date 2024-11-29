import abc
from typing import List, Optional, Any, Union
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.saldo import SaldoResponse
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest


class ISaldoService(abc.ABC):
    """
    Abstract base class defining the interface for SaldoService.
    """

    @abc.abstractmethod
    async def get_saldos(self) -> Union[ApiResponse[List[SaldoResponse]], ErrorResponse]:
        """
        Retrieve a list of all saldos.
        """
        pass

    @abc.abstractmethod
    async def get_saldo(self, id: int) -> Union[ApiResponse[Optional[SaldoResponse]], ErrorResponse]:
        """
        Retrieve a single saldo by ID.
        """
        pass

    @abc.abstractmethod
    async def get_saldo_users(self, id: int) -> Union[ApiResponse[Optional[List[SaldoResponse]]], ErrorResponse]:
        """
        Retrieve all saldos associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def get_saldo_user(self, id: int) -> Union[ApiResponse[Optional[SaldoResponse]], ErrorResponse]:
        """
        Retrieve a single saldo associated with a specific user ID.
        """
        pass

    @abc.abstractmethod
    async def create_saldo(self, input: CreateSaldoRequest) -> Union[ApiResponse[SaldoResponse], ErrorResponse]:
        """
        Create a new saldo from the given request.
        """
        pass

    @abc.abstractmethod
    async def update_saldo(self, input: UpdateSaldoRequest) -> ApiResponse[Optional[SaldoResponse]]:
        """
        Update an existing saldo with the given request data.
        """
        pass

    @abc.abstractmethod
    async def delete_saldo(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        """
        Delete a saldo by its ID.
        """
        pass
