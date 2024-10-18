from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entity.user import User
from src.domain.values.user import Email, HashedPassword, Username
from src.infra.repositories.postgres.factories import Base
from src.infra.repositories.postgres.models.mixins import CreatedUpdatedMixin, UUIDMixin


class UserModel(UUIDMixin, CreatedUpdatedMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=Username(self.username),
            password=HashedPassword(self.password),
            email=Email(str(self.email)) if self.email else None,
        )
