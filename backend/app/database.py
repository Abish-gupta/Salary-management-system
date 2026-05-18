"""Database engine, session factory, and FastAPI dependency.

Design decisions:
- Single SQLite file by default (zero-config, per assessment guidance)
- `get_db` is a FastAPI dependency — injected into routes, easily overridden in tests
- `Base` is the declarative base all models inherit from
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator

from app.config import get_settings

settings = get_settings()

# ── Engine ─────────────────────────────────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    # Required for SQLite when used across threads (e.g. FastAPI async context)
    connect_args={"check_same_thread": False},
    # Reduces overhead for short-lived connections
    pool_pre_ping=True,
)


# Enable foreign key enforcement for SQLite (disabled by default in SQLite)
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_conn, _connection_record) -> None:
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ── Session factory ────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Declarative base ───────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


# ── FastAPI dependency ─────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after the request.

    Usage in routes:
        @router.get("/employees")
        def list_employees(db: Session = Depends(get_db)): ...

    Overridden in tests via `app.dependency_overrides[get_db] = override_get_db`.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all registered ORM tables.

    Called at application startup. Safe to call multiple times (CREATE IF NOT EXISTS).
    """
    Base.metadata.create_all(bind=engine)
