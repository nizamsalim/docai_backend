from pydantic import BaseModel,field_validator
from ..utils.exception import ValidationError

def validate_password(cls,val):
        if len(val) < 6:
            raise ValidationError(data=[{"field":"password","message":"Password should have a minimum length of 6 characters"}])
        return val

class LoginRequest(BaseModel):
    username:str
    password:str

    _validate_password = field_validator("password",mode="before")(validate_password)

class RegisterRequest(BaseModel):
    name:str
    username:str
    password:str

    _validate_password = field_validator("password",mode="before")(validate_password)
    

