from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import bcrypt
import hashlib
from app.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # We pre-hash with SHA-256 to bypass bcrypt's 72-byte limit
    pwd_sha256 = hashlib.sha256(plain_password.encode('utf-8')).hexdigest().encode('utf-8')
    try:
        return bcrypt.checkpw(pwd_sha256, hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    pwd_sha256 = hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')
    return bcrypt.hashpw(pwd_sha256, bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
