# Full-Stack Demo: AI-Assisted Task Manager / 全栈示例：AI 辅助的任务管理器

A reference implementation showing how a real project is configured for AI-assisted
development with Claude Code.

这是一个参考实现，展示如何为 AI 辅助开发配置真实项目。

---

## Project Overview / 项目概览

This is a simple **Task Manager** application built with:

| Layer | Technology |
|-------|-----------|
| Backend | Express.js (Node.js) |
| Frontend | React 18 + Vite |
| Database | SQLite (via better-sqlite3) |
| Testing | Jest (backend) + Vitest (frontend) |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |

The project demonstrates how to configure Claude Code for a fullstack monorepo,
including CLAUDE.md, hooks, MCP servers, and CI integration.

本项目演示如何为全栈 monorepo 配置 Claude Code，包括 CLAUDE.md、钩子、MCP 服务器和 CI 集成。

---

## Directory Structure / 目录结构

```
fullstack-demo/
├── CLAUDE.md                  # AI assistant configuration / AI 助手配置
├── .claude/
│   └── settings.json          # Claude Code permissions & hooks / 权限与钩子
├── .github/
│   └── workflows/
│       └── ai-review.yml      # CI: AI-assisted code review / AI 辅助代码审查
├── docker-compose.yml         # Local dev environment / 本地开发环境
├── backend/
│   ├── package.json
│   ├── src/
│   │   ├── index.js           # Express app entry / 应用入口
│   │   ├── routes/
│   │   │   └── tasks.js       # Task CRUD endpoints / 任务增删改查接口
│   │   ├── models/
│   │   │   └── task.js        # SQLite data access / 数据访问层
│   │   ├── middleware/
│   │   │   ├── auth.js        # JWT authentication / JWT 认证
│   │   │   └── errors.js      # Centralized error handler / 集中错误处理
│   │   └── db/
│   │       ├── schema.sql     # Database schema / 数据库模式
│   │       └── migrate.js     # Migration runner / 迁移执行器
│   └── tests/
│       └── tasks.test.js      # API integration tests / API 集成测试
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx           # React entry / React 入口
│   │   ├── App.jsx            # Root component / 根组件
│   │   ├── components/
│   │   │   ├── TaskList.jsx   # Task list view / 任务列表视图
│   │   │   └── TaskForm.jsx   # Create/edit form / 创建/编辑表单
│   │   ├── hooks/
│   │   │   └── useTasks.js    # Data fetching hook / 数据获取 Hook
│   │   └── api/
│   │       └── client.js      # API client wrapper / API 客户端封装
│   └── tests/
│       └── TaskList.test.jsx  # Component tests / 组件测试
└── README.md                  # This file / 本文件
```

---

## How CLAUDE.md Is Configured / CLAUDE.md 配置方式

The `CLAUDE.md` file at the project root gives Claude Code everything it needs to work
effectively in this codebase:

CLAUDE.md 文件为 Claude Code 提供了在此代码库中高效工作所需的全部信息：

1. **Project overview** -- what the app does and its tech stack
2. **All commands** -- exact scripts for dev, test, lint, build, deploy
3. **Architecture** -- where each type of code lives
4. **Code conventions** -- naming, formatting, patterns to follow
5. **Anti-patterns** -- things to avoid, specific to this project
6. **Environment** -- required env vars, ports, database location

See [CLAUDE.md](./CLAUDE.md) for the full configuration.

---

## How Hooks Enforce Quality / 钩子如何保证质量

The `.claude/settings.json` file configures three types of hooks:

`.claude/settings.json` 配置了三种钩子：

### PreToolUse Hooks / 工具使用前钩子

- **check-protected-files**: Prevents modifications to migration files, lock files,
  and CI configuration without explicit confirmation.

  防止在未经确认的情况下修改迁移文件、锁文件和 CI 配置。

### PostToolUse Hooks / 工具使用后钩子

- **auto-lint**: Runs ESLint on any file that was just edited, ensuring consistent
  code style without manual intervention.

  对刚编辑的文件自动运行 ESLint，无需手动干预即可保持一致的代码风格。

### Stop Hooks / 停止钩子

- **notify**: Sends a desktop notification when Claude Code completes a long-running
  task.

  当 Claude Code 完成长时间运行的任务时发送桌面通知。

---

## How MCP Connects to the Database / MCP 如何连接数据库

You can configure an MCP server to give Claude Code direct read access to the SQLite
database. Add this to your `.claude/settings.json`:

可以配置 MCP 服务器，让 Claude Code 直接读取 SQLite 数据库：

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-sqlite", "./backend/data/tasks.db"]
    }
  }
}
```

This lets Claude Code query the database schema and data directly, which helps it
write more accurate queries and understand the data model.

这让 Claude Code 能直接查询数据库结构和数据，有助于编写更准确的查询和理解数据模型。

---

## Running Locally / 本地运行

### Option 1: Docker (recommended / 推荐)

```bash
# Start all services / 启动所有服务
docker-compose up

# App available at / 应用访问地址:
#   Frontend: http://localhost:5173
#   Backend:  http://localhost:3001
```

### Option 2: Manual / 手动运行

```bash
# Backend / 后端
cd backend
npm install
cp .env.example .env
npm run dev          # Starts on port 3001 / 启动于端口 3001

# Frontend (in another terminal / 在另一个终端)
cd frontend
npm install
npm run dev          # Starts on port 5173 / 启动于端口 5173
```

### Running Tests / 运行测试

```bash
# Backend tests / 后端测试
cd backend && npm test

# Frontend tests / 前端测试
cd frontend && npm test

# All tests (from project root) / 所有测试（从项目根目录）
npm test --workspaces
```

---

## CI/CD Configuration / CI/CD 配置

The `.github/workflows/ai-review.yml` workflow runs on every pull request:

该工作流在每个 Pull Request 上运行：

1. **Install dependencies** -- `npm ci` for both backend and frontend
2. **Run tests** -- Jest (backend) and Vitest (frontend)
3. **Run linter** -- ESLint across both packages
4. **AI review** -- Claude Code Action reviews the diff and posts comments
5. **Post results** -- Test and lint results appear as PR comments

---

## Using Harness Frameworks / 使用治理框架

This project is compatible with any of the 10 harness frameworks described in the
main guide. Here is how each applies:

本项目兼容主指南中描述的所有 10 个治理框架：

| Framework / 框架 | How It Applies / 应用方式 |
|---|---|
| **CLAUDE.md** | See `CLAUDE.md` -- covers stack, commands, conventions |
| **Hooks** | See `.claude/settings.json` -- pre/post/stop hooks |
| **MCP** | SQLite MCP server for database access |
| **Custom Commands** | Add `/project:migrate`, `/project:seed` for common tasks |
| **Git Hooks** | pre-commit runs lint; pre-push runs tests |
| **CI/CD** | GitHub Actions with Claude Code Action |
| **Permissions** | Scoped in settings.json -- allow test/lint/build only |
| **Multi-Agent** | Use Orchestrator for cross-stack refactors |
| **Memory** | CLAUDE.md acts as persistent project memory |
| **Templates** | Use `CLAUDE-fullstack.md` template as starting point |

---

## Key Files to Study / 关键文件

| File | Purpose / 用途 |
|------|----------------|
| `CLAUDE.md` | The core AI configuration -- study this first |
| `.claude/settings.json` | Permissions, hooks, and MCP configuration |
| `ai-review.yml` | How to integrate Claude Code into CI |
| `docker-compose.yml` | Local development environment |
| `backend/package.json` | Backend dependencies and scripts |
| `frontend/package.json` | Frontend dependencies and scripts |

---

## License / 许可

MIT -- see the root LICENSE file.

MIT 许可证 -- 见根目录 LICENSE 文件。
