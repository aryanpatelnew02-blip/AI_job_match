from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import setup_logging
from backend.app.core.middleware import RequestIDMiddleware
from backend.app.core.exceptions import register_exception_handlers
from backend.app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    setup_logging(settings.LOG_LEVEL)
    yield
    # Shutdown cleanup if needed


def create_application() -> FastAPI:
    app = FastAPI(
        title="AI Job Matching & Search Agent API",
        version="1.0.0",
        description="Backend API for AI Job Matching, Semantic Search, and Recommendation Agent",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)

    # Exception Handlers
    register_exception_handlers(app)

    # Routes
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_application()
