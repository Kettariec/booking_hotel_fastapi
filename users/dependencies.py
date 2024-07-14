import logging
from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from config import settings
from exceptions import (IncorrectTokenFormatException, TokenAbsentException,
                        TokenExpiredException, UserIsNotPresentException)
from users.dao import UserDAO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        logger.error("Token is absent in cookies")
        raise TokenAbsentException
    logger.info(f"Token from cookies: {token}")
    return token


async def get_current_user(token: str = Depends(get_token)):
    logger.info(f"Decoding token: {token}")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as e:
        logger.error(f"Incorrect token format: {e}")
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        logger.error("Token expired")
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        logger.error("User ID not present in token")
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise UserIsNotPresentException

    logger.info(f"Authenticated user: {user}")
    return user
