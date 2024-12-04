from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional

from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest, UpdateTransferAmountRequest


from domain.dtos.record.transfer import TransferRecordDTO
from domain.repository.transfer import ITransferRepository
from infrastructure.models.main import Transfer


class TransferRepository(ITransferRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> List[TransferRecordDTO]:
        """
        Retrieve all transfer records.
        """
        result = await self.session.execute(select(Transfer))
        transfers = result.scalars().all()
        return [TransferRecordDTO.from_orm(transfer) for transfer in transfers]

    async def find_by_id(self, id: int) -> Optional[TransferRecordDTO]:
        """
        Find a transfer record by its ID.
        """
        result = await self.session.execute(
            select(Transfer).filter(Transfer.transfer_id == id)
        )
        transfer = result.scalars().first()
        return TransferRecordDTO.from_orm(transfer) if transfer else None

    async def find_by_users(self, user_id: int) -> Optional[List[TransferRecordDTO]]:
        """
        Find all transfer records associated with a given user ID.
        """
        result = await self.session.execute(
            select(Transfer)
            .filter(
                or_(
                    Transfer.transfer_from == user_id,
                    Transfer.transfer_to == user_id
                )
            )
            .order_by(Transfer.created_at.desc())  
        )
        transfers = result.scalars().all() 
        return [TransferRecordDTO.from_orm(t) for t in transfers]

    async def find_by_user(self, user_id: int) -> Optional[TransferRecordDTO]:
        """
        Find a single transfer record associated with a given user ID.
        """
        result = await self.session.execute(
            select(Transfer)
            .filter(
                or_(
                    Transfer.transfer_from == user_id,  
                    Transfer.transfer_to == user_id, 
                )
            )
            .limit(1) 
        )

        transfer = result.scalars().first()  # Get the first (and only) matching transfer
        return TransferRecordDTO.from_orm(transfer) if transfer else None

    async def create(self, input: CreateTransferRequest) -> TransferRecordDTO:
        """
        Create a new transfer record from the given input.
        """
        new_transfer = Transfer(
            transfer_from=input.transfer_from,
            transfer_to=input.transfer_to,
            transfer_amount=input.transfer_amount,
            transfer_time=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(new_transfer)
        await self.session.commit()
        await self.session.refresh(new_transfer)
        return TransferRecordDTO.from_orm(new_transfer)

    async def update(self, input: UpdateTransferRequest) -> TransferRecordDTO:
        """
        Update an existing transfer record based on the given input.
        """
        result = await self.session.execute(
            update(Transfer)
            .where(Transfer.transfer_id == input.transfer_id)
            .values(
                transfer_id=input.transfer_id,
                transfer_from=input.transfer_from,
                transfer_to=input.transfer_to,
                transfer_amount=input.transfer_amount,
                transfer_time=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            .returning(Transfer)
        )
        updated_transfer = result.scalars().first()
        if updated_transfer:
            await self.session.commit()
            await self.session.refresh(updated_transfer)
            return TransferRecordDTO.from_orm(updated_transfer)
        else:
            raise ValueError("Transfer record not found")

    async def update_amount(
        self, input: UpdateTransferAmountRequest
    ) -> TransferRecordDTO:
        """
        Update the amount of an existing transfer record.
        """
        result = await self.session.execute(
            update(Transfer)
            .where(Transfer.transfer_id == input.transfer_id)
            .values(
                transfer_id=input.transfer_id,
                transfer_amount=input.transfer_amount,
                updated_at=datetime.utcnow(),
            )
            .returning(Transfer)
        )
        updated_transfer = result.scalars().first()
        if updated_transfer:
            await self.session.commit()
            await self.session.refresh(updated_transfer)
            return TransferRecordDTO.from_orm(updated_transfer)
        else:
            raise ValueError("Transfer record not found")

    async def delete(self, id: int) -> None:
        """
        Delete a transfer record by its ID.
        """
        result = await self.session.execute(
            delete(Transfer).where(Transfer.transfer_id == id)
        )
        if result.rowcount == 0:
            raise ValueError("Transfer record not found")
        await self.session.commit()
