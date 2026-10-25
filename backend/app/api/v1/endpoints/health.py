from datetime import datetime, timezone
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.db.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", status_code=status.HTTP_200_OK)
def get_health(db: Session = Depends(get_db)):
    """
    Health check endpoint verifying:
    1. Application liveness
    2. PostgreSQL database connectivity
    3. pgvector extension presence and version
    """
    db_status = "disconnected"
    pgvector_status = "missing"
    pgvector_version = None
    errors = []

    # 1. Check DB connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        errors.append(f"Database error: {str(e)}")

    # 2. Check pgvector extension
    if db_status == "connected":
        try:
            result = db.execute(
                text("SELECT installed_version FROM pg_available_extensions WHERE name = 'vector' AND installed_version IS NOT NULL")
            ).scalar()
            if result:
                pgvector_status = "installed"
                pgvector_version = result
            else:
                errors.append("pgvector extension is not installed in the database.")
        except Exception as e:
            logger.error(f"pgvector health check failed: {e}")
            errors.append(f"pgvector check error: {str(e)}")

    is_healthy = db_status == "connected" and pgvector_status == "installed"
    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    payload = {
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "pgvector": {
            "status": pgvector_status,
            "version": pgvector_version,
        },
    }
    if errors:
        payload["errors"] = errors

    return JSONResponse(status_code=status_code, content=payload)
