from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from domain.dtos.record.user import UserRecordDTO

class UserResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    email: str
    noc_transfer: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dto(dto: UserRecordDTO) -> 'UserResponse':
        return UserResponse(
            user_id=dto.user_id,
            firstname=dto.firstname,
            lastname=dto.lastname,
            email=dto.email,
            noc_transfer=dto.noc_transfer,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def from_dtos(dtos: List[UserRecordDTO]) -> List['UserResponse']:
        return [
            UserResponse.from_dto(dto) for dto in dtos
        ]