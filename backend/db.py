# backend/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.MONGO_DB]  # <- banking_dash

users_col = db["users"]
transactions_col = db["transactions"]
