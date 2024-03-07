from sqlalchemy import create_engine
from config.config import settings
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(settings.database_url)
Base = declarative_base()

class BaseDB:
    def get(self):
        raise NotImplementedError(f"Not implemented in {self.__class__}")

    def add(self):
        raise NotImplementedError(f"Not implemented in {self.__class__}")

    def delete(self):
        raise NotImplementedError(f"Not implemented in {self.__class__}")
