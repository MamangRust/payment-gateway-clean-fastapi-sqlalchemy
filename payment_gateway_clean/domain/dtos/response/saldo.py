from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from domain.dtos.record.saldo import SaldoRecordDTO

class SaldoResponse(BaseModel):
    saldo_id: int
    total_balance: int
    withdraw_amount: Optional[int]
    withdraw_time: Optional[datetime]

    @staticmethod
    def from_dto(dto: SaldoRecordDTO) -> 'SaldoResponse':
        """
        Converts a SaldoRecordDTO to a SaldoResponse.
        """
        return SaldoResponse(
            saldo_id=dto.saldo_id,
            total_balance=dto.total_balance,
            withdraw_amount=dto.withdraw_amount,
            withdraw_time=dto.withdraw_time
        )

    @staticmethod
    def from_dtos(dtos: List[SaldoRecordDTO]) -> List['SaldoResponse']:
        """
        Converts a list of SaldoRecordDTO to a list of SaldoResponse.
        """
        return [SaldoResponse.from_dto(dto) for dto in dtos]
