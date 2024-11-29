from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.dtos.record.withdraw import WithdrawRecordDTO

class WithdrawResponse(BaseModel):
    withdraw_id: int
    user_id: int
    withdraw_amount: int
    withdtaw_time: datetime

    @staticmethod
    def from_dto(dto: WithdrawRecordDTO) -> 'WithdrawResponse':
        """
        Converts a WithdrawRecordDTO to a WithdrawResponse.
        """
        return WithdrawResponse(
            withdraw_id=dto.withdraw_id,
            user_id=dto.user_id,
            withdraw_amount=dto.withdraw_amount,
            withdtaw_time=dto.withdtaw_time
        )

    @staticmethod
    def from_dtos(dtos: List[WithdrawRecordDTO]) -> List['WithdrawResponse']:
        """
        Converts a list of WithdrawRecordDTO to a list of WithdrawResponse.
        """
        return [WithdrawResponse.from_dto(dto) for dto in dtos]