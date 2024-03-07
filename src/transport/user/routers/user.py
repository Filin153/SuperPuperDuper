from database.user import UserDB
from models import User
from services.auth import auth_service
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from schemas.user import *
import os

router = APIRouter()
user_db = UserDB()

@router.post("/", response_model=CreateUser)
async def add_user(user_data: CreateUser):
    user_data.password = auth_service.get_password_hash(user_data.password)
    try:
        user = user_db.add(**user_data.dict())
        resp = CreateUser(
            login=user.login,
            banned=user.banned,
            password="",
        )
        os.mkdir(f"file/{user_data.login}")
        return resp
    except:
        raise HTTPException(status_code=400, detail="Юзер уже есть")


@router.get("/", response_model=UserModel)
async def get_user(current_user: Annotated[User, Depends(auth_service.current_user)]):
    try:
        return UserModel(
            login=current_user.login,
            banned=current_user.banned,
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@router.delete("/")
async def delete_user(current_user: Annotated[User, Depends(auth_service.current_user)]):
    try:
        return user_db.delete(current_user)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)
