# backend/db.py
from pymongo import MongoClient
from backend.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# collections
users_col = db["users"]
transactions_col = db["transactions"]
