# CLAUDE.md — Universal Project Template / 通用项目模板

> Copy this file to the root of your project and customize it.
> 将此文件复制到项目根目录并进行自定义。
> Claude Code will automatically read this file for project context.
> Claude Code 会自动读取此文件以获取项目上下文。

## Project Overview / 项目概述

<!-- Describe what this project does in 1-2 sentences / 用1-2句话描述项目功能 -->
[Project Name] is a [type of application] that [primary function].

## Tech Stack / 技术栈

- **Language / 编程语言**: [e.g., Python 3.12, TypeScript 5.x]
- **Framework / 框架**: [e.g., FastAPI, Next.js 14, Axum]
- **Database / 数据库**: [e.g., PostgreSQL, SQLite, MongoDB]
- **Package Manager / 包管理器**: [e.g., uv, pnpm, cargo]
- **Testing / 测试**: [e.g., pytest, vitest, cargo test]
- **CI/CD / 持续集成与部署**: [e.g., GitHub Actions]

## Commands / 常用命令

<!-- List the most frequently used commands / 列出最常用的命令 -->
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

## Architecture / 项目架构

<!-- Describe the project structure and key directories / 描述项目结构和关键目录 -->
```
src/
├── [dir]/       # [Description]
├── [dir]/       # [Description]
├── [dir]/       # [Description]
└── [dir]/       # [Description]
tests/           # Test files (mirror src/ structure)
```

## Code Conventions / 代码规范

<!-- List the coding standards Claude should follow / 列出 Claude 应遵循的编码标准 -->
- [Convention 1, e.g., "Use functional components with hooks"]
- [Convention 2, e.g., "All functions must have type annotations"]
- [Convention 3, e.g., "Use descriptive variable names, no abbreviations"]
- [Convention 4, e.g., "Error handling: use Result types, not exceptions"]

## Important Patterns / 重要模式

<!-- Describe patterns Claude should follow when generating code / 描述 Claude 生成代码时应遵循的模式 -->
- **Error Handling / 错误处理**: [How errors should be handled]
- **Logging / 日志记录**: [Logging conventions and levels]
- **API Responses / API 响应**: [Response format/wrapper]
- **Authentication / 认证**: [Auth pattern used]

## Things to Avoid / 禁止事项

<!-- What Claude should NOT do in this project / Claude 在此项目中不应做的事情 -->
- Do NOT / 禁止 [e.g., "modify migration files manually"]
- Do NOT / 禁止 [e.g., "use any/unknown types"]
- Do NOT / 禁止 [e.g., "add new dependencies without asking"]
- Do NOT / 禁止 [e.g., "skip writing tests for new features"]

## Environment / 环境配置

<!-- Environment-specific notes / 环境相关说明 -->
- Environment variables are in `.env` (never commit this file) — 环境变量位于 `.env`（切勿提交此文件）
- Configuration is loaded from [config file path] — 配置从 [配置文件路径] 加载
- [Any other environment notes]

## Context for Claude / Claude 上下文信息

<!-- Additional context that helps Claude understand the project / 帮助 Claude 理解项目的额外上下文 -->
- [e.g., "This is a monorepo — only work in the specified package"]
- [e.g., "We use trunk-based development, all PRs go to main"]
- [e.g., "The API follows REST conventions with versioning in URL"]
