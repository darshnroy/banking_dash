# backend/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb+srv://darshanroy35_db_user:yBV0DruY2dKITszN@cluster0.x86qxeb.mongodb.net/?appName=Cluster0"
    DB_NAME: str = "banking_demo"
    JWT_SECRET: str = "change_this_secret_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day

    class Config:
        env_file = ".env"

settings = Settings()
