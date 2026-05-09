# CLAUDE.md — TypeScript Project Template

> Copy this to your TypeScript project root and customize.

## Project Overview

<!-- Describe your project -->
[Project Name] is a [web app / API / CLI tool / library] built with TypeScript.

## Tech Stack

- **Runtime**: Node.js 20+ / Bun / Deno
- **Language**: TypeScript 5.x (strict mode)
- **Framework**: [Next.js 14 / Express / Fastify / Hono / None]
- **Frontend**: [React 18 / Vue 3 / Svelte / None]
- **Database**: [PostgreSQL / SQLite / MongoDB / None]
- **ORM**: [Prisma / Drizzle / TypeORM / None]
- **Package Manager**: [pnpm / npm / yarn / bun]
- **Testing**: [vitest / jest]
- **Linting**: [ESLint / Biome]
- **Formatting**: [Prettier / Biome]

## Commands

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

## Architecture

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

## Code Conventions

- Strict TypeScript — no `any`, no `@ts-ignore`, no `as` casts without justification
- Prefer `interface` for object shapes, `type` for unions/intersections
- Functional components with hooks — no class components
- Server Components by default (Next.js), `"use client"` only when needed
- Prefer named exports over default exports
- Use `const` by default, `let` only when reassignment is needed
- Async/await over raw promises — never use `.then()` chains
- Destructure props in function parameters
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Error handling: custom error classes extending `Error`
- Prefer `Map`/`Set` over plain objects for dynamic keys

## Naming Conventions

- **Files**: kebab-case (`user-profile.tsx`, `auth-service.ts`)
- **Components**: PascalCase (`UserProfile`, `AuthGuard`)
- **Functions/vars**: camelCase (`getUserById`, `isAuthenticated`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- **Types/Interfaces**: PascalCase (`UserProfile`, `ApiResponse`)
- **Enums**: PascalCase members (`Status.Active`, not `Status.ACTIVE`)

## Important Notes

- Never commit `.env` files — use `.env.example` as reference
- All API responses follow `{ data: T }` or `{ error: { message, code } }` format
- Use Zod for runtime validation at API boundaries
- Images go through `next/image` for optimization
- Environment variables accessed via `src/lib/env.ts` (validated with Zod)
- Use `next/link` for internal navigation, never `<a>` tags
