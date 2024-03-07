from .db import engine, BaseDB
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User


class UserDB(BaseDB):
    @staticmethod
    def get(*args) -> User:
        if isinstance(args[0], str):
            stmt = select(User).where(User.login == args[0])
        else:
            stmt = select(User).where(User.id_user == args[0])

        with Session(engine) as session:
            return session.execute(stmt).scalars().first()

    @staticmethod
    def add(login: str, password: str) -> User:
        user = User(login=login, password=password, banned=False)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def delete(user) -> User:
        with Session(engine) as session:
            session.delete(user)
            session.commit()
        return True
