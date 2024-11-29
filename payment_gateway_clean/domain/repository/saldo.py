import abc
from typing import List, Optional, Any
from domain.dtos.record.saldo import SaldoRecordDTO
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoBalanceRequest, UpdateSaldoRequest

class ISaldoRepository(abc.ABC):
    """
    Saldo Repository interface defining operations for saldo management.
    """

    @abc.abstractmethod
    async def find_all(self, session: Any) -> List[SaldoRecordDTO]:
        """
        Retrieve all saldo records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, session: Any,id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a saldo record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users_id(self, session: Any,id: int) -> List[Optional[SaldoRecordDTO]]:
        """
        Find all saldo records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user_id(self, session: Any,id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, session: Any,input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, session: Any,input: UpdateSaldoRequest) -> SaldoRecordDTO:
        """
        Update an existing saldo record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_balance(self, session: Any,input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, session: Any,id: int) -> None:
        """
        Delete a saldo record by its ID.
        """
        pass
