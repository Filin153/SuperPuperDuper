from typing import Union
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class AuthUserModel(BaseModel):
    login: str
    password: str



class AuthCreateUser(AuthUserModel):
    password: str = None


class AuthUserInDB(AuthUserModel):
    hashed_password: str