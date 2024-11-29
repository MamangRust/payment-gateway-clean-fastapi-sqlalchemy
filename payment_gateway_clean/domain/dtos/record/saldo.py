from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SaldoRecordDTO(BaseModel):
    saldo_id: int
    user_id: int
    total_balance: int
    withdraw_amount: Optional[int]
    withdraw_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
