from fastapi.security import OAuth2PasswordRequestForm
from config.config import settings
import logging
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import JWTError, jwt
from .schemas import *
from database.user import UserDB
from models import User


class Auth:
    def __init__(self, with_my_ttl: bool = False):
        """
        :param with_my_ttl: default 15min, TTL set in settings
        """
        self.with_my_ttl = with_my_ttl
        self.user_db = UserDB()

    def authenticate_user(self, username: str, password: str):
        user = self.user_db.get(username)
        if not user:
            logging.debug("Not user")
            return False
        if not self.__verify_password(password, user.password):
            logging.debug("Password incorrect")
            return False

        logging.debug("User found")
        return user

    def get_token(self, data: OAuth2PasswordRequestForm):
        user = self.authenticate_user(data.username, data.password)
        if self.with_my_ttl:
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = self.create_access_token(
                data={"sub": user.login}, expires_delta=access_token_expires
            )
        else:
            access_token = self.create_access_token(
                data={"sub": user.login}
            )
        return Token(access_token=access_token, token_type="bearer")

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            logging.debug(f"Setting expiration time: {expires_delta}min")
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        logging.debug(f"JWT encoded successfully: {encoded_jwt}")
        return encoded_jwt

    async def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as e:
            logging.debug(e)
            raise credentials_exception
        user = self.user_db.get(token_data.username)
        logging.debug(user)
        if user is None:
            logging.debug("No user")
            raise credentials_exception
        return user

    def __verify_password(self, plain_password, hashed_password):
        return settings.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return settings.pwd_context.hash(password)


class AuthService(Auth):
    async def current_user(
            self,
            token: str,

    ):
        current_user = await Auth().get_current_user(token=token)
        user = self.get_current_active_user(current_user)
        user.token = token
        return user

    def get_current_active_user(
            self,
            user: User

    ):
        if user.banned:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user


auth_service = AuthService()
