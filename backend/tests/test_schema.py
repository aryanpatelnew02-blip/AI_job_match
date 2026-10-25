import uuid
from backend.app.models import (
    Base,
    User,
    CandidateProfile,
    Job,
    UserPreference,
    Conversation,
    Message,
    SavedJob,
    Feedback,
)
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR


def test_all_models_registered_in_metadata():
    """Verify all 8 Section 11 tables are properly registered in SQLAlchemy metadata."""
    expected_tables = {
        "users",
        "candidate_profiles",
        "jobs",
        "user_preferences",
        "conversations",
        "messages",
        "saved_jobs",
        "feedback",
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables), f"Missing tables: {expected_tables - actual_tables}"


def test_job_model_columns_and_vector():
    """Verify Job model has the required vector and generated tsvector columns."""
    jobs_table = Base.metadata.tables["jobs"]

    assert "embedding" in jobs_table.columns
    assert isinstance(jobs_table.columns["embedding"].type, Vector)
    assert jobs_table.columns["embedding"].type.dim == 384

    assert "tsv" in jobs_table.columns
    assert isinstance(jobs_table.columns["tsv"].type, TSVECTOR)
    assert jobs_table.columns["tsv"].computed is not None
    assert jobs_table.columns["tsv"].computed.persisted is True


def test_unique_constraints():
    """Verify unique constraints across user, job, and saved_jobs tables."""
    saved_jobs_table = Base.metadata.tables["saved_jobs"]
    constraints = [c.name for c in saved_jobs_table.constraints]
    assert "uq_user_saved_job" in constraints

    users_table = Base.metadata.tables["users"]
    email_col = users_table.columns["email"]
    assert email_col.unique is True or any(
        idx.unique and "email" in [c.name for c in idx.columns]
        for idx in users_table.indexes
    )


def test_model_instantiation():
    """Verify all models can be instantiated with valid attributes."""
    user_id = uuid.uuid4()
    job_id = uuid.uuid4()
    conv_id = uuid.uuid4()

    user = User(id=user_id, email="test@example.com")
    assert user.id == user_id
    assert user.email == "test@example.com"

    profile = CandidateProfile(
        user_id=user_id,
        skills=["Python", "FastAPI"],
        projects=[{"title": "Search Engine"}],
        education=[{"degree": "B.S. CS"}],
        experience_level="entry-level",
    )
    assert profile.user_id == user_id
    assert len(profile.skills) == 2

    job = Job(
        id=job_id,
        source_job_id="test_001",
        title="AI Engineer",
        company="Example Corp",
        description="Build LLM agents",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        application_url="https://jobs.example.invalid/1",
    )
    assert job.source_job_id == "test_001"
    assert job.company == "Example Corp"

    pref = UserPreference(
        user_id=user_id,
        preferred_roles=["AI Engineer"],
        preferred_skills=["Python"],
        preferred_locations=["Remote"],
        employment_types=["full-time"],
    )
    assert pref.user_id == user_id

    conv = Conversation(id=conv_id, user_id=user_id, title="Job Search")
    assert conv.user_id == user_id

    msg = Message(conversation_id=conv_id, role="user", content="Find Python jobs")
    assert msg.conversation_id == conv_id

    saved = SavedJob(user_id=user_id, job_id=job_id)
    assert saved.job_id == job_id

    fb = Feedback(user_id=user_id, job_id=job_id, relevance_rating=2, feedback_reason="Great match")
    assert fb.relevance_rating == 2
