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
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> List[TopupRecordDTO]:
        """
        Retrieve all topup records.
        """
        result = await self.session.execute(select(Topup))
        topups = result.scalars().all()
        return [TopupRecordDTO.from_orm(topup) for topup in topups]

    async def find_by_id(self, id: int) -> Optional[TopupRecordDTO]:
        """
        Find a topup record by its ID.
        """
        result = await self.session.execute(select(Topup).filter(Topup.topup_id == id))
        topup = result.scalars().first()
        return TopupRecordDTO.from_orm(topup) if topup else None

    async def find_by_users(self, user_id: int) -> List[Optional[TopupRecordDTO]]:
        """
        Find all topup records associated with a given user ID.
        """
        result = await self.session.execute(
            select(Topup).filter(Topup.user_id == user_id)
        )
        topups = result.scalars().all()
        return [TopupRecordDTO.from_orm(topup) for topup in topups]

    async def find_by_user(self, user_id: int) -> Optional[TopupRecordDTO]:
        """
        Find a single topup record associated with a given user ID.
        """
        result = await self.session.execute(
            select(Topup).filter(Topup.user_id == user_id)
        )
        topup = result.scalars().first()
        return TopupRecordDTO.from_orm(topup) if topup else None

    async def create(self, input: CreateTopupRequest) -> TopupRecordDTO:
        """
        Create a new topup record from the given input.
        """
        new_topup = Topup(
            topup_no=input.topup_no,
            user_id=input.user_id,
            topup_amount=input.topup_amount,
            topup_method=input.topup_method,
            topup_time=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(new_topup)
        await self.session.commit()
        await self.session.refresh(new_topup)
        return TopupRecordDTO.from_orm(new_topup)

    async def update(self, input: UpdateTopupRequest) -> TopupRecordDTO:
        """
        Update an existing topup record based on the given input.
        """
        result = await self.session.execute(
            update(Topup)
            .where(Topup.topup_id == input.topup_id)
            .values(
                topup_no=input.topup_no,
                user_id=input.user_id,
                topup_amount=input.topup_amount,
                topup_method=input.topup_method,
                topup_time=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            .returning(Topup)
        )
        updated_topup = result.scalars().first()
        if updated_topup:
            await self.session.commit()
            await self.session.refresh(updated_topup)
            return TopupRecordDTO.from_orm(updated_topup)
        else:
            raise ValueError("Topup record not found")

    async def update_amount(self, input: UpdateTopupAmount) -> TopupRecordDTO:
        """
        Update the amount of an existing topup record.
        """
        result = await self.session.execute(
            update(Topup)
            .where(Topup.topup_id == input.topup_id)
            .values(topup_amount=input.topup_amount, updated_at=datetime.utcnow())
            .returning(Topup)
        )
        updated_topup = result.scalars().first()
        if updated_topup:
            await self.session.commit()
            await self.session.refresh(updated_topup)
            return TopupRecordDTO.from_orm(updated_topup)
        else:
            raise ValueError("Topup record not found")

    async def delete(self, id: int) -> None:
        """
        Delete a topup record by its ID.
        """
        result = await self.session.execute(delete(Topup).where(Topup.topup_id == id))
        if result.rowcount == 0:
            raise ValueError("Topup record not found")
        await self.session.commit()
