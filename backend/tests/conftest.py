import os
import sys
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.main import app
from backend.app.db.database import get_db


@pytest.fixture
def mock_db_session() -> Generator[MagicMock, None, None]:
    """Mock database session that simulates a healthy DB and pgvector extension."""
    mock_session = MagicMock(spec=Session)

    def mock_execute(query, *args, **kwargs):
        query_str = str(query)
        mock_result = MagicMock()
        if "SELECT 1" in query_str:
            mock_result.scalar.return_value = 1
        elif "pg_available_extensions" in query_str:
            mock_result.scalar.return_value = "0.7.0"
        else:
            mock_result.scalar.return_value = None
        return mock_result

    mock_session.execute.side_effect = mock_execute
    yield mock_session


@pytest.fixture
def client(mock_db_session: MagicMock) -> Generator[TestClient, None, None]:
    """Test client using overridden DB dependency with mock session."""
    app.dependency_overrides[get_db] = lambda: mock_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
