from pydantic import BaseModel, Field, model_validator, EmailStr

class RegisterRequest(BaseModel):
    firstname: str = Field(..., max_length=50)
    lastname: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @model_validator(mode="before")
    def check_password_match(cls, values):
        password = values.get("password")
        confirm = values.get("confirm_password")

        if password != confirm:
            raise ValueError('Password and confirm password must match')
        return values



class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=6)