from pydantic import BaseModel
from services.auth.schemas import AuthUserModel

class UserModel(BaseModel):
    login: str
    banned: bool

class CreateUser(AuthUserModel):
    password: str