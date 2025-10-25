# backend/main.py
from backend.config import settings

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.db import users_col, transactions_col
from backend.schemas import RegisterRequest, LoginRequest, Transaction, TransactionsResponse, UserResponse
from backend.auth import hash_password, verify_password, create_access_token, get_current_user
from backend.populate import ensure_demo_data
from datetime import timedelta

app = FastAPI(title="Banking Dashboard Demo")

# CORS: allow frontend local files and localhost dev server origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    ensure_demo_data()

@app.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest):
    if users_col.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_doc = {
        "username": payload.username,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
    }
    users_col.insert_one(user_doc)
    return UserResponse(id=str(user_doc.get("_id", "")), username=payload.username, email=payload.email)

@app.post("/login")
def login(payload: LoginRequest):
    user = users_col.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user": {"username": user["username"], "email": user["email"]}}

@app.get("/transactions", response_model=TransactionsResponse)
def get_transactions(current_user=Depends(get_current_user)):
    # Fetch transactions for user by email
    docs = list(transactions_col.find({"user_email": current_user["email"]}).sort("date", -1))
    txns = []
    for d in docs:
        txns.append({
            "id": str(d.get("_id")),
            "user_id": current_user["id"],
            "amount": d.get("amount", 0.0),
            "type": d.get("type", "debit"),
            "description": d.get("description"),
            "category": d.get("category"),
            "date": d.get("date")
        })
    return TransactionsResponse(transactions=txns)
