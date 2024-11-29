from pydantic import BaseModel
from datetime import datetime


class UserRecordDTO(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    email: str
    password: str
    noc_transfer: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True