from pydantic import BaseModel
from datetime import datetime

class TransferRecordDTO(BaseModel):
    transfer_id: int
    transfer_from: int
    transfer_to: int
    tranfer_amount: int
    tranfer_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

        