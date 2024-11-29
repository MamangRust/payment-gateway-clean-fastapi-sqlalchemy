from pydantic import BaseModel
from datetime import datetime

class TopupRecordDTO(BaseModel):
    topup_id: int
    user_id: int
    topup_amount: int
    topup_method: str
    topup_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_config = True