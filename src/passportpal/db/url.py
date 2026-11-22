"""Convert database URLs into asynchronous SQLAlchemy URLs."""

from sqlalchemy.engine import make_url

SYNC_POSTGRES_DRIVERS = {
    "postgres",
    "postgresql",
    "postgresql+psycopg",
    "postgresql+psycopg2",
}

SYNC_SQLITE_DRIVERS = {
    "sqlite",
    "sqlite+pysqlite",
}


def to_asyncpg_url(raw: str) -> str:
    """Convert synchronous or generic database URLs to async URLs."""
    url = make_url(raw)

    # SQLite async support
    if url.drivername in SYNC_SQLITE_DRIVERS:
        url = url.set(drivername="sqlite+aiosqlite")

    # PostgreSQL async support
    elif url.drivername in SYNC_POSTGRES_DRIVERS:
        url = url.set(drivername="postgresql+asyncpg")

        query = dict(url.query)

        sslmode = query.pop("sslmode", None)
        query.pop("channel_binding", None)

        if sslmode and sslmode != "disable":
            query["ssl"] = "require"

        url = url.set(query=query)

    return url.render_as_string(hide_password=False)
