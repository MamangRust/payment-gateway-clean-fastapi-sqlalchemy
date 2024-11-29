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
    async def find_all(self, session: AsyncSession) -> List[WithdrawRecordDTO]:
        """
        Retrieve all withdrawal records.
        """
        result = await session.execute(select(Withdraw))
        withdrawals = result.scalars().all()
        return [WithdrawRecordDTO.from_orm(withdrawal) for withdrawal in withdrawals]

    async def find_by_id(self, session: AsyncSession, id: int) -> Optional[WithdrawRecordDTO]:
        """
        Find a withdrawal record by its ID.
        """
        result = await session.execute(select(Withdraw).filter(Withdraw.id == id))
        withdrawal = result.scalars().first()
        return WithdrawRecordDTO.from_orm(withdrawal) if withdrawal else None

    async def find_by_users(self, session: AsyncSession, user_id: int) -> Optional[List[WithdrawRecordDTO]]:
        """
        Find all withdrawal records associated with a given user ID.
        """
        result = await session.execute(select(Withdraw).filter(Withdraw.user_id == user_id))
        withdrawals = result.scalars().all()
        return [WithdrawRecordDTO.from_orm(withdrawal) for withdrawal in withdrawals] if withdrawals else None

    async def find_by_user(self, session: AsyncSession, user_id: int) -> Optional[WithdrawRecordDTO]:
        """
        Find a single withdrawal record associated with a given user ID.
        """
        result = await session.execute(select(Withdraw).filter(Withdraw.user_id == user_id))
        withdrawal = result.scalars().first()
        return WithdrawRecordDTO.from_orm(withdrawal) if withdrawal else None

    async def create(self, session: AsyncSession, input: CreateWithdrawRequest) -> WithdrawRecordDTO:
        """
        Create a new withdrawal record from the given input.
        """
        new_withdrawal = Withdraw(
            user_id=input.user_id,
            amount=input.amount,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_withdrawal)
        await session.commit()
        await session.refresh(new_withdrawal)
        return WithdrawRecordDTO.from_orm(new_withdrawal)

    async def update(self, session: AsyncSession, input: UpdateWithdrawRequest) -> WithdrawRecordDTO:
        """
        Update an existing withdrawal record based on the given input.
        """
        result = await session.execute(
            update(Withdraw)
            .where(Withdraw.id == input.id)
            .values(
                user_id=input.user_id,
                amount=input.amount,
                updated_at=datetime.utcnow()
            )
            .returning(Withdraw)
        )
        updated_withdrawal = result.scalars().first()
        if updated_withdrawal:
            await session.commit()
            await session.refresh(updated_withdrawal)
            return WithdrawRecordDTO.from_orm(updated_withdrawal)
        else:
            raise ValueError("Withdrawal record not found")

    async def delete(self, session: AsyncSession, id: int) -> None:
        """
        Delete a withdrawal record by its ID.
        """
        result = await session.execute(delete(Withdraw).where(Withdraw.id == id))
        if result.rowcount == 0:
            raise ValueError("Withdrawal record not found")
        await session.commit()
