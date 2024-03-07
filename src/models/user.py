from sqlalchemy import Column, String, Integer, Boolean
from database.db import Base


class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(100), unique=True)
    password = Column(String(100))
    banned = Column(Boolean, default=False)

