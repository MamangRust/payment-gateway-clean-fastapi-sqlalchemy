from pydantic import BaseModel, model_validator
from datetime import datetime

class CreateWithdrawRequest(BaseModel):
    user_id: int
    withdraw_amount: int
    withdraw_time: datetime

    @model_validator(mode="before")
    def validate_withdraw_amount(cls, values):
        if values['withdraw_time'] >= 50000:
            raise ValueError('Withdraw amount must be less than 50000')
        return values


class UpdateWithdrawRequest(BaseModel):
    user_id: int
    withdraw_id: int
    withdraw_amount: int
    withdraw_time: datetime

    @model_validator(mode="before")
    def validate_withdraw_amount(cls, values):
        if values['withdraw_time'] >= 50000:
            raise ValueError('Withdraw amount must be less than 50000')
        return values