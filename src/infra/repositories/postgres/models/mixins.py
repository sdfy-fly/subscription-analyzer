from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.helpers import get_utc_now


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True)


class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
