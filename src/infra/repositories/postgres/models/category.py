from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entity.category import Category
from src.domain.values.category import Name
from src.infra.repositories.postgres.factories import Base
from src.infra.repositories.postgres.models.mixins import CreatedUpdatedMixin, UUIDMixin
from src.infra.repositories.postgres.models.user import UserModel


class CategoryModel(UUIDMixin, CreatedUpdatedMixin, Base):
    __tablename__ = 'categories'

    name: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped[UserModel] = relationship('UserModel')

    __table_args__ = (UniqueConstraint('name', 'user_id', name='idx_category_name_user_id_uniq'),)

    def to_entity(self) -> Category:
        return Category(
            id=self.id,
            name=Name(self.name),
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
