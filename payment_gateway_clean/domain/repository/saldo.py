import abc
from typing import List, Optional, Any
from domain.dtos.record.saldo import SaldoRecordDTO
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoBalanceRequest, UpdateSaldoRequest

class ISaldoRepository(abc.ABC):
    """
    Saldo Repository interface defining operations for saldo management.
    """

    @abc.abstractmethod
    async def find_all(self) -> List[SaldoRecordDTO]:
        """
        Retrieve all saldo records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a saldo record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users_id(self, id: int) -> List[Optional[SaldoRecordDTO]]:
        """
        Find all saldo records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user_id(self, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, input: UpdateSaldoRequest) -> SaldoRecordDTO:
        """
        Update an existing saldo record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_balance(self, input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete a saldo record by its ID.
        """
        pass
