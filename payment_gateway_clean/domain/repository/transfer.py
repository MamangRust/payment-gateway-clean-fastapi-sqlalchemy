import abc
from typing import List, Optional, Any
from domain.dtos.record.transfer import TransferRecordDTO
from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest, UpdateTransferAmountRequest

class ITransferRepository(abc.ABC):
    """
    Transfer Repository interface defining operations for transfer management.
    """

    @abc.abstractmethod
    async def find_all(self, session: Any) -> List[TransferRecordDTO]:
        """
        Retrieve all transfer records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, session: Any,id: int) -> Optional[TransferRecordDTO]:
        """
        Find a transfer record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users(self, session: Any,user_id: int) -> Optional[List[TransferRecordDTO]]:
        """
        Find all transfer records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user(self, session: Any,user_id: int) -> Optional[TransferRecordDTO]:
        """
        Find a single transfer record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, session: Any,input: CreateTransferRequest) -> TransferRecordDTO:
        """
        Create a new transfer record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, session: Any,input: UpdateTransferRequest) -> TransferRecordDTO:
        """
        Update an existing transfer record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_amount(self, session: Any,input: UpdateTransferAmountRequest) -> TransferRecordDTO:
        """
        Update the amount of an existing transfer record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, session: Any,id: int) -> None:
        """
        Delete a transfer record by its ID.
        """
        pass
