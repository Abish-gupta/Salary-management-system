"""Shared test fixtures for the Salary Management backend test suite.

This module provides:
- An in-memory SQLite engine (fast, isolated, no disk I/O)
- A per-test database session (rolled back or dropped after each test)
- A TestClient for API integration tests

Using in-memory SQLite means:
- Tests run in ~100ms
- No cleanup needed between runs
- Complete isolation — no test data leaks
"""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# ── In-memory SQLite engine ────────────────────────────────────────────────────
# "check_same_thread=False" is required because pytest may call fixtures from
# different threads. Safe here because tests are sequential.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Enable foreign key enforcement (SQLite disables it by default)
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_conn, _connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all database tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Session:
    """Provide a database session that rolls back after each test.

    Rolling back (rather than truncating tables) keeps tests fast and isolated.
    Each test starts with a clean slate.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    """Provide a FastAPI TestClient with the test database injected.

    Overrides the real `get_db` dependency so API tests never touch
    the production database.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
