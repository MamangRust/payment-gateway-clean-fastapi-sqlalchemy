from pydantic import BaseModel, model_validator

class CreateTransferRequest(BaseModel):
    transfer_from: int
    transfer_to: int
    transfer_amount: int

    @model_validator(mode="before")
    def validate_transfer_amount(cls, values):
        if values['transfer_amount'] >= 50000:
            raise ValueError('Transfer amount must be less than 50000')
        return values


class UpdateTransferRequest(BaseModel):
    transfer_id: int
    transfer_from: int
    transfer_to: int
    transfer_amount: int

    @model_validator(mode="before")
    def validate_transfer_amount(cls, values):
        if values['transfer_amount'] >= 50000:
            raise ValueError('Transfer amount must be less than 50000')
        return values


class UpdateTransferAmountRequest(BaseModel):
    transfer_id: int
    transfer_amount: int

    @model_validator(mode="before")
    def validate_transfer_amount(cls, values):
        if values['transfer_amount'] >= 50000:
            raise ValueError('Transfer amount must be less than 50000')
        return values