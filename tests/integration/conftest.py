"""Shared fixtures for PostgreSQL integration tests."""

import os

import pytest


@pytest.fixture
def database_url() -> str:
    """Return the dedicated integration-test database URL."""
    url = os.getenv("TEST_DATABASE_URL")

    if not url:
        pytest.fail(
            "TEST_DATABASE_URL is not configured. Set it to the PostgreSQL test database URL."
        )

    return url
