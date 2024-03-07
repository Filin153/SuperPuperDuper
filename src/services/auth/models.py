from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import select
from sqlalchemy.orm import Session

class AuthUser:
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(100), unique=True)
    password = Column(String(100))
    banned = Column(Boolean, default=False)

class AuthUserDB:
    def get(self, *args):
        if isinstance(args[0], str):
            stmt = select(self.model).where(self.model.login == args[0])
        else:
            stmt = select(self.model).where(self.model.id_user == args[0])

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().first()

    def add(self, login: str, password: str):
        user = self.model(login=login, password=password, banned=False)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user