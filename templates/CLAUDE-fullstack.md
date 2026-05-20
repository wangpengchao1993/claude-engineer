# [Project Name] -- CLAUDE.md
# [项目名称] -- CLAUDE.md

<!-- Copy this template and fill in every section for your fullstack project. -->
<!-- 复制此模板并为你的全栈项目填写每个部分。 -->
<!-- Delete all HTML comments and placeholder text when done. -->
<!-- 完成后删除所有 HTML 注释和占位文本。 -->

## Project Overview / 项目概览

<!-- 1-3 sentences: what does this application do? Who are the users? -->
<!-- 1-3 句话：这个应用做什么？用户是谁？ -->

## Tech Stack / 技术栈

- **Backend**: <!-- e.g. Express.js 4.x, Django 5, Rails 7 -->
- **Frontend**: <!-- e.g. React 18 + Vite, Next.js 14, Vue 3 + Nuxt -->
- **Database**: <!-- e.g. PostgreSQL 16, SQLite, MongoDB 7 -->
- **Auth**: <!-- e.g. JWT, session cookies, OAuth 2.0, Clerk -->
- **Testing**: <!-- e.g. Jest + supertest, Vitest + Testing Library -->
- **Linting**: <!-- e.g. ESLint + Prettier, Biome, Ruff -->
- **Deployment**: <!-- e.g. Docker + Kubernetes, Vercel, AWS ECS -->

## Commands / 命令

```bash
# Development / 开发
# <!-- backend start command -->
# <!-- frontend start command -->

# Testing / 测试
# <!-- backend test command -->
# <!-- frontend test command -->
# <!-- single file test command -->

# Linting / 代码检查
# <!-- lint command -->
# <!-- lint fix command -->

# Build / 构建
# <!-- build command -->

# Database / 数据库
# <!-- migration command -->
# <!-- seed command -->

# Deployment / 部署
# <!-- deploy command -->
```

## Architecture / 架构

### Backend / 后端

```
<!-- Paste your backend directory tree here. Example: -->
<!-- 在此粘贴你的后端目录树。示例： -->
src/
├── index.js              # Entry point / 入口
├── routes/               # HTTP route handlers / HTTP 路由处理器
├── models/               # Data access layer / 数据访问层
├── middleware/            # Auth, validation, error handling / 认证、验证、错误处理
├── services/             # Business logic / 业务逻辑
├── db/                   # Schema, migrations / 模式、迁移
├── utils/                # Shared utilities / 共享工具
└── config.js             # Environment config / 环境配置
```

### Frontend / 前端

```
<!-- Paste your frontend directory tree here. Example: -->
<!-- 在此粘贴你的前端目录树。示例： -->
src/
├── main.jsx              # Entry point / 入口
├── App.jsx               # Root component + router / 根组件 + 路由
├── components/           # Reusable UI components / 可复用 UI 组件
├── pages/                # Route-level pages / 路由级页面
├── hooks/                # Custom React hooks / 自定义 Hook
├── api/                  # API client / API 客户端
├── context/              # Global state providers / 全局状态提供者
└── styles/               # CSS / Tailwind entry / 样式入口
```

### Monorepo Structure (if applicable) / Monorepo 结构（如适用）

```
<!-- If using workspaces, describe the top-level layout: -->
<!-- 如果使用工作区，描述顶层布局： -->
packages/
├── api/                  # Backend package / 后端包
├── web/                  # Frontend package / 前端包
├── shared/               # Shared types and utilities / 共享类型和工具
└── config/               # Shared ESLint, TS config / 共享配置
```

## Code Conventions / 代码规范

### General / 通用

<!-- List 5-10 conventions that apply across the project. Be specific. -->
<!-- 列出 5-10 条适用于整个项目的规范。要具体。 -->

- <!-- e.g. Use ES modules (import/export), not CommonJS -->
- <!-- e.g. Prefer const over let; never use var -->
- <!-- e.g. async/await over raw Promises -->
- <!-- e.g. All functions have JSDoc with @param and @returns -->
- <!-- e.g. Maximum line length: 100 characters -->

### Backend Conventions / 后端规范

<!-- List conventions specific to the backend. -->
<!-- 列出后端特有的规范。 -->

- <!-- e.g. Route handlers are thin; logic goes in services -->
- <!-- e.g. All SQL in models/ directory only -->
- <!-- e.g. Use parameterized queries, never string interpolation -->
- <!-- e.g. Validate all input with Joi/Zod before processing -->
- <!-- e.g. Use structured logger, never console.log -->

### Frontend Conventions / 前端规范

<!-- List conventions specific to the frontend. -->
<!-- 列出前端特有的规范。 -->

- <!-- e.g. Functional components only -->
- <!-- e.g. State: Context + useReducer for global, useState for local -->
- <!-- e.g. Data fetching only in custom hooks, not in components -->
- <!-- e.g. Tailwind utility classes, no inline styles -->
- <!-- e.g. Test queries: by role/label, not test IDs -->

## API Conventions / API 规范

### Response Format / 响应格式

```json
// Success response / 成功响应
{
  "success": true,
  "data": { },
  "meta": { "page": 1, "total": 100 }
}

// Error response / 错误响应
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": []
  }
}
```

### Status Codes / 状态码

<!-- Document which HTTP status codes you use and when. -->
<!-- 记录你使用哪些 HTTP 状态码以及何时使用。 -->

| Code | Usage / 用途 |
|------|-------------|
| 200 | Successful read / update / 读取/更新成功 |
| 201 | Resource created / 资源已创建 |
| 400 | Validation error / 验证错误 |
| 401 | Not authenticated / 未认证 |
| 403 | Not authorized / 未授权 |
| 404 | Resource not found / 资源未找到 |
| 500 | Internal server error / 内部服务器错误 |

### Endpoint Naming / 端点命名

<!-- Document your URL conventions. -->
<!-- 记录你的 URL 规范。 -->

- REST: `GET /api/resources`, `POST /api/resources`, `PUT /api/resources/:id`
- Plural nouns for collections / 集合使用复数名词
- Nested resources: `/api/users/:userId/tasks` / 嵌套资源

## Database Patterns / 数据库模式

### Naming / 命名

- Tables: `snake_case`, plural (`tasks`, `user_sessions`)
- Columns: `snake_case` (`created_at`, `due_date`)
- Always include: `id`, `created_at`, `updated_at`

### Migrations / 迁移

<!-- How are migrations organized and run? -->
<!-- 迁移如何组织和运行？ -->

- Sequential numbering: `001_create_users.sql`, `002_create_tasks.sql`
- Never modify applied migrations / 不要修改已应用的迁移
- Add new migration for schema changes / 为模式变更添加新迁移

### Data Integrity / 数据完整性

<!-- Soft deletes? Referential integrity? Indexes? -->
<!-- 软删除？引用完整性？索引？ -->

- Soft-delete with `deleted_at` column / 使用 `deleted_at` 列软删除
- Foreign keys enforced / 强制外键约束
- Index all foreign keys and frequently queried columns / 为所有外键和常查列建索引

## Frontend Patterns / 前端模式

### Component Organization / 组件组织

<!-- How are components structured? -->
<!-- 组件如何组织？ -->

- `components/` -- Reusable UI components / 可复用 UI 组件
- `pages/` -- Route-level components / 路由级组件
- `ui/` -- Primitive components (Button, Input, Modal) / 基础组件

### State Management / 状态管理

<!-- What tools/patterns do you use for state? -->
<!-- 你使用什么工具/模式管理状态？ -->

- <!-- e.g. React Context + useReducer for auth/theme -->
- <!-- e.g. React Query / SWR for server state -->
- <!-- e.g. useState for component-local state -->

### Routing / 路由

<!-- What router and route structure do you use? -->
<!-- 你使用什么路由器和路由结构？ -->

- <!-- e.g. react-router-dom v6 with nested routes -->
- <!-- e.g. File-based routing via Next.js -->

## Authentication / 认证

<!-- Describe the auth flow step by step. -->
<!-- 逐步描述认证流程。 -->

1. <!-- e.g. Client sends credentials to POST /api/auth/login -->
2. <!-- e.g. Server returns tokens in httpOnly cookies -->
3. <!-- e.g. Middleware validates token on every protected route -->
4. <!-- e.g. Client refreshes token before expiry -->

## Deployment / 部署

### Docker / Docker

<!-- Describe your container setup. -->
<!-- 描述你的容器设置。 -->

- <!-- e.g. Multi-stage Dockerfile for production builds -->
- <!-- e.g. docker-compose for local development -->
- <!-- e.g. Separate containers for API, frontend, database -->

### Environment Variables / 环境变量

```bash
# Backend / 后端
# PORT=3001
# NODE_ENV=development
# DATABASE_URL=
# JWT_SECRET=

# Frontend / 前端
# VITE_API_URL=http://localhost:3001
```

### CI/CD

<!-- Describe your CI/CD pipeline. -->
<!-- 描述你的 CI/CD 流程。 -->

- <!-- e.g. GitHub Actions: test -> lint -> build -> deploy -->
- <!-- e.g. Claude Code Action for AI-assisted code review -->

## Things to Avoid / 禁止事项

<!-- List 5-10 anti-patterns specific to this project. -->
<!-- 列出 5-10 个特定于此项目的反模式。 -->

- <!-- e.g. Do not add dependencies without discussion -->
- <!-- e.g. Do not modify applied migration files -->
- <!-- e.g. Do not store secrets in code -->
- <!-- e.g. Do not write SQL outside models/ directory -->
- <!-- e.g. Do not use dangerouslySetInnerHTML -->
- <!-- e.g. Do not disable ESLint rules inline -->
- <!-- e.g. Do not commit .env files or database files -->

## Notes / 备注

<!-- Anything else Claude should know about this project. -->
<!-- Claude 还需要了解的关于此项目的其他信息。 -->

- <!-- e.g. Database is auto-created on first run -->
- <!-- e.g. Tests use in-memory database, not dev database -->
- <!-- e.g. Hot reload via nodemon (backend) and Vite HMR (frontend) -->
