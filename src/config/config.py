import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{pathlib.Path(__file__).parent.resolve()}/.env',
                                      env_file_encoding='utf-8')
    # database
    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: int
    pg_db_name: str
    database_url: str = ""

    debug: bool

    # JWT auth
    secret_key: str
    algorithm: str
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def new_setting():
    set = Settings()
    if set.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO, filename="logs.log")

    set.database_url = f"postgresql+psycopg2://{set.pg_user}:{set.pg_pass}@{set.pg_host}:{set.pg_port}/{set.pg_db_name}"
    return set


tmp = Jinja2Templates(directory="templates")
settings = new_setting()
logging.debug(settings.__dict__)
