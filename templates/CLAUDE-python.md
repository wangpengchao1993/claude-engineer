# CLAUDE.md — Python Project Template

> Copy this to your Python project root and customize.

## Project Overview

<!-- Describe your project -->
[Project Name] is a [Python application/library/API] that [primary function].

## Tech Stack

- **Python**: 3.12+
- **Framework**: [FastAPI / Django / Flask / None]
- **Database**: [PostgreSQL / SQLite / MongoDB / None]
- **ORM**: [SQLAlchemy / Django ORM / Prisma / None]
- **Task Queue**: [Celery / None]
- **Package Manager**: [uv / pip / poetry / pdm]
- **Testing**: pytest
- **Linting**: ruff
- **Type Checking**: [mypy / pyright]

## Commands

```bash
# Environment
uv sync                      # Install dependencies
uv run python -m myapp       # Run the application

# Development
uv run fastapi dev           # Start dev server (FastAPI)
uv run python manage.py runserver  # Start dev server (Django)

# Testing
uv run pytest                # Run all tests
uv run pytest tests/unit/    # Run unit tests only
uv run pytest -x             # Stop on first failure
uv run pytest -k "test_name" # Run specific test
uv run pytest --cov          # Run with coverage

# Code Quality
uv run ruff check .          # Lint
uv run ruff check --fix .    # Lint and auto-fix
uv run ruff format .         # Format
uv run mypy src/             # Type check

# Database
uv run alembic upgrade head           # Run migrations
uv run alembic revision -m "desc"     # Create migration
```

## Architecture

```
src/myapp/
├── __init__.py
├── main.py          # Entry point
├── config.py        # Settings (loaded from env vars)
├── api/             # Route handlers / views
│   ├── __init__.py
│   ├── routes.py
│   └── deps.py      # Dependency injection
├── models/          # Database models
├── schemas/         # Pydantic schemas (request/response)
├── services/        # Business logic
├── repositories/    # Database queries
└── utils/           # Shared utilities

tests/
├── conftest.py      # Fixtures
├── factories.py     # Test data factories
├── unit/            # Unit tests
└── integration/     # Integration tests (require DB)
```

## Code Conventions

- Type hints on ALL function signatures (params + return)
- Docstrings: Google style for public functions
- `async def` for any I/O operation
- Use `Annotated[type, Depends()]` for dependency injection (FastAPI)
- Pydantic `BaseModel` for all data validation
- Custom exceptions in `src/myapp/exceptions.py`
- Structured logging with `structlog` (not print or stdlib logging)
- Tests follow arrange-act-assert pattern
- Use `pytest.mark.parametrize` for similar test cases

## Important Notes

- Never use `datetime.now()` — use `datetime.now(UTC)` or `datetime.utcnow()`
- Never use `float` for monetary values — use `Decimal`
- Never modify existing Alembic migration files
- Never import from tests in source code
- All environment variables loaded via `src/myapp/config.py` using pydantic-settings
- Use `pathlib.Path` instead of `os.path`
