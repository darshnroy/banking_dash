# backend/populate.py
from backend.db import users_col, transactions_col
from backend.auth import hash_password
from datetime import datetime, timedelta
import uuid

def ensure_demo_data():
    # Create demo user if not exists
    demo_email = "demo@example.com"
    if not users_col.find_one({"email": demo_email}):
        users_col.insert_one({
            "username": "demo_user",
            "email": demo_email,
            "hashed_password": hash_password("demo1"),
        })
    # Ensure another user
    alice_email = "alice@example.com"
    if not users_col.find_one({"email": alice_email}):
        users_col.insert_one({
            "username": "alice",
            "email": alice_email,
            "hashed_password": hash_password("alicepass"),
        })

    # If there are no transactions, insert some for each user
    if transactions_col.count_documents({}) == 0:
        users = list(users_col.find({}))
        for user in users:
            for i in range(6):
                t = {
                    "user_email": user["email"],
                    "amount": round((i+1) * (10.5 + i), 2),
                    "type": "credit" if i % 2 == 0 else "debit",
                    "description": f"Sample txn {i+1}",
                    "category": "Salary" if i % 2 == 0 else "Shopping",
                    "date": (datetime.utcnow() - timedelta(days=i)).isoformat()
                }
                transactions_col.insert_one(t)

if __name__ == "__main__":
    ensure_demo_data()
