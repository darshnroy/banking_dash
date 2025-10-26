# backend/db.py
from pymongo import MongoClient
from backend.config import settings

# MongoDB client
client = MongoClient(settings.MONGO_URL)  # <-- correct attribute name
db = client[settings.DB_NAME]

# Collections
users_col = db["users"]
transactions_col = db["transactions"]
