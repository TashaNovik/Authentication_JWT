from fastapi import Request, FastAPI, status, Response
import logging
from exceptions import TokenExpiredError, UserIdNotFoundError, InvalidSignatureError, InvalidTokenError, AuthError
from posts_api import posts_router

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(posts_router)

# Обработчик для истекшего токена и отсутствия user_id
@app.exception_handler(TokenExpiredError)
@app.exception_handler(UserIdNotFoundError)
async def handle_token_auth_error(request: Request, exc: AuthError):
    logger.warning(f"Authentication failed (401): {exc.detail}")
    return Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": f"Bearer error=\"{exc.detail}\""}
    )

# Обработчик для неверной подписи/формата
@app.exception_handler(InvalidSignatureError)
async def handle_invalid_signature_error(request: Request, exc: InvalidSignatureError):
    logger.warning(f"Token validation failed: {exc.detail}")
    return Response(status_code=status.HTTP_400_BAD_REQUEST)

# Обработчик для отсутствия/неверного заголовка Authorization
@app.exception_handler(InvalidTokenError)
async def handle_invalid_token_generic(request: Request, exc: InvalidTokenError):
     logger.warning(f"Invalid token: {exc.detail}")
     headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
     return Response(status_code=exc.status_code, headers=headers)