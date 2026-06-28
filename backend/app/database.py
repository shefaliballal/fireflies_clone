"""
SQLAlchemy database setup for the Fireflies clone backend.

This module owns the engine, declarative Base, session factory, and the FastAPI
dependency that yields a database session per request. Route handlers inject
`Session` via `Depends(get_db)`; sessions are always closed after the request.

Models will inherit from `Base` and be registered in a separate `models` package.
Call `init_db()` once at startup to create tables when models exist.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

# SQLite requires check_same_thread=False when used with FastAPI's thread pool.
connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy ORM models."""


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a transactional database session.

    Yields a session for the duration of a single request, then closes it
    whether the handler succeeds or raises.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all tables defined on `Base.metadata`.

    Imports ORM models first so they register with `Base` before `create_all`.
    """
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
