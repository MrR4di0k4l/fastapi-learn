from pydantic import BaseModel,Field, field_validator
from datetime import datetime

class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250)
    password: str = Field(...)
    
    
class UserRegisterSchema(UserLoginSchema):
    username: str = Field(..., max_length=250)
    password: str = Field(...)
    password_confrim: str = Field(...)
    
    @field_validator("password")
    @classmethod
    def check_passwords_match(cls, password_confrim: str) -> str:
        # در اینجا فقط password داریم. برای مقایسه با confirm_password از model_validator باید استفاده کنیم.
        print("Password:", password_confrim)
        return password_confrim
