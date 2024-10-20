from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from punq import Container
from starlette import status

from src.core.container import get_container
from src.infra.exceptions.security import InvalidJwt
from src.infra.security.base import BaseTokenManager


http_bearer = HTTPBearer()


async def get_user_id_by_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer), container: Container = Depends(get_container)
) -> UUID:
    token = credentials.credentials
    manager: BaseTokenManager = container.resolve(BaseTokenManager)
    try:
        user_id = manager.verify_token(token)
    except InvalidJwt as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

    return user_id
