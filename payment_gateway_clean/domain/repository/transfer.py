import abc
from typing import List, Optional, Any
from domain.dtos.record.transfer import TransferRecordDTO
from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest, UpdateTransferAmountRequest

class ITransferRepository(abc.ABC):
    """
    Transfer Repository interface defining operations for transfer management.
    """

    @abc.abstractmethod
    async def find_all(self) -> List[TransferRecordDTO]:
        """
        Retrieve all transfer records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, id: int) -> Optional[TransferRecordDTO]:
        """
        Find a transfer record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users(self, user_id: int) -> Optional[List[TransferRecordDTO]]:
        """
        Find all transfer records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user(self, user_id: int) -> Optional[TransferRecordDTO]:
        """
        Find a single transfer record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, input: CreateTransferRequest) -> TransferRecordDTO:
        """
        Create a new transfer record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, input: UpdateTransferRequest) -> TransferRecordDTO:
        """
        Update an existing transfer record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_amount(self, input: UpdateTransferAmountRequest) -> TransferRecordDTO:
        """
        Update the amount of an existing transfer record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete a transfer record by its ID.
        """
        pass

