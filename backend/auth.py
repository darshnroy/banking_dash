# backend/auth.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.config import settings
from backend.db import users_col

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str) -> str:
    # Bcrypt max 72 bytes, truncate safely for multibyte chars
    max_bytes = 72
    truncated = password.encode('utf-8')[:max_bytes].decode('utf-8', 'ignore')
    return pwd_context.hash(truncated)

def verify_password(plain: str, hashed: str) -> bool:
    max_bytes = 72
    truncated = plain.encode('utf-8')[:max_bytes].decode('utf-8', 'ignore')
    return pwd_context.verify(truncated, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = users_col.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return {"id": str(user["_id"]), "username": user["username"], "email": user["email"]}
