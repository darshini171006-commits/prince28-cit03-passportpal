"""Shared pytest fixtures for unit and integration tests."""

import asyncio
import os
import sys
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from passportpal.api.deps import (
    check_db,
    get_gateway,
    get_repo,
    get_usage_repo,
)
from passportpal.api.main import create_app
from passportpal.config import Settings
from passportpal.llm.gateway import FakeLLM, LLMGateway

# Tiny fake records: unit tests never touch a real database or data file.
SAMPLE = [
    {
        "id": "001",
        "title": "Alpha guideline",
        "year": 2023,
        "kind": "guideline",
    },
    {
        "id": "002",
        "title": "Beta circular",
        "year": 2024,
        "kind": "circular",
    },
    {
        "id": "003",
        "title": "Gamma notice",
        "year": 2025,
        "kind": "circular",
    },
    {
        "id": "PP001",
        "title": "Aarav passport guideline",
        "year": 2025,
        "kind": "guideline",
    },
]


class FakeRepo:
    """Behaves like DocumentRepository but keeps rows in a Python list."""

    def __init__(self, rows):
        self.rows = rows

    async def list(self, *, q, filters, limit, offset):
        rows = [
            row
            for row in self.rows
            if (not q or q.lower() in str(row).lower())
            and all(str(row.get(key)) == value for key, value in filters.items())
        ]

        return len(rows), rows[offset : offset + limit]

    async def get(self, external_id):
        return next(
            (row for row in self.rows if row["id"] == external_id),
            None,
        )


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use the Windows selector event loop when running on Windows."""
    if sys.platform == "win32":
        return asyncio.WindowsSelectorEventLoopPolicy()

    return asyncio.get_event_loop_policy()


@pytest.fixture
def settings():
    """Ignore the local .env file so unit tests behave consistently."""
    return Settings(
        app_env="ci",
        database_url="postgresql://localhost:5432/unused",
        _env_file=None,
    )


@pytest.fixture
def db_state():
    return {"up": True}


class FakeUsage:
    """Fake LLM usage repository for unit tests."""

    async def by_day(self, days=7):
        return [
            {
                "day": "2026-11-25",
                "calls": 3,
                "errors": 1,
                "fallbacks": 1,
                "tokens_in": 300,
                "tokens_out": 120,
                "cost_inr": 0.0642,
            }
        ]


@pytest.fixture
def llm():
    """Fake model used by /v1/chat unit tests."""
    return FakeLLM()


@pytest.fixture
def client(settings, db_state, llm) -> Iterator[TestClient]:
    """Create a test client with fake database and LLM dependencies."""
    app = create_app(settings)

    app.dependency_overrides[get_repo] = lambda: FakeRepo(SAMPLE)
    app.dependency_overrides[check_db] = lambda: db_state["up"]
    app.dependency_overrides[get_gateway] = lambda: LLMGateway([llm])
    app.dependency_overrides[get_usage_repo] = lambda: FakeUsage()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def database_url() -> str:
    """Return a safe test database URL for integration tests."""
    url = os.getenv("TEST_DATABASE_URL")

    if not url:
        pytest.fail(
            "TEST_DATABASE_URL is missing. Run integration tests using: uv run poe test-integration"
        )

    if not url.rstrip("/").endswith("/app_test"):
        pytest.fail("Safety check failed: TEST_DATABASE_URL must point to the app_test database.")

    return url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )
