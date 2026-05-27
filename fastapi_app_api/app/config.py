import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL:str = "sqlite+aiosqlite:///./fastapi_auth.db"
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRATION_MINUTES:int = 300
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7
    SECRET_KEY:str = os.getenv("SECRET_KEY")
    API_KEY:str = os.getenv("API_KEY")
    BASE_URL:str = os.getenv("BASE_URL")
    REDIS_URL:str = os.getenv("REDIS_URL", "redis://localhost:6379")


settings = Settings()
