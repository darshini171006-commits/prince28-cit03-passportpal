"""One engine (a pool of connections) per app; one session per request."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from passportpal.config import Settings
from passportpal.db.url import to_asyncpg_url


def make_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        to_asyncpg_url(settings.database_url),
        pool_size=settings.db_pool_size,
        pool_pre_ping=True,
        pool_recycle=300,
    )


def make_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)
