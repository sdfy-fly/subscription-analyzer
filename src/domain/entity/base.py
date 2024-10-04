from dataclasses import dataclass, field
from datetime import datetime

from src.domain.helpers import get_utc_now


@dataclass(kw_only=True)
class BaseEntity:
    created_at: datetime = field(default_factory=get_utc_now)
    """Дата создания"""
    updated_at: datetime = field(default_factory=get_utc_now)
    """Дата обновления"""
