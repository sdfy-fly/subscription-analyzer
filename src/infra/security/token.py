from dataclasses import dataclass
from uuid import UUID

import jwt
from jwt import PyJWTError

from src.core.settings import settings
from src.domain.helpers import get_utc_now
from src.infra.exceptions.security import InvalidJwt
from src.infra.security.base import BaseTokenManager


@dataclass
class JwtTokenManager(BaseTokenManager):
    def create_token(self, user_id: UUID) -> str:
        now = get_utc_now()
        payload = {'sub': str(user_id), 'iat': now, 'exp': now + settings.jwt.ttl}
        return jwt.encode(payload=payload, key=settings.jwt.key, algorithm=settings.jwt.algorithm)

    def verify_token(self, token: str) -> UUID:
        try:
            payload: dict = jwt.decode(jwt=token, algorithms=[settings.jwt.algorithm], key=settings.jwt.key)
        except PyJWTError as e:
            raise InvalidJwt from e

        user_id = UUID(payload['sub'])
        return user_id
