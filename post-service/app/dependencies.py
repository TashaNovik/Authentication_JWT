import logging
import os

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from exceptions import TokenExpiredError, UserIdNotFoundError, InvalidSignatureError
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY_FILE = os.environ.get("SECRET_KEY_FILE")
if SECRET_KEY_FILE:
    with open(SECRET_KEY_FILE, "r") as f:
        SECRET_KEY = f.read().strip()
else:
    raise ValueError("Secret key file not found.")

ALGORITHM = "HS256"

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("user_id")
        if user_id is None:
            raise UserIdNotFoundError("User identifier ('user_id') not found in token")
        return user_id

    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError as e:
        raise InvalidSignatureError(f"Token signature or format is invalid: {e}")