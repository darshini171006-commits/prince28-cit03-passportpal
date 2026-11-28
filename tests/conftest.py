import asyncio
import os
import sys
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from passportpal.api.main import create_app
from passportpal.config import Settings


@pytest.fixture(scope="session")
def event_loop_policy():
    if sys.platform == "win32":
        return asyncio.WindowsSelectorEventLoopPolicy()

    return asyncio.get_event_loop_policy()


@pytest.fixture
def client() -> Iterator[TestClient]:
    settings = Settings(app_env="ci")
    app = create_app(settings=settings)

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def database_url() -> str:
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
