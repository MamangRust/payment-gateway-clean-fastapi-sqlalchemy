from pydantic import BaseModel, model_validator, EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    confirm_password: str
    noc_transfer: Optional[str]

    # @model_validator(mode="before")
    # def check_password_match(cls, values):
    #     password = values.get("password")
    #     confirm = values.get("confirm_password")

    #     if password != confirm:
    #         raise ValueError('Password and confirm password must match')
    #     return values



class UpdateUserRequest(BaseModel):
    id: Optional[int]
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    confirm_password: Optional[str]

    @model_validator(mode="before")
    def check_password_match(cls, values):
        password = values.get("password")
        confirm = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError('Password and confirm password must match')
        return values