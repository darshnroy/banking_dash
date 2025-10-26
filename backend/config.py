# backend/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL = "mongodb+srv://<USERNAME>:<PASSWORD>@<cluster-name>.mongodb.net/<DBNAME>?retryWrites=true&w=majority"

    DB_NAME: str = "banking_demo"
    JWT_SECRET: str = "change_this_secret_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day

    class Config:
        env_file = ".env"

settings = Settings()
