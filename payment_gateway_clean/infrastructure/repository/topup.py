from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime

from typing import List, Optional

from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest, UpdateTopupAmount
from domain.dtos.record.topup import TopupRecordDTO
from domain.repository.topup import ITopupRepository
from infrastructure.models.main import Topup


class TopupRepository(ITopupRepository):
    async def find_all(self, session: AsyncSession) -> List[TopupRecordDTO]:
        """
        Retrieve all topup records.
        """
        result = await session.execute(select(Topup))
        topups = result.scalars().all()
        return [TopupRecordDTO.from_orm(topup) for topup in topups]

    async def find_by_id(self, session: AsyncSession, id: int) -> Optional[TopupRecordDTO]:
        """
        Find a topup record by its ID.
        """
        result = await session.execute(select(Topup).filter(Topup.id == id))
        topup = result.scalars().first()
        return TopupRecordDTO.from_orm(topup) if topup else None

    async def find_by_users(self, session: AsyncSession, user_id: int) -> List[Optional[TopupRecordDTO]]:
        """
        Find all topup records associated with a given user ID.
        """
        result = await session.execute(select(Topup).filter(Topup.user_id == user_id))
        topups = result.scalars().all()
        return [TopupRecordDTO.from_orm(topup) for topup in topups]

    async def find_by_user(self, session: AsyncSession, user_id: int) -> Optional[TopupRecordDTO]:
        """
        Find a single topup record associated with a given user ID.
        """
        result = await session.execute(select(Topup).filter(Topup.user_id == user_id))
        topup = result.scalars().first()
        return TopupRecordDTO.from_orm(topup) if topup else None

    async def create(self, session: AsyncSession, input: CreateTopupRequest) -> TopupRecordDTO:
        """
        Create a new topup record from the given input.
        """
        new_topup = Topup(
            user_id=input.user_id,
            amount=input.amount,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_topup)
        await session.commit()
        await session.refresh(new_topup)
        return TopupRecordDTO.from_orm(new_topup)

    async def update(self, session: AsyncSession, input: UpdateTopupRequest) -> TopupRecordDTO:
        """
        Update an existing topup record based on the given input.
        """
        result = await session.execute(
            update(Topup)
            .where(Topup.id == input.id)
            .values(
                user_id=input.user_id,
                amount=input.amount,
                updated_at=datetime.utcnow()
            )
            .returning(Topup)
        )
        updated_topup = result.scalars().first()
        if updated_topup:
            await session.commit()
            await session.refresh(updated_topup)
            return TopupRecordDTO.from_orm(updated_topup)
        else:
            raise ValueError("Topup record not found")

    async def update_amount(self, session: AsyncSession, input: UpdateTopupAmount) -> TopupRecordDTO:
        """
        Update the amount of an existing topup record.
        """
        result = await session.execute(
            update(Topup)
            .where(Topup.id == input.id)
            .values(
                amount=input.amount,
                updated_at=datetime.utcnow()
            )
            .returning(Topup)
        )
        updated_topup = result.scalars().first()
        if updated_topup:
            await session.commit()
            await session.refresh(updated_topup)
            return TopupRecordDTO.from_orm(updated_topup)
        else:
            raise ValueError("Topup record not found")

    async def delete(self, session: AsyncSession, id: int) -> None:
        """
        Delete a topup record by its ID.
        """
        result = await session.execute(delete(Topup).where(Topup.id == id))
        if result.rowcount == 0:
            raise ValueError("Topup record not found")
        await session.commit()
