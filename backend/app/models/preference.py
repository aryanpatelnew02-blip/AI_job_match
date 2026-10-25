from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.user import User


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False
    )

    preferred_roles: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_skills: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_locations: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    employment_types: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    work_arrangement: Mapped[str | None] = mapped_column(String(50), nullable=True)
    max_experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="preferences")
