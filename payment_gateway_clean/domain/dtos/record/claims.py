from pydantic import BaseModel
from typing import Optional

class Claims(BaseModel):
    user_id: int
    exp: float
    iat: float

    @staticmethod
    def create(user_id: int, exp: float, iat: float) -> 'Claims':
        return Claims(user_id=user_id, exp=exp, iat=iat)
