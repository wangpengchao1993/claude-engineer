# CLAUDE.md — Rust Project Template / Rust 项目模板

> Copy this to your Rust project root and customize.
> 将此文件复制到 Rust 项目根目录并进行自定义。

## Project Overview / 项目概述

<!-- Describe your project / 描述你的项目 -->
[Project Name] is a [CLI tool / web service / library / system tool] written in Rust.

## Tech Stack / 技术栈

- **Rust**: 1.78+ (stable)
- **Async Runtime / 异步运行时**: [tokio / async-std / None]
- **Web Framework / Web 框架**: [Axum / Actix-web / Rocket / None]
- **Database / 数据库**: [PostgreSQL via sqlx / SQLite / None]
- **Serialization / 序列化**: serde + serde_json
- **CLI / 命令行**: [clap / None]
- **Error Handling / 错误处理**: [anyhow + thiserror / color-eyre]
- **Logging / 日志**: [tracing / log + env_logger]
- **Testing / 测试**: built-in + [proptest / criterion for benchmarks]

## Commands / 常用命令

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

## Architecture / 项目架构

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

## Code Conventions / 代码规范

- Use `Result<T, E>` for all fallible operations — never `unwrap()` in production code — 所有可能失败的操作使用 `Result<T, E>`，生产代码中禁止使用 `unwrap()`
- `unwrap()` / `expect()` only in tests and with clear justification — `unwrap()` / `expect()` 仅在测试中使用，且需有明确理由
- `anyhow::Result` in binaries, `thiserror` for library error types — 二进制程序使用 `anyhow::Result`，库的错误类型使用 `thiserror`
- Prefer `&str` over `String` in function parameters — 函数参数优先使用 `&str` 而非 `String`
- Use `impl Trait` for function parameters when concrete type doesn't matter — 当具体类型不重要时，函数参数使用 `impl Trait`
- Derive `Debug` on all public types — 所有公共类型派生 `Debug`
- Derive `Clone`, `PartialEq` where sensible — 在合理的情况下派生 `Clone`、`PartialEq`
- Use `#[must_use]` on functions where ignoring return value is likely a bug — 在忽略返回值可能导致错误的函数上使用 `#[must_use]`
- Doc comments (`///`) on all public items — 所有公共项使用文档注释 (`///`)
- Module-level docs (`//!`) at the top of each file — 每个文件顶部使用模块级文档 (`//!`)
- Keep functions under 50 lines — extract helpers for clarity — 函数保持在50行以内，提取辅助函数以提高可读性
- Use `tracing` spans for observability, not println debugging — 使用 `tracing` span 进行可观测性追踪，不用 println 调试

## Naming Conventions / 命名规范

- **Crates/modules / Crate与模块**: snake_case (`my_crate`, `user_service`)
- **Types/Traits / 类型与 Trait**: PascalCase (`UserProfile`, `Serializable`)
- **Functions/methods / 函数与方法**: snake_case (`get_user_by_id`)
- **Constants / 常量**: UPPER_SNAKE_CASE (`MAX_CONNECTIONS`)
- **Lifetimes / 生命周期**: short lowercase (`'a`, `'ctx`)
- **Type parameters / 类型参数**: single uppercase or descriptive (`T`, `Item`)

## Important Notes / 重要说明

- Never use `unsafe` without a `// SAFETY:` comment explaining why it's sound — 禁止在没有 `// SAFETY:` 注释说明安全性的情况下使用 `unsafe`
- Never ignore compiler warnings — fix them or annotate with `#[allow()]` + reason — 禁止忽略编译器警告，修复或使用 `#[allow()]` + 原因进行标注
- All public API changes require updating CHANGELOG.md — 所有公共 API 变更需更新 CHANGELOG.md
- Run `cargo clippy` before committing — CI will reject clippy warnings — 提交前运行 `cargo clippy`，CI 会拒绝 clippy 警告
- Use `todo!()` for unfinished code, never empty implementations — 未完成的代码使用 `todo!()`，禁止空实现
- Pin dependency versions in `Cargo.toml` for applications (not libraries) — 应用程序在 `Cargo.toml` 中固定依赖版本（库不需要）
