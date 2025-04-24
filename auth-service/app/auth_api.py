import logging
import re
from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import Token
from security import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

logger = logging.getLogger(__name__)

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if not email_regex.match(user_data.username):
        logger.warning("Invalid email format")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
    if len(user_data.password) < 6:
        logger.warning("Password too short")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
    existing_user = db.query(User).filter(User.email == user_data.username).first()
    if existing_user:
        logger.warning("Email already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)


@auth_router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        logger.warning("User not found")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(form_data.password, user.password_hash):
        logger.warning("Invalid password")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )

    logger.info("Token created")
    return Token(access_token=access_token, token_type="bearer")