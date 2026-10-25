from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import (
    String, Text, Integer, Numeric, DateTime, Computed, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from pgvector.sqlalchemy import Vector
from backend.app.db.base import Base
from backend.app.core.config import settings

if TYPE_CHECKING:
    from backend.app.models.saved_job import SavedJob
    from backend.app.models.feedback import Feedback


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_job_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    company: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # JSONB is chosen for required/preferred skills to allow containment filtering (@>)
    # and future metadata enrichment (e.g., years of experience per skill, weighting).
    required_skills: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_skills: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    experience_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    location: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    remote_policy: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)

    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), default="USD", nullable=True)

    application_url: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="synthetic_sample", nullable=False)

    # Vector embedding column for semantic search (384 dims by default for all-MiniLM-L6-v2)
    embedding = mapped_column(Vector(settings.EMBEDDING_DIM), nullable=True)

    # PostgreSQL Full-Text Search generated column, automatically persisted and updated on row change
    tsv: Mapped[Any] = mapped_column(
        TSVECTOR,
        Computed(
            "to_tsvector('english', coalesce(title, '') || ' ' || coalesce(company, '') || ' ' || coalesce(description, ''))",
            persisted=True
        ),
        nullable=True
    )

    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", index=True, nullable=False)

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

    # Relationships
    saved_by: Mapped[list[SavedJob]] = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")
    feedback: Mapped[list[Feedback]] = relationship("Feedback", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_jobs_tsv", "tsv", postgresql_using="gin"),
        Index("ix_jobs_required_skills", "required_skills", postgresql_using="gin"),
    )
