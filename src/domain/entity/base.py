from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.helpers import get_utc_now


@dataclass(kw_only=True)
class BaseEntity(ABC):
    created_at: datetime = field(default_factory=get_utc_now)
    updated_at: datetime = field(default_factory=get_utc_now)
