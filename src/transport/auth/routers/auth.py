from fastapi import APIRouter, Depends, HTTPException
from services.auth import *
from services.auth import auth_service
from typing import Annotated

router = APIRouter(
    tags=["Auth"]
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={"sub": user.login})
    return Token(access_token=access_token, token_type="bearer")

# @router.get("/hello/me")
# async def hello(current_user: Annotated[User, Depends(auth_service.current_user)]):
#     return {"msg": f"hello {current_user.login}"}