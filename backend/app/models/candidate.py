from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.user import User


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False
    )
    resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # JSONB chosen over ARRAY because it supports structured items (projects with titles/bullets/links,
    # education with degrees/dates, skills with taxonomy tags) and GIN jsonb_path_ops indexing.
    skills: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    projects: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    education: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    experience_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

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

    user: Mapped[User] = relationship("User", back_populates="profile")
