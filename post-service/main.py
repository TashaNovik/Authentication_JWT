import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Message


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY_FILE = os.environ.get("SECRET_KEY_FILE")
if SECRET_KEY_FILE:
    with open(SECRET_KEY_FILE, "r") as f:
        SECRET_KEY = f.read().strip()
else:
    raise ValueError("Secret key file not found.")
ALGORITHM = "HS256"


Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class PostMessage(BaseModel):
    message: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

    except JWTError as e:
        print(e)  # For better debugging
        raise credentials_exception
    except Exception as e:
        print(e)

    return user_id



@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostMessage, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    new_message = Message(user_id=user_id, message=post_data.message)
    db.add(new_message)
    db.commit()
    return {"message": "Post created successfully"}