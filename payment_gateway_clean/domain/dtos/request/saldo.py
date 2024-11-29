from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateSaldoRequest(BaseModel):
    user_id: int
    total_balance: int


class UpdateSaldoRequest(BaseModel):
    saldo_id: int
    user_id: int
    total_balance: int
    withdraw_amount: Optional[int]
    withdraw_time: Optional[datetime]



class UpdateSaldoBalanceRequest(BaseModel):
    total_balance: int
    user_id: int