.PHONY: test coverage lint up down

test:
uv run pytest -v

coverage:
uv run pytest --cov=passportpal --cov-report=term-missing

lint:
uv run ruff check src tests

up:
docker-compose up --build -d

down:
docker-compose down
