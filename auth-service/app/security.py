import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# Настройки JWT (из переменной окружения)
SECRET_KEY_FILE = os.environ.get("SECRET_KEY_FILE")
if SECRET_KEY_FILE:
    with open(SECRET_KEY_FILE, "r") as f:
        SECRET_KEY = f.read().strip()
else:
    raise ValueError("Secret key file not found.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info("Token created")
    return encoded_jwt


def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError: # Ловим общую ошибку JWT (включая ExpiredSignatureError)
        return None