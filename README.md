# AI Job Matching & Search Agent

An AI-powered job discovery and recommendation platform featuring semantic search, deterministic multi-factor ranking, explainable LLM outputs, and an agentic conversational assistant with persistent memory.

---

## Prerequisites (Windows)

- **Python 3.12** (64-bit)
- **Docker Desktop** (running, with Docker Compose)
- **Node.js LTS** (v20+ or v22+) & **npm**
- **Git**

---

## Phase 1: Environment & Foundation Setup

### 1. Create and Activate Python Virtual Environment
Open PowerShell in the project root:
```powershell
# Create Python 3.12 virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 2. Install Backend Dependencies
```powershell
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables
```powershell
Copy-Item .env.example .env
```

### 4. Start PostgreSQL with pgvector via Docker Compose
The database is configured on port `5433` to prevent port collisions with any local PostgreSQL instance:
```powershell
docker compose up -d
```
Verify the container is healthy:
```powershell
docker compose ps
```

### 5. Run Database Migrations
Apply the initial schema including the `vector` extension and all 8 application tables:
```powershell
alembic upgrade head
```

### 6. Start the FastAPI Development Server
```powershell
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Verify Health Endpoint
In a separate PowerShell terminal:
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/v1/health | ConvertTo-Json
```
Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "pgvector": {
    "status": "installed",
    "version": "0.7.0"
  }
}
```

Interactive API documentation is available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 8. Run Automated Tests
```powershell
pytest backend/tests -v
```

### 9. Run Code Quality Checks (Ruff)
```powershell
ruff check .
```

---

## Database Architecture (Section 11)

All tables use SQLAlchemy 2.0 with PostgreSQL 16 + pgvector:

| Table | Primary Key | Description |
| :--- | :--- | :--- |
| `users` | UUID | User authentication accounts and system identities |
| `candidate_profiles` | UUID | Parsed resume, structured skills, projects, education |
| `jobs` | UUID | Job listings with `Vector(384)` and generated `tsvector` column |
| `user_preferences` | UUID | Persistent filters (roles, locations, work arrangements) |
| `conversations` | UUID | Multi-session chat threads |
| `messages` | UUID | Chat history with role and optional tool metadata |
| `saved_jobs` | UUID | Candidate saved bookmarks with unique constraint |
| `feedback` | UUID | Ground-truth relevance ratings (0/1/2) for evaluation |

*Note: JSONB is utilized for skills, projects, and metadata to support rich hierarchical schemas and GIN index queries without rigid migrations.*
