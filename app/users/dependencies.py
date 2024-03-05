from datetime import datetime

from jose import JWTError, jwt
from fastapi import Request, Depends
from app.config import settings
from app.exceptions import TokenNotExistException, TokenExpiredException, InvalidTokenException, UserIsNotPresent
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenNotExistException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
                token, settings.SECRET_KEY, settings.ALGORITHM
            )
    except JWTError:
        raise InvalidTokenException

    expire : str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresent
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresent

    return user
