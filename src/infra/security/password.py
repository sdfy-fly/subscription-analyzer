import bcrypt

from src.infra.security.base import BasePasswordHasher


class PasswordHasher(BasePasswordHasher):
    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=hashed_password)
