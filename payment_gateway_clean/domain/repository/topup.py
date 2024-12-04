import abc
from typing import List, Optional, Any
from domain.dtos.record.topup import TopupRecordDTO
from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest, UpdateTopupAmount


class ITopupRepository(abc.ABC):
    """
    Topup Repository interface defining operations for topup management.
    """

    @abc.abstractmethod
    async def find_all(self) -> List[TopupRecordDTO]:
        """
        Retrieve all topup records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, id: int) -> Optional[TopupRecordDTO]:
        """
        Find a topup record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users(self, user_id: int) -> List[Optional[TopupRecordDTO]]:
        """
        Find all topup records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user(self, user_id: int) -> Optional[TopupRecordDTO]:
        """
        Find a single topup record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, input: CreateTopupRequest) -> TopupRecordDTO:
        """
        Create a new topup record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, input: UpdateTopupRequest) -> TopupRecordDTO:
        """
        Update an existing topup record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_amount(self, input: UpdateTopupAmount) -> TopupRecordDTO:
        """
        Update the amount of an existing topup record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete a topup record by its ID.
        """
        pass