from fastapi import FastAPI
from auth_api import auth_router

app = FastAPI()

app.include_router(auth_router)