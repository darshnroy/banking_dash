import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

MONGO_URI = os.getenv("MONGO_URI")  # get URI from environment variable
client = MongoClient(MONGO_URI)

db = client["banking_dash"]
users_col = db["users"]
transactions_col = db["transactions"]
