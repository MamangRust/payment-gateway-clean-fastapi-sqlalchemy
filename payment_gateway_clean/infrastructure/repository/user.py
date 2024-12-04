from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional

from domain.dtos.request.user import CreateUserRequest, UpdateUserRequest
from domain.dtos.record.user import UserRecordDTO
from domain.repository.user import IUserRepository
from infrastructure.models.main import User



class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: CreateUserRequest) -> UserRecordDTO:
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=user.password,
            noc_transfer=user.noc_transfer,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserRecordDTO.from_orm(new_user)
    
    async def find_all(self) -> List[UserRecordDTO]:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return [UserRecordDTO.from_orm(user) for user in users]

    async def find_by_email_exists(self, email: str) -> bool:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return user is not None

    async def find_by_email(self, email: str) -> Optional[UserRecordDTO]:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return UserRecordDTO.from_orm(user) if user else None

    async def find_by_email(self, email: str) -> Optional[UserRecordDTO]:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return UserRecordDTO.from_orm(user) if user else None

    async def find_by_id(self, user_id: int) -> Optional[UserRecordDTO]:
        result = await self.session.execute(select(User).filter(User.user_id == user_id))
        user = result.scalars().first()
        return UserRecordDTO.from_orm(user) if user else None

    async def update_user(self, user: UpdateUserRequest) -> UserRecordDTO:
        result = await self.session.execute(
            update(User)
            .where(User.user_id == user.id)
            .values(
                firstname=user.firstname,
                lastname=user.lastname,
                email=user.email,
                password=user.password,
                updated_at=datetime.utcnow()
            )
            .returning(User)
        )
        updated_user = result.scalars().first()
        if updated_user:
            await self.session.commit()
            await self.session.refresh(updated_user)
            return UserRecordDTO.from_orm(updated_user)
        else:
            raise ValueError("User not found")

    async def delete_user(self, user_id: int) -> None:
        result = await self.session.execute(delete(User).where(User.user_id == user_id))
        if result.rowcount == 0:
            raise ValueError("User not found")
        await self.session.commit()