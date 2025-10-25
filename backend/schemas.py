# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# request / response models

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

class Transaction(BaseModel):
    id: Optional[str]
    user_id: str
    amount: float
    type: str  # 'credit' or 'debit'
    description: Optional[str] = None
    category: Optional[str] = None
    date: datetime

class TransactionsResponse(BaseModel):
    transactions: List[Transaction]
