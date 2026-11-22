
# syntax=docker/dockerfile:1

# ---------- Stage 1: Build virtual environment ----------
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy application source
COPY . /app

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

RUN groupadd --system app && \
    useradd --system --gid app --home-dir /app --no-create-home app

WORKDIR /app

# Copy virtual environment
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy Alembic configuration
COPY --from=builder --chown=app:app /app/alembic.ini ./alembic.ini
COPY --from=builder --chown=app:app /app/alembic ./alembic

# Copy application folders
COPY --from=builder --chown=app:app /app/src ./src
COPY --from=builder --chown=app:app /app/migrations ./migrations
COPY --from=builder --chown=app:app /app/data ./data

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn passportpal.api.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8000} --no-access-log"]
