from pydantic import BaseModel

class PostMessage(BaseModel):
    message: str