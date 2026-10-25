from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.candidate import CandidateProfile
    from backend.app.models.preference import UserPreference
    from backend.app.models.conversation import Conversation
    from backend.app.models.saved_job import SavedJob
    from backend.app.models.feedback import Feedback


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    profile: Mapped[CandidateProfile] = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    preferences: Mapped[UserPreference] = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversations: Mapped[list[Conversation]] = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    saved_jobs: Mapped[list[SavedJob]] = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    feedback: Mapped[list[Feedback]] = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
