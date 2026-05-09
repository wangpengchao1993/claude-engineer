# CLAUDE.md — Universal Project Template

> Copy this file to the root of your project and customize it.
> Claude Code will automatically read this file for project context.

## Project Overview

<!-- Describe what this project does in 1-2 sentences -->
[Project Name] is a [type of application] that [primary function].

## Tech Stack

- **Language**: [e.g., Python 3.12, TypeScript 5.x]
- **Framework**: [e.g., FastAPI, Next.js 14, Axum]
- **Database**: [e.g., PostgreSQL, SQLite, MongoDB]
- **Package Manager**: [e.g., uv, pnpm, cargo]
- **Testing**: [e.g., pytest, vitest, cargo test]
- **CI/CD**: [e.g., GitHub Actions]

## Commands

<!-- List the most frequently used commands -->
```bash
# Development
[command]        # Start development server

# Testing
[command]        # Run all tests
[command]        # Run specific test file
[command]        # Run tests with coverage

# Code Quality
[command]        # Run linter
[command]        # Auto-format code
[command]        # Type checking

# Build & Deploy
[command]        # Build for production
[command]        # Deploy
```

## Architecture

<!-- Describe the project structure and key directories -->
```
src/
├── [dir]/       # [Description]
├── [dir]/       # [Description]
├── [dir]/       # [Description]
└── [dir]/       # [Description]
tests/           # Test files (mirror src/ structure)
```

## Code Conventions

<!-- List the coding standards Claude should follow -->
- [Convention 1, e.g., "Use functional components with hooks"]
- [Convention 2, e.g., "All functions must have type annotations"]
- [Convention 3, e.g., "Use descriptive variable names, no abbreviations"]
- [Convention 4, e.g., "Error handling: use Result types, not exceptions"]

## Important Patterns

<!-- Describe patterns Claude should follow when generating code -->
- **Error Handling**: [How errors should be handled]
- **Logging**: [Logging conventions and levels]
- **API Responses**: [Response format/wrapper]
- **Authentication**: [Auth pattern used]

## Things to Avoid

<!-- What Claude should NOT do in this project -->
- Do NOT [e.g., "modify migration files manually"]
- Do NOT [e.g., "use any/unknown types"]
- Do NOT [e.g., "add new dependencies without asking"]
- Do NOT [e.g., "skip writing tests for new features"]

## Environment

<!-- Environment-specific notes -->
- Environment variables are in `.env` (never commit this file)
- Configuration is loaded from [config file path]
- [Any other environment notes]

## Context for Claude

<!-- Additional context that helps Claude understand the project -->
- [e.g., "This is a monorepo — only work in the specified package"]
- [e.g., "We use trunk-based development, all PRs go to main"]
- [e.g., "The API follows REST conventions with versioning in URL"]
