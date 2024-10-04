from dataclasses import dataclass

from src.domain.entity.base import BaseEntity
from src.domain.values.category import Name


@dataclass(kw_only=True)
class Category(BaseEntity):
    name: Name
    """Название категории"""
