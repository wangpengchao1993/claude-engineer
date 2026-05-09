# CLAUDE.md — Rust Project Template

> Copy this to your Rust project root and customize.

## Project Overview

<!-- Describe your project -->
[Project Name] is a [CLI tool / web service / library / system tool] written in Rust.

## Tech Stack

- **Rust**: 1.78+ (stable)
- **Async Runtime**: [tokio / async-std / None]
- **Web Framework**: [Axum / Actix-web / Rocket / None]
- **Database**: [PostgreSQL via sqlx / SQLite / None]
- **Serialization**: serde + serde_json
- **CLI**: [clap / None]
- **Error Handling**: [anyhow + thiserror / color-eyre]
- **Logging**: [tracing / log + env_logger]
- **Testing**: built-in + [proptest / criterion for benchmarks]

## Commands

```bash
# Development
cargo build                  # Build debug
cargo run                    # Run (debug)
cargo run -- <args>          # Run with arguments
cargo run --release          # Run optimized build

# Testing
cargo test                   # Run all tests
cargo test test_name         # Run specific test
cargo test -- --nocapture    # Show stdout in tests
cargo test -p crate_name     # Test specific crate (workspace)

# Code Quality
cargo clippy                 # Run linter
cargo clippy --fix           # Auto-fix lint issues
cargo fmt                    # Format code
cargo fmt -- --check         # Check formatting (CI)
cargo doc --open             # Generate and view docs

# Checks
cargo check                  # Fast type check (no codegen)
cargo audit                  # Check for security vulnerabilities
cargo outdated               # Check for outdated dependencies
```

## Architecture

```
src/
├── main.rs           # Entry point, CLI parsing
├── lib.rs            # Library root (public API)
├── config.rs         # Configuration (env vars, config files)
├── error.rs          # Error types (thiserror)
├── commands/         # CLI subcommands (one module per command)
│   ├── mod.rs
│   ├── init.rs
│   └── deploy.rs
├── api/              # HTTP handlers (if web service)
│   ├── mod.rs
│   ├── routes.rs
│   └── middleware.rs
├── db/               # Database layer
│   ├── mod.rs
│   ├── models.rs
│   └── queries.rs
├── services/         # Business logic
│   ├── mod.rs
│   └── user.rs
└── utils/            # Shared utilities
    └── mod.rs

tests/                # Integration tests
├── common/           # Shared test utilities
│   └── mod.rs
└── api_tests.rs
```

## Code Conventions

- Use `Result<T, E>` for all fallible operations — never `unwrap()` in production code
- `unwrap()` / `expect()` only in tests and with clear justification
- `anyhow::Result` in binaries, `thiserror` for library error types
- Prefer `&str` over `String` in function parameters
- Use `impl Trait` for function parameters when concrete type doesn't matter
- Derive `Debug` on all public types
- Derive `Clone`, `PartialEq` where sensible
- Use `#[must_use]` on functions where ignoring return value is likely a bug
- Doc comments (`///`) on all public items
- Module-level docs (`//!`) at the top of each file
- Keep functions under 50 lines — extract helpers for clarity
- Use `tracing` spans for observability, not println debugging

## Naming Conventions

- **Crates/modules**: snake_case (`my_crate`, `user_service`)
- **Types/Traits**: PascalCase (`UserProfile`, `Serializable`)
- **Functions/methods**: snake_case (`get_user_by_id`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_CONNECTIONS`)
- **Lifetimes**: short lowercase (`'a`, `'ctx`)
- **Type parameters**: single uppercase or descriptive (`T`, `Item`)

## Important Notes

- Never use `unsafe` without a `// SAFETY:` comment explaining why it's sound
- Never ignore compiler warnings — fix them or annotate with `#[allow()]` + reason
- All public API changes require updating CHANGELOG.md
- Run `cargo clippy` before committing — CI will reject clippy warnings
- Use `todo!()` for unfinished code, never empty implementations
- Pin dependency versions in `Cargo.toml` for applications (not libraries)
