from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from typing import List, Optional

from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest, UpdateSaldoBalanceRequest
from domain.dtos.record.saldo import SaldoRecordDTO
from domain.repository.saldo import ISaldoRepository
from infrastructure.models.main import Saldo
from datetime import datetime

class SaldoRepository(ISaldoRepository):
    async def find_all(self, session: AsyncSession) -> List[SaldoRecordDTO]:
        """
        Retrieve all saldo records.
        """
        result = await session.execute(select(Saldo))
        saldos = result.scalars().all()
        return [SaldoRecordDTO.from_orm(saldo) for saldo in saldos]

    async def find_by_id(self, session: AsyncSession, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a saldo record by its ID.
        """
        result = await session.execute(select(Saldo).filter(Saldo.id == id))
        saldo = result.scalars().first()
        return SaldoRecordDTO.from_orm(saldo) if saldo else None

    async def find_by_users_id(self, session: AsyncSession, id: int) -> List[Optional[SaldoRecordDTO]]:
        """
        Find all saldo records associated with a given user ID.
        """
        result = await session.execute(select(Saldo).filter(Saldo.user_id == id))
        saldos = result.scalars().all()
        return [SaldoRecordDTO.from_orm(saldo) for saldo in saldos]

    async def find_by_user_id(self, session: AsyncSession, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        result = await session.execute(select(Saldo).filter(Saldo.user_id == id))
        saldo = result.scalars().first()
        return SaldoRecordDTO.from_orm(saldo) if saldo else None

    async def create(self, session: AsyncSession, input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        new_saldo = Saldo(
            user_id=input.user_id,
            balance=input.balance,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_saldo)
        await session.commit()
        await session.refresh(new_saldo)
        return SaldoRecordDTO.from_orm(new_saldo)

    async def update(self, session: AsyncSession, input: UpdateSaldoRequest) -> SaldoRecordDTO:
        """
        Update an existing saldo record based on the given input.
        """
        result = await session.execute(
            update(Saldo)
            .where(Saldo.id == input.id)
            .values(
                user_id=input.user_id,
                balance=input.balance,
                updated_at=datetime.utcnow()
            )
            .returning(Saldo)
        )
        updated_saldo = result.scalars().first()
        if updated_saldo:
            await session.commit()
            await session.refresh(updated_saldo)
            return SaldoRecordDTO.from_orm(updated_saldo)
        else:
            raise ValueError("Saldo record not found")

    async def update_balance(self, session: AsyncSession, input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        result = await session.execute(
            update(Saldo)
            .where(Saldo.id == input.id)
            .values(
                balance=input.balance,
                updated_at=datetime.utcnow()
            )
            .returning(Saldo)
        )
        updated_saldo = result.scalars().first()
        if updated_saldo:
            await session.commit()
            await session.refresh(updated_saldo)
            return SaldoRecordDTO.from_orm(updated_saldo)
        else:
            raise ValueError("Saldo record not found")

    async def delete(self, session: AsyncSession, id: int) -> None:
        """
        Delete a saldo record by its ID.
        """
        result = await session.execute(delete(Saldo).where(Saldo.id == id))
        if result.rowcount == 0:
            raise ValueError("Saldo record not found")
        await session.commit()
