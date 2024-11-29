from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union

class CreateTopupRequest(BaseModel):
    user_id: int
    topup_no: str
    topup_amount: int
    topup_method: str

    @validator('topup_amount')
    def validate_topup_amount(cls, value):
        if value > 50000:
            raise ValueError('Topup amount must not exceed 50000')
        return value

    @validator('topup_method')
    def payment_method_validator(cls, value):
        payment_rules = [
            "alfamart", "indomart", "lawson", "dana", "ovo", "gopay", "linkaja", "jenius",
            "fastpay", "kudo", "bri", "mandiri", "bca", "bni", "bukopin", "e-banking", "visa",
            "mastercard", "discover", "american express", "paypal"
        ]
        if value.lower() not in payment_rules:
            raise ValueError(f'Invalid payment method: {value}')
        return value

class UpdateTopupRequest(BaseModel):
    user_id: int
    topup_id: int
    topup_amount: int
    topup_method: str

    @validator('topup_amount')
    def validate_topup_amount(cls, value):
        if value > 50000:
            raise ValueError('Topup amount must not exceed 50000')
        return value

    @validator('topup_method')
    def payment_method_validator(cls, value):
        payment_rules = [
            "alfamart", "indomart", "lawson", "dana", "ovo", "gopay", "linkaja", "jenius",
            "fastpay", "kudo", "bri", "mandiri", "bca", "bni", "bukopin", "e-banking", "visa",
            "mastercard", "discover", "american express", "paypal"
        ]
        if value.lower() not in payment_rules:
            raise ValueError(f'Invalid payment method: {value}')
        return value


class UpdateTopupAmount(BaseModel):
    topup_id: int = Field(..., gt=0, description="Top-up ID must be a positive integer")
    topup_amount: int = Field(..., ge=50000, description="Top-up amount must be greater than or equal to 50000")

    @validator("topup_id")
    def validate_topup_id(cls, value):
        if value <= 0:
            raise ValueError("Top-up ID must be a positive integer")
        return value

    @validator("topup_amount")
    def validate_topup_amount(cls, value):
        if value < 50000:
            raise ValueError("Topup amount must be greater than or equal to 50000")
        return value