from passlib.context import CryptContext
from jose import jwt, JWTError
from ..core.config import settings
from datetime import datetime, timezone, timedelta
from uuid import UUID


crypt = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return crypt.hash(password)

def verify_password(password: str, hash_pass: str) -> bool:
    return crypt.verify(password, hash_pass)

# создание access-токена
def create_access_token(user_id: UUID) -> str:
    time = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    access_token = jwt.encode({"sub": str(user_id), "exp": time, "type": "access"},
                              algorithm=settings.jwt.algorithms,
                              key=settings.jwt.secret_key)
    return access_token

# Создание refresh-токена
def create_refresh_token(user_id: UUID) -> str:
    time = datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expire_days)
    refresh_token = jwt.encode({"sub": str(user_id), "exp": time, "type": "refresh"},
                              algorithm=settings.jwt.algorithms,
                              key=settings.jwt.secret_key)
    return refresh_token

# Декодинг токена
def decode_token(token: str) -> dict | None:
    try:
        decode_t = jwt.decode(token,
                              key=settings.jwt.secret_key,
                              algorithms=[settings.jwt.algorithms])
        return decode_t
    except JWTError:
        return None