from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.dtos.record.topup import TopupRecordDTO

class TopupResponse(BaseModel):
    topup_id: int
    user_id: int
    topup_amount: int
    topup_method: str
    topup_time: datetime

    @staticmethod
    def from_dto(dto: TopupRecordDTO) -> 'TopupResponse':
        """
        Converts a TopupRecordDTO to a TopupResponse.
        """
        return TopupResponse(
            topup_id=dto.topup_id,
            user_id=dto.user_id,
            topup_amount=dto.topup_amount,
            topup_method=dto.topup_method,
            topup_time=dto.topup_time
        )

    @staticmethod
    def from_dtos(dtos: List[TopupRecordDTO]) -> List['TopupResponse']:
        """
        Converts a list of TopupRecordDTO to a list of TopupResponse.
        """
        return [TopupResponse.from_dto(dto) for dto in dtos]
