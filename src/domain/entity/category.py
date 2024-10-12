from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.domain.entity.base import BaseEntity
from src.domain.values.category import Name


@dataclass(kw_only=True)
class Category(BaseEntity):
    id: UUID = field(default_factory=uuid4)
    """Id категории"""
    name: Name
    """Название категории"""
    user_id: UUID
    """Id пользователя"""
