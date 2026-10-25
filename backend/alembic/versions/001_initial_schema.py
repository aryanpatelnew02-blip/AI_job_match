"""initial schema with pgvector and all section 11 tables

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-25 19:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from pgvector.sqlalchemy import Vector
from backend.app.core.config import settings

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. Table: users
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # 3. Table: candidate_profiles
    op.create_table(
        "candidate_profiles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("resume_text", sa.Text(), nullable=True),
        sa.Column("skills", JSONB(), nullable=False, server_default="[]"),
        sa.Column("projects", JSONB(), nullable=False, server_default="[]"),
        sa.Column("education", JSONB(), nullable=False, server_default="[]"),
        sa.Column("experience_level", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_candidate_profiles_user_id", "candidate_profiles", ["user_id"], unique=True)

    # 4. Table: jobs
    op.create_table(
        "jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("source_job_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("company", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("required_skills", JSONB(), nullable=False, server_default="[]"),
        sa.Column("preferred_skills", JSONB(), nullable=False, server_default="[]"),
        sa.Column("experience_min", sa.Integer(), nullable=True),
        sa.Column("experience_max", sa.Integer(), nullable=True),
        sa.Column("experience_level", sa.String(50), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("remote_policy", sa.String(50), nullable=True),
        sa.Column("employment_type", sa.String(50), nullable=True),
        sa.Column("salary_min", sa.Numeric(12, 2), nullable=True),
        sa.Column("salary_max", sa.Numeric(12, 2), nullable=True),
        sa.Column("currency", sa.String(10), nullable=True, server_default="USD"),
        sa.Column("application_url", sa.Text(), nullable=False),
        sa.Column("source", sa.String(100), nullable=False, server_default="synthetic_sample"),
        sa.Column("embedding", Vector(settings.EMBEDDING_DIM), nullable=True),
        sa.Column(
            "tsv",
            TSVECTOR(),
            sa.Computed(
                "to_tsvector('english', coalesce(title, '') || ' ' || coalesce(company, '') || ' ' || coalesce(description, ''))",
                persisted=True
            ),
            nullable=True
        ),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_jobs_source_job_id", "jobs", ["source_job_id"], unique=True)
    op.create_index("ix_jobs_title", "jobs", ["title"])
    op.create_index("ix_jobs_company", "jobs", ["company"])
    op.create_index("ix_jobs_location", "jobs", ["location"])
    op.create_index("ix_jobs_remote_policy", "jobs", ["remote_policy"])
    op.create_index("ix_jobs_employment_type", "jobs", ["employment_type"])
    op.create_index("ix_jobs_status", "jobs", ["status"])
    op.create_index("ix_jobs_tsv", "jobs", ["tsv"], postgresql_using="gin")
    op.create_index("ix_jobs_required_skills", "jobs", ["required_skills"], postgresql_using="gin")

    # 5. Table: user_preferences
    op.create_table(
        "user_preferences",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("preferred_roles", JSONB(), nullable=False, server_default="[]"),
        sa.Column("preferred_skills", JSONB(), nullable=False, server_default="[]"),
        sa.Column("preferred_locations", JSONB(), nullable=False, server_default="[]"),
        sa.Column("employment_types", JSONB(), nullable=False, server_default="[]"),
        sa.Column("work_arrangement", sa.String(50), nullable=True),
        sa.Column("max_experience_years", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_user_preferences_user_id", "user_preferences", ["user_id"], unique=True)

    # 6. Table: conversations
    op.create_table(
        "conversations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_conversations_user_id", "conversations", ["user_id"])

    # 7. Table: messages
    op.create_table(
        "messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", UUID(as_uuid=True), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata_json", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])

    # 8. Table: saved_jobs
    op.create_table(
        "saved_jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", UUID(as_uuid=True), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "job_id", name="uq_user_saved_job"),
    )
    op.create_index("ix_saved_jobs_user_id", "saved_jobs", ["user_id"])
    op.create_index("ix_saved_jobs_job_id", "saved_jobs", ["job_id"])

    # 9. Table: feedback
    op.create_table(
        "feedback",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("job_id", UUID(as_uuid=True), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relevance_rating", sa.Integer(), nullable=False),
        sa.Column("feedback_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_feedback_user_id", "feedback", ["user_id"])
    op.create_index("ix_feedback_job_id", "feedback", ["job_id"])


def downgrade() -> None:
    op.drop_table("feedback")
    op.drop_table("saved_jobs")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("user_preferences")
    op.drop_table("jobs")
    op.drop_table("candidate_profiles")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS vector;")
