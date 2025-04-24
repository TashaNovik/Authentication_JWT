import logging
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from models import Message
from database import get_db
from dependencies import get_current_user_id
from schemas import PostMessage

logger = logging.getLogger(__name__)

posts_router = APIRouter(prefix="/posts", tags=["posts"])

@posts_router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostMessage, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    new_message = Message(user_id=user_id, message=post_data.message)
    db.add(new_message)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)
