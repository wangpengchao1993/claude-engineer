# CLAUDE.md Guide — Project Configuration Best Practices

> `CLAUDE.md` is the most powerful way to make Claude understand your project. This guide covers everything from basics to advanced patterns.

## Table of Contents

- [What is CLAUDE.md?](#what-is-claudemd)
- [How It Works](#how-it-works)
- [Essential Sections](#essential-sections)
- [Writing Effective Instructions](#writing-effective-instructions)
- [Advanced Patterns](#advanced-patterns)
- [Per-Directory Configuration](#per-directory-configuration)
- [Real-World Examples](#real-world-examples)
- [Common Mistakes](#common-mistakes)
- [Templates](#templates)

---

## What is CLAUDE.md?

`CLAUDE.md` is a special markdown file that Claude Code reads automatically at the start of every session. Think of it as a **project-level system prompt** — it tells Claude:

- What the project is and how it works
- Which commands to use for building, testing, and linting
- What coding conventions to follow
- What to avoid doing

**Impact**: A well-written `CLAUDE.md` can reduce the need for repetitive instructions by 80%+ and dramatically improve code quality.

---

## How It Works

### File Locations and Priority

Claude loads `CLAUDE.md` files from multiple locations, in this order:

| Location | Scope | When to Use |
|----------|-------|-------------|
| `~/.claude/CLAUDE.md` | Global (all projects) | Personal preferences, global tools |
| `./CLAUDE.md` | Project root | Project-specific config (commit to git) |
| `./src/CLAUDE.md` | Subdirectory | Module-specific overrides |
| `./.claude/CLAUDE.md` | Project (hidden) | Config you don't want to commit |

All files are merged — subdirectory files add to (not replace) parent files.

### What Gets Loaded When

- **Interactive mode**: All applicable CLAUDE.md files
- **Non-interactive (`-p`)**: Same as interactive
- **Subagents**: Inherit parent context including CLAUDE.md

---

## Essential Sections

Every CLAUDE.md should have these sections at minimum:

### 1. Project Overview

```markdown
## Project Overview
TaskFlow is a task management API built with FastAPI and PostgreSQL.
It serves the web frontend (React) and mobile apps (React Native).
The API follows REST conventions with JWT authentication.
```

**Why**: Claude needs to understand what it's working on. Without this, it guesses — often incorrectly.

### 2. Tech Stack

```markdown
## Tech Stack
- Python 3.12 with FastAPI
- PostgreSQL 16 with SQLAlchemy 2.0 (async)
- Alembic for migrations
- pytest for testing
- Ruff for linting and formatting
- Docker Compose for local development
```

**Why**: Prevents Claude from suggesting incompatible solutions (e.g., using sync SQLAlchemy when you use async).

### 3. Commands

```markdown
## Commands
- `make dev` — Start dev server (runs on port 8000)
- `make test` — Run all tests
- `make test-unit` — Run unit tests only
- `make test-integration` — Run integration tests (requires DB)
- `make lint` — Run ruff linter
- `make fmt` — Auto-format with ruff
- `make migrate` — Run database migrations
- `make migrate-create NAME=xxx` — Create new migration
```

**Why**: Claude needs to know exactly how to build, test, and lint your project. Wrong commands = wasted time.

### 4. Code Conventions

```markdown
## Code Conventions
- All functions must have type annotations
- Use async def for any I/O operation
- Docstrings: Google style, required for public functions
- Errors: raise custom exceptions from src/exceptions.py
- Logging: use structlog, not print() or stdlib logging
- Tests: arrange-act-assert pattern, descriptive names
```

**Why**: Without this, Claude uses generic conventions that may not match your team's style.

### 5. Architecture

```markdown
## Architecture
src/
├── api/          # FastAPI route handlers (thin layer)
├── services/     # Business logic (all logic goes here)
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas for request/response
├── repositories/  # Database queries (raw SQL or ORM)
├── middleware/    # Custom middleware
└── utils/        # Shared utilities

Tests mirror the src/ structure in tests/
```

**Why**: Claude knows where to find things and where to put new code.

---

## Writing Effective Instructions

### Be Specific, Not Vague

```markdown
# Bad — too vague
Follow best practices for error handling.

# Good — specific and actionable
Error handling rules:
- API endpoints: catch exceptions in route handlers, return appropriate HTTP status codes
- Services: raise domain-specific exceptions from src/exceptions.py
- Never catch broad Exception — catch specific types
- Always log errors with structlog before re-raising
- Include request_id in all error logs
```

### Use Imperative Statements

```markdown
# Bad — passive/suggestive
It would be nice if tests were written for new features.

# Good — clear directive
Write tests for all new features. Place test files in tests/ mirroring the src/ structure.
Run `make test` to verify before considering the task complete.
```

### Include the "Why" for Non-Obvious Rules

```markdown
## Important Notes
- Never use `datetime.now()` — use `datetime.utcnow()` instead
  (the server runs in multiple timezones, local time causes bugs)
- Always use `Decimal` for money amounts, never `float`
  (we had a billing incident from float rounding in 2024)
```

### Keep It Scannable

Claude reads the entire file, but well-structured content works better:

```markdown
## API Conventions
- **Versioning**: All endpoints under `/api/v1/`
- **Auth**: JWT Bearer token required except `/health` and `/auth/login`
- **Pagination**: Use `?page=1&per_page=20`, max 100 per page
- **Errors**: Return `{"error": {"code": "...", "message": "..."}}`
- **Naming**: kebab-case for URLs, snake_case for JSON fields
```

---

## Advanced Patterns

### Conditional Instructions

Use headings to scope instructions to specific areas:

```markdown
## When Working on API Routes
- Follow the existing pattern in src/api/
- Always add OpenAPI descriptions to endpoints
- Validate request bodies with Pydantic schemas

## When Working on Database Models
- Run `make migrate-create NAME=descriptive_name` after model changes
- Never modify existing migration files
- Add indexes for columns used in WHERE clauses

## When Writing Tests
- Use fixtures from tests/conftest.py
- Integration tests must use the test database (not mocks)
- Reset database state between tests with the `clean_db` fixture
```

### Environment-Specific Notes

```markdown
## Local Development
- Run `docker-compose up -d` before starting the app (starts PostgreSQL and Redis)
- The API runs on http://localhost:8000
- Swagger docs at http://localhost:8000/docs
- Hot reload is enabled by default

## CI/CD
- Tests run on GitHub Actions (see .github/workflows/)
- Deploy is automatic on merge to main
- Staging: api-staging.example.com
- Production: api.example.com
```

### Team-Specific Conventions

```markdown
## PR Conventions
- Title format: `feat(scope): description` or `fix(scope): description`
- Always include a test plan in the PR description
- Request review from the relevant team lead
- Squash merge only — no merge commits

## Git
- Branch naming: `feat/description`, `fix/description`, `chore/description`
- Commit messages: conventional commits format
- Never force push to main or develop
```

### Excluding Areas

```markdown
## Do Not Modify
- `src/generated/` — auto-generated code, will be overwritten
- `migrations/versions/` — never edit existing migrations
- `.env.production` — production secrets, not for local use
- `vendor/` — vendored dependencies, update via script only
```

---

## Per-Directory Configuration

Use subdirectory `CLAUDE.md` files for module-specific context:

### Example: `src/api/CLAUDE.md`

```markdown
# API Routes

All route handlers in this directory follow this pattern:

1. Validate input (Pydantic does this automatically)
2. Call the appropriate service function
3. Transform the service result into a response schema
4. Return with appropriate status code

Route handlers should be thin — no business logic here.
All business logic belongs in src/services/.

Example:
```python
@router.post("/users", status_code=201)
async def create_user(
    body: CreateUserRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.create_user(body)
    return UserResponse.from_orm(user)
```
```

### Example: `tests/CLAUDE.md`

```markdown
# Tests

- Use pytest fixtures from conftest.py
- Factory functions are in tests/factories.py
- Test database is configured in tests/conftest.py
- Run specific test: `pytest tests/path/to/test.py::test_name -v`
- All test functions must start with `test_`
- Use `@pytest.mark.integration` for tests that need the database
```

---

## Real-World Examples

### Full-Stack Web App

```markdown
# CLAUDE.md — E-Commerce Platform

## Overview
Full-stack e-commerce platform with Next.js frontend and Node.js/Express backend.
Monorepo managed with Turborepo.

## Tech Stack
- Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS
- Backend: Express.js, TypeScript, Prisma ORM
- Database: PostgreSQL 15
- Cache: Redis
- Queue: BullMQ
- Monorepo: Turborepo with pnpm workspaces

## Packages
- `apps/web` — Customer-facing storefront
- `apps/admin` — Admin dashboard
- `apps/api` — Backend API
- `packages/ui` — Shared UI components
- `packages/db` — Prisma schema and client
- `packages/types` — Shared TypeScript types

## Commands
- `pnpm dev` — Start all apps in dev mode
- `pnpm build` — Build all packages
- `pnpm test` — Run all tests
- `pnpm lint` — Lint all packages
- `pnpm db:migrate` — Run Prisma migrations
- `pnpm db:seed` — Seed the database
- Working in a specific package: `pnpm --filter @app/api test`

## Conventions
- Functional components with hooks (no class components)
- Server Components by default in Next.js, "use client" only when needed
- API routes return `{ data: T }` on success, `{ error: { message, code } }` on failure
- Use Zod for all runtime validation
- Prefer named exports over default exports
```

### CLI Tool

```markdown
# CLAUDE.md — mycli

## Overview
A CLI tool for managing cloud deployments, written in Rust.

## Tech Stack
- Rust 1.78+
- clap for argument parsing
- tokio for async runtime
- reqwest for HTTP
- serde for serialization

## Commands
- `cargo build` — Build debug binary
- `cargo test` — Run all tests
- `cargo run -- <args>` — Run the CLI
- `cargo clippy` — Run linter
- `cargo fmt` — Format code

## Architecture
src/
├── main.rs        # Entry point, CLI argument parsing
├── commands/      # One module per subcommand
├── api/           # Cloud provider API clients
├── config/        # Configuration file handling
├── output/        # Output formatting (table, json, yaml)
└── error.rs       # Error types (use thiserror)

## Conventions
- All public functions have doc comments
- Error handling: use `anyhow::Result` in main, `thiserror` for library errors
- CLI output: support --format json|table|yaml on all commands
- Tests: unit tests in the same file (#[cfg(test)] mod), integration tests in tests/
```

---

## Common Mistakes

### 1. Too Much Detail

```markdown
# Bad — Claude doesn't need a novel
This project was started in 2019 by the founding team when we realized
that our existing solution wasn't scaling well. After evaluating several
options including Django, Rails, and Express, we chose FastAPI because...

# Good — just the facts
## Overview
Task management API. FastAPI + PostgreSQL. Serves web and mobile clients.
```

### 2. Outdated Information

If your CLAUDE.md says `npm test` but your project uses `pnpm test`, Claude will run the wrong command. **Keep it current.**

### 3. Contradicting the Code

Don't write conventions that your codebase doesn't actually follow. Claude will see the contradiction and get confused. Either update your code or your CLAUDE.md.

### 4. Missing Commands

The #1 most impactful section is **Commands**. If Claude doesn't know how to run tests or lint, it either guesses or skips them.

### 5. Ignoring the File

Many developers create a CLAUDE.md once and forget it. Treat it like documentation — update it when your project evolves.

---

## Templates

We provide ready-to-use templates for common project types:

- [Universal Template](../../templates/CLAUDE.md) — Works for any project
- [Python Template](../../templates/CLAUDE-python.md) — Python/FastAPI/Django
- [TypeScript Template](../../templates/CLAUDE-typescript.md) — TypeScript/Node.js/React
- [Rust Template](../../templates/CLAUDE-rust.md) — Rust projects

---

<p align="center">
  <strong>Next:</strong> <a href="04-hooks-and-automation.md">Hooks & Automation</a> — Automate your workflows
</p>

---

## Context Window Practical Strategies

Different context window sizes call for different CLAUDE.md approaches.

### 200K Window (Default)

Context is precious — keep CLAUDE.md lean:
- Target **200-500 lines**
- Only write what AI can't infer from code (constraints, conventions, commands)
- Don't write what AI can figure out (tech stack, file structure)
- Use `/compact` proactively — when Claude's responses start degrading or slowing down

### 1M Window (Bedrock/Vertex)

Context is abundant — CLAUDE.md can be richer:
- Can expand to **1000-3000 lines**
- Can include architecture decision rationale ("why X over Y")
- Can include code examples ("good code looks like this")
- `/compact` frequency drops significantly

### When to /compact

| Signal | Time to /compact? |
|--------|--------------------|
| Claude starts repeating earlier points | Yes |
| Response quality noticeably drops | Yes |
| `/cost` shows tokens near limit | Yes |
| Just finished a feature, starting the next one | Yes (clean context) |

---

[← Previous: Claude Code Mastery](02-claude-code-mastery.md) | [Table of Contents](../../README.md) | [Next: Hooks & Automation →](04-hooks-and-automation.md)
