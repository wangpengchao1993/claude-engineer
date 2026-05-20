# CLAUDE.md — Full-Stack E-Commerce App (Real Example) / 全栈电商应用（真实示例）

## Overview / 概述
E-commerce platform with Next.js 14 frontend and Express.js backend.
Monorepo managed with Turborepo. Stripe for payments, Auth0 for authentication.
（使用 Next.js 14 前端和 Express.js 后端的电商平台。使用 Turborepo 管理的 Monorepo。Stripe 处理支付，Auth0 处理认证。）

## Tech Stack / 技术栈
- **Frontend / 前端**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand
- **Backend / 后端**: Express.js, TypeScript, Prisma ORM
- **Database / 数据库**: PostgreSQL 16
- **Cache / 缓存**: Redis 7
- **Queue / 消息队列**: BullMQ (order processing, email sending)
- **Auth / 认证**: Auth0
- **Payments / 支付**: Stripe
- **Monorepo / 单仓库**: Turborepo + pnpm workspaces

## Packages / 包结构
- `apps/web` — Customer storefront (Next.js) — 客户店面
- `apps/admin` — Admin dashboard (Next.js) — 管理后台
- `apps/api` — REST API (Express) — REST API 接口
- `packages/ui` — Shared React components — 共享 React 组件
- `packages/db` — Prisma schema + generated client — Prisma 模式与生成的客户端
- `packages/types` — Shared TypeScript types — 共享 TypeScript 类型
- `packages/config` — Shared configuration — 共享配置

## Commands / 常用命令
```bash
pnpm dev                          # Start all apps
pnpm build                        # Build everything
pnpm test                         # Run all tests
pnpm lint                         # Lint everything
pnpm --filter @app/api test       # Test API only
pnpm --filter @app/web dev        # Dev web only
pnpm db:migrate                   # Run Prisma migrations
pnpm db:seed                      # Seed database
pnpm db:studio                    # Open Prisma Studio
docker compose up -d              # Start PostgreSQL + Redis
```

## Architecture Notes / 架构说明
- API follows REST conventions with `/api/v1/` prefix — API 遵循 REST 规范，使用 `/api/v1/` 前缀
- All API responses: `{ data: T }` on success, `{ error: { code, message } }` on failure — 所有 API 响应：成功时 `{ data: T }`，失败时 `{ error: { code, message } }`
- Auth middleware validates Auth0 JWT on every request — 认证中间件在每个请求上验证 Auth0 JWT
- Payments: all Stripe operations go through `apps/api/src/services/stripe.ts` — 支付：所有 Stripe 操作通过 `apps/api/src/services/stripe.ts`
- Background jobs: order confirmation emails, inventory sync, report generation — 后台任务：订单确认邮件、库存同步、报表生成

## Code Conventions / 代码规范
- Functional components, hooks only — 仅使用函数组件和 hooks
- Server Components by default, `"use client"` only when needed — 默认使用服务端组件，仅在需要时使用 `"use client"`
- Named exports everywhere (no default exports) — 全部使用具名导出（禁止默认导出）
- Zod for all request validation in API — API 中所有请求验证使用 Zod
- Custom error classes in `apps/api/src/errors/` — 自定义错误类放在 `apps/api/src/errors/`
- Use `Decimal` for all prices (never float) — 所有价格使用 `Decimal`（禁止使用 float）
- Tests: Vitest for unit, Playwright for E2E — 测试：单元测试用 Vitest，端到端测试用 Playwright

## Do Not Modify / 禁止修改
- `packages/db/prisma/migrations/` — never edit existing migrations — 禁止编辑已有的迁移文件
- `packages/types/generated/` — auto-generated from API schema — 从 API schema 自动生成
- `.env.production` — managed by DevOps — 由 DevOps 管理
- Any file in `node_modules/` or `dist/` — `node_modules/` 或 `dist/` 中的任何文件

## Git Conventions / Git 规范
- Branch / 分支: `feat/xxx`, `fix/xxx`, `chore/xxx`
- Commits / 提交: conventional commits (`feat(web): add cart page`)
- PRs / 拉取请求: squash merge to main, require 1 approval — 向 main 合并时使用 squash merge，需要1人审批
