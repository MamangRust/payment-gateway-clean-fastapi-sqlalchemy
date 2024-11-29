import abc
from typing import List, Optional, Any
from domain.dtos.record.topup import TopupRecordDTO
from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest, UpdateTopupAmount


class ITopupRepository(abc.ABC):
    """
    Topup Repository interface defining operations for topup management.
    """

    @abc.abstractmethod
    async def find_all(self, session: Any) -> List[TopupRecordDTO]:
        """
        Retrieve all topup records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, session: Any,id: int) -> Optional[TopupRecordDTO]:
        """
        Find a topup record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users(self, session: Any,user_id: int) -> List[Optional[TopupRecordDTO]]:
        """
        Find all topup records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user(self, session: Any,user_id: int) -> Optional[TopupRecordDTO]:
        """
        Find a single topup record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, session: Any,input: CreateTopupRequest) -> TopupRecordDTO:
        """
        Create a new topup record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(self, session: Any,input: UpdateTopupRequest) -> TopupRecordDTO:
        """
        Update an existing topup record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def update_amount(self, session: Any,input: UpdateTopupAmount) -> TopupRecordDTO:
        """
        Update the amount of an existing topup record.
        """
        pass

    @abc.abstractmethod
    async def delete(self, session: Any,id: int) -> None:
        """
        Delete a topup record by its ID.
        """
        pass

