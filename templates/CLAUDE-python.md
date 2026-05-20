# CLAUDE.md — Python Project Template / Python 项目模板

> Copy this to your Python project root and customize.
> 将此文件复制到 Python 项目根目录并进行自定义。

## Project Overview / 项目概述

<!-- Describe your project / 描述你的项目 -->
[Project Name] is a [Python application/library/API] that [primary function].

## Tech Stack / 技术栈

- **Python**: 3.12+
- **Framework / 框架**: [FastAPI / Django / Flask / None]
- **Database / 数据库**: [PostgreSQL / SQLite / MongoDB / None]
- **ORM / 对象关系映射**: [SQLAlchemy / Django ORM / Prisma / None]
- **Task Queue / 任务队列**: [Celery / None]
- **Package Manager / 包管理器**: [uv / pip / poetry / pdm]
- **Testing / 测试**: pytest
- **Linting / 代码检查**: ruff
- **Type Checking / 类型检查**: [mypy / pyright]

## Commands / 常用命令

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

## Architecture / 项目架构

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

## Code Conventions / 代码规范

- Type hints on ALL function signatures (params + return) — 所有函数签名必须有类型注解（参数和返回值）
- Docstrings: Google style for public functions — 文档字符串：公共函数使用 Google 风格
- `async def` for any I/O operation — 所有 I/O 操作使用 `async def`
- Use `Annotated[type, Depends()]` for dependency injection (FastAPI) — 使用 `Annotated[type, Depends()]` 进行依赖注入（FastAPI）
- Pydantic `BaseModel` for all data validation — 所有数据验证使用 Pydantic `BaseModel`
- Custom exceptions in `src/myapp/exceptions.py` — 自定义异常放在 `src/myapp/exceptions.py`
- Structured logging with `structlog` (not print or stdlib logging) — 使用 `structlog` 进行结构化日志记录（不用 print 或标准库 logging）
- Tests follow arrange-act-assert pattern — 测试遵循 arrange-act-assert 模式
- Use `pytest.mark.parametrize` for similar test cases — 相似测试用例使用 `pytest.mark.parametrize`

## Important Notes / 重要说明

- Never use `datetime.now()` — use `datetime.now(UTC)` or `datetime.utcnow()` — 禁止使用 `datetime.now()`，应使用 `datetime.now(UTC)` 或 `datetime.utcnow()`
- Never use `float` for monetary values — use `Decimal` — 禁止用 `float` 表示金额，应使用 `Decimal`
- Never modify existing Alembic migration files — 禁止修改已有的 Alembic 迁移文件
- Never import from tests in source code — 禁止在源代码中导入测试模块
- All environment variables loaded via `src/myapp/config.py` using pydantic-settings — 所有环境变量通过 `src/myapp/config.py` 使用 pydantic-settings 加载
- Use `pathlib.Path` instead of `os.path` — 使用 `pathlib.Path` 而非 `os.path`
