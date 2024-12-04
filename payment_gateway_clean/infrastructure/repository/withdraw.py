from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional

from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest
from domain.dtos.record.withdraw import WithdrawRecordDTO
from domain.repository.withdraw import IWithdrawRepository
from infrastructure.models.main import Withdraw

class WithdrawRepository(IWithdrawRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> List[WithdrawRecordDTO]:
        """
        Retrieve all withdrawal records.
        """
        result = await self.session.execute(select(Withdraw))
        withdrawals = result.scalars().all()
        return [WithdrawRecordDTO.from_orm(withdrawal) for withdrawal in withdrawals]

    async def find_by_id(self, id: int) -> Optional[WithdrawRecordDTO]:
        """
        Find a withdrawal record by its ID.
        """
        result = await self.session.execute(
            select(Withdraw).filter(Withdraw.withdraw_id == id)
        )
        withdrawal = result.scalars().first()
        return WithdrawRecordDTO.from_orm(withdrawal) if withdrawal else None

    async def find_by_users(self, user_id: int) -> Optional[List[WithdrawRecordDTO]]:
        """
        Find all withdrawal records associated with a given user ID.
        """
        result = await self.session.execute(
            select(Withdraw).filter(Withdraw.user_id == user_id)
        )
        withdraws = result.scalars().all()
        return [WithdrawRecordDTO.from_orm(withdraw) for withdraw in withdraws]

    async def find_by_user(self, user_id: int) -> Optional[WithdrawRecordDTO]:
        """
        Find a single withdrawal record associated with a given user ID.
        """
        result = await self.session.execute(
            select(Withdraw).filter(Withdraw.user_id == user_id).limit(1)
        )
        withdraw = result.scalars().first()
        return WithdrawRecordDTO.from_orm(withdraw) if withdraw else None

    async def create(self, input: CreateWithdrawRequest) -> WithdrawRecordDTO:
        """
        Create a new withdrawal record from the given input.
        """
        withdraw_time = input.withdraw_time.replace(tzinfo=None) if input.withdraw_time.tzinfo else input.withdraw_time

        # Create `created_at` and `updated_at` as offset-naive datetime objects
        created_at = datetime.now().replace(tzinfo=None)
        updated_at = datetime.now().replace(tzinfo=None)

        new_withdrawal = Withdraw(
            user_id=input.user_id,
            withdraw_amount=input.withdraw_amount,
            withdraw_time=withdraw_time,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.session.add(new_withdrawal)
        await self.session.commit()
        await self.session.refresh(new_withdrawal)
        return WithdrawRecordDTO.from_orm(new_withdrawal)

    async def update(self, input: UpdateWithdrawRequest) -> WithdrawRecordDTO:
        """
        Update an existing withdrawal record based on the given input.
        """
        withdraw_time = input.withdraw_time.replace(tzinfo=None) if input.withdraw_time.tzinfo else input.withdraw_time

        result = await self.session.execute(
            update(Withdraw)
            .where(Withdraw.withdraw_id == input.withdraw_id)
            .values(
                user_id=input.user_id,
                withdraw_amount=input.withdraw_amount,
                withdraw_time=withdraw_time,
                updated_at=datetime.utcnow(),
            )
            .returning(Withdraw)
        )
        updated_withdrawal = result.scalars().first()
        if updated_withdrawal:
            await self.session.commit()
            await self.session.refresh(updated_withdrawal)
            return WithdrawRecordDTO.from_orm(updated_withdrawal)
        else:
            raise ValueError("Withdrawal record not found")

    async def delete(self, id: int) -> None:
        """
        Delete a withdrawal record by its ID.
        """
        result = await self.session.execute(delete(Withdraw).where(Withdraw.withdraw_id == id))
        if result.rowcount == 0:
            raise ValueError("Withdrawal record not found")
        await self.session.commit()
