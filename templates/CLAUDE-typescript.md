# CLAUDE.md — TypeScript Project Template / TypeScript 项目模板

> Copy this to your TypeScript project root and customize.
> 将此文件复制到 TypeScript 项目根目录并进行自定义。

## Project Overview / 项目概述

<!-- Describe your project / 描述你的项目 -->
[Project Name] is a [web app / API / CLI tool / library] built with TypeScript.

## Tech Stack / 技术栈

- **Runtime / 运行时**: Node.js 20+ / Bun / Deno
- **Language / 编程语言**: TypeScript 5.x (strict mode)
- **Framework / 框架**: [Next.js 14 / Express / Fastify / Hono / None]
- **Frontend / 前端**: [React 18 / Vue 3 / Svelte / None]
- **Database / 数据库**: [PostgreSQL / SQLite / MongoDB / None]
- **ORM / 对象关系映射**: [Prisma / Drizzle / TypeORM / None]
- **Package Manager / 包管理器**: [pnpm / npm / yarn / bun]
- **Testing / 测试**: [vitest / jest]
- **Linting / 代码检查**: [ESLint / Biome]
- **Formatting / 格式化**: [Prettier / Biome]

## Commands / 常用命令

```bash
# Development
pnpm dev                     # Start dev server
pnpm build                   # Production build
pnpm start                   # Start production server

# Testing
pnpm test                    # Run all tests
pnpm test:watch              # Watch mode
pnpm test -- path/to/file    # Run specific test
pnpm test:coverage           # Run with coverage

# Code Quality
pnpm lint                    # Run ESLint
pnpm lint:fix                # Lint and auto-fix
pnpm format                  # Run Prettier
pnpm typecheck               # Run tsc --noEmit

# Database (if applicable)
pnpm db:migrate              # Run migrations
pnpm db:generate             # Generate Prisma client
pnpm db:seed                 # Seed database
pnpm db:studio               # Open database GUI
```

## Architecture / 项目架构

```
src/
├── app/              # Next.js App Router pages (or routes)
│   ├── layout.tsx
│   ├── page.tsx
│   └── api/          # API routes
├── components/       # React components
│   ├── ui/           # Base UI components (Button, Input, etc.)
│   └── features/     # Feature-specific components
├── hooks/            # Custom React hooks
├── lib/              # Core utilities and configs
│   ├── db.ts         # Database client
│   ├── auth.ts       # Authentication
│   └── utils.ts      # Helper functions
├── services/         # Business logic / API calls
├── types/            # TypeScript type definitions
└── middleware.ts     # Middleware (Next.js)

tests/
├── setup.ts          # Test setup
├── unit/             # Unit tests
└── integration/      # Integration tests
```

## Code Conventions / 代码规范

- Strict TypeScript — no `any`, no `@ts-ignore`, no `as` casts without justification — 严格 TypeScript，禁止使用 `any`、`@ts-ignore`、无理由的 `as` 类型断言
- Prefer `interface` for object shapes, `type` for unions/intersections — 对象结构优先使用 `interface`，联合/交叉类型使用 `type`
- Functional components with hooks — no class components — 使用函数组件和 hooks，禁止类组件
- Server Components by default (Next.js), `"use client"` only when needed — 默认使用服务端组件（Next.js），仅在需要时使用 `"use client"`
- Prefer named exports over default exports — 优先使用具名导出而非默认导出
- Use `const` by default, `let` only when reassignment is needed — 默认使用 `const`，仅在需要重新赋值时使用 `let`
- Async/await over raw promises — never use `.then()` chains — 使用 async/await 而非原始 Promise，禁止使用 `.then()` 链
- Destructure props in function parameters — 在函数参数中解构 props
- Use optional chaining (`?.`) and nullish coalescing (`??`) — 使用可选链 (`?.`) 和空值合并 (`??`)
- Error handling: custom error classes extending `Error` — 错误处理：使用继承 `Error` 的自定义错误类
- Prefer `Map`/`Set` over plain objects for dynamic keys — 动态键优先使用 `Map`/`Set` 而非普通对象

## Naming Conventions / 命名规范

- **Files / 文件**: kebab-case (`user-profile.tsx`, `auth-service.ts`)
- **Components / 组件**: PascalCase (`UserProfile`, `AuthGuard`)
- **Functions/vars / 函数与变量**: camelCase (`getUserById`, `isAuthenticated`)
- **Constants / 常量**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- **Types/Interfaces / 类型与接口**: PascalCase (`UserProfile`, `ApiResponse`)
- **Enums / 枚举**: PascalCase members (`Status.Active`, not `Status.ACTIVE`)

## Important Notes / 重要说明

- Never commit `.env` files — use `.env.example` as reference — 禁止提交 `.env` 文件，使用 `.env.example` 作为参考
- All API responses follow `{ data: T }` or `{ error: { message, code } }` format — 所有 API 响应遵循 `{ data: T }` 或 `{ error: { message, code } }` 格式
- Use Zod for runtime validation at API boundaries — 在 API 边界使用 Zod 进行运行时验证
- Images go through `next/image` for optimization — 图片通过 `next/image` 进行优化
- Environment variables accessed via `src/lib/env.ts` (validated with Zod) — 环境变量通过 `src/lib/env.ts` 访问（使用 Zod 验证）
- Use `next/link` for internal navigation, never `<a>` tags — 内部导航使用 `next/link`，禁止使用 `<a>` 标签
