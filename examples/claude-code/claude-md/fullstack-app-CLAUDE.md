# CLAUDE.md — Full-Stack E-Commerce App (Real Example)

## Overview
E-commerce platform with Next.js 14 frontend and Express.js backend.
Monorepo managed with Turborepo. Stripe for payments, Auth0 for authentication.

## Tech Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand
- **Backend**: Express.js, TypeScript, Prisma ORM
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **Queue**: BullMQ (order processing, email sending)
- **Auth**: Auth0
- **Payments**: Stripe
- **Monorepo**: Turborepo + pnpm workspaces

## Packages
- `apps/web` — Customer storefront (Next.js)
- `apps/admin` — Admin dashboard (Next.js)
- `apps/api` — REST API (Express)
- `packages/ui` — Shared React components
- `packages/db` — Prisma schema + generated client
- `packages/types` — Shared TypeScript types
- `packages/config` — Shared configuration

## Commands
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

## Architecture Notes
- API follows REST conventions with `/api/v1/` prefix
- All API responses: `{ data: T }` on success, `{ error: { code, message } }` on failure
- Auth middleware validates Auth0 JWT on every request
- Payments: all Stripe operations go through `apps/api/src/services/stripe.ts`
- Background jobs: order confirmation emails, inventory sync, report generation

## Code Conventions
- Functional components, hooks only
- Server Components by default, `"use client"` only when needed
- Named exports everywhere (no default exports)
- Zod for all request validation in API
- Custom error classes in `apps/api/src/errors/`
- Use `Decimal` for all prices (never float)
- Tests: Vitest for unit, Playwright for E2E

## Do Not Modify
- `packages/db/prisma/migrations/` — never edit existing migrations
- `packages/types/generated/` — auto-generated from API schema
- `.env.production` — managed by DevOps
- Any file in `node_modules/` or `dist/`

## Git Conventions
- Branch: `feat/xxx`, `fix/xxx`, `chore/xxx`
- Commits: conventional commits (`feat(web): add cart page`)
- PRs: squash merge to main, require 1 approval
