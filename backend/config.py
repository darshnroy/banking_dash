# backend/config.py
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    MONGO_USER: str = "darshanroy35_db_user"
    MONGO_PASS: str = quote_plus("yBV0DruY2dKITszN")
    MONGO_DB: str = "banking_dash"  # <- changed here
    CLUSTER: str = "cluster0.x86qxeb.mongodb.net"
    
    MONGO_URL: str = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"
    
    JWT_SECRET: str = "change_this_secret_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day

    class Config:
        env_file = ".env"

settings = Settings()
