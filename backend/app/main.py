"""
FastAPI application entry point for the Fireflies.ai clone backend.

Creates the app instance, registers lifecycle hooks, and mounts API routes.
Run locally with:

    uvicorn app.main:app --reload --app-dir backend

Or from the `backend` directory:

    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Run startup and shutdown logic around the request loop.

    On startup we ensure database tables exist (no-op until models are added).
    """
    init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
