import abc
from typing import List, Optional, Any
from domain.dtos.record.withdraw import WithdrawRecordDTO
from domain.dtos.request.withdraw import (
    CreateWithdrawRequest,
    UpdateWithdrawRequest,
)


class IWithdrawRepository(abc.ABC):
    """
    Withdraw Repository interface defining operations for managing withdrawal records.
    """

    @abc.abstractmethod
    async def find_all(self, session: Any) -> List[WithdrawRecordDTO]:
        """
        Retrieve all withdrawal records.
        """
        pass

    @abc.abstractmethod
    async def find_by_id(self, session: Any, id: int) -> Optional[WithdrawRecordDTO]:
        """
        Find a withdrawal record by its ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_users(
        self, session: Any, user_id: int
    ) -> Optional[List[WithdrawRecordDTO]]:
        """
        Find all withdrawal records associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def find_by_user(
        self, session: Any, user_id: int
    ) -> Optional[WithdrawRecordDTO]:
        """
        Find a single withdrawal record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(
        self, session: Any, input: CreateWithdrawRequest
    ) -> WithdrawRecordDTO:
        """
        Create a new withdrawal record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update(
        self, session: Any, input: UpdateWithdrawRequest
    ) -> WithdrawRecordDTO:
        """
        Update an existing withdrawal record based on the given input.
        """
        pass

    @abc.abstractmethod
    async def delete(self, session: Any, id: int) -> None:
        """
        Delete a withdrawal record by its ID.
        """
        pass
