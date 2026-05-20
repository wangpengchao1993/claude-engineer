# Managing Large Codebases with AI

> Strategies for using Claude Code effectively in projects with 100K+ lines of code: context management, CLAUDE.md layering, multi-session workflows, monorepo patterns, and knowing when AI cannot help.

## Table of Contents

- [The Context Challenge](#the-context-challenge)
- [CLAUDE.md Layering Strategy](#claudemd-layering-strategy)
- [Context Management Tactics](#context-management-tactics)
- [Multi-Session Workflows](#multi-session-workflows)
- [Monorepo Strategies](#monorepo-strategies)
- [When AI Cannot Help](#when-ai-cannot-help)
- [Real Example: Refactoring a 200K LOC Monolith](#real-example-refactoring-a-200k-loc-monolith)

---

## The Context Challenge

Large codebases do not fit in an AI context window. A 100K+ LOC project may have thousands of files, and Claude Code can only hold a fraction of them in a single session.

```
Typical project sizes vs context:
- Small project (5K LOC):     Fits comfortably, AI sees everything
- Medium project (20K LOC):   Fits with care, focus on relevant modules
- Large project (100K LOC):   Cannot fit, must use selective strategies
- Monolith (500K+ LOC):       Requires strict scoping and multi-session work

The solution is NOT to dump everything into context.
The solution is to give AI the right context for each task.
```

### Why "Just Read Everything" Fails

```bash
# BAD: Trying to load entire codebase
claude "Read all files in src/ and then refactor the auth module"
# Result: context fills up with irrelevant code, AI loses focus

# GOOD: Targeted context loading
claude "Read src/auth/ and src/types/auth.ts, then refactor the token refresh logic"
# Result: AI has exactly what it needs
```

---

## CLAUDE.md Layering Strategy

The key to large codebases is a hierarchy of CLAUDE.md files. Each level describes only its own domain.

### Three-Level Hierarchy

```
project-root/
  CLAUDE.md                           # Level 1: Project overview
  packages/
    auth/
      CLAUDE.md                       # Level 2: Auth module details
      src/
        providers/
          CLAUDE.md                   # Level 3: OAuth provider specifics
    api/
      CLAUDE.md                       # Level 2: API module details
    web/
      CLAUDE.md                       # Level 2: Frontend details
    shared/
      CLAUDE.md                       # Level 2: Shared utilities
```

### Level 1: Root CLAUDE.md (Project Overview)

```markdown
# Acme Platform

## Architecture
Monorepo with 4 packages managed by Turborepo:
- packages/auth: Authentication service (Express, JWT, OAuth)
- packages/api: REST API gateway (Express, OpenAPI)
- packages/web: Customer-facing SPA (React, Vite)
- packages/shared: Shared types and utilities

## Tech Stack
- Language: TypeScript 5.4 (strict mode)
- Runtime: Node.js 20 LTS
- Database: PostgreSQL 16 via Drizzle ORM
- Cache: Redis 7
- Queue: BullMQ
- CI: GitHub Actions

## Key Conventions
- Named exports only (no default exports)
- Result<T, E> pattern for error handling (see packages/shared/src/result.ts)
- All API endpoints use zod validation (see packages/api/src/validation/)
- Database migrations in packages/api/drizzle/

## How to Run
- `npm run dev`: starts all packages in dev mode
- `npm run test`: runs all tests
- `npm run build`: builds all packages

## Module Owners
- auth: @alice
- api: @bob
- web: @carol
- shared: @dave
```

### Level 2: Module CLAUDE.md

```markdown
# packages/auth/CLAUDE.md

## Purpose
Handles all authentication and authorization. Issues JWTs, manages sessions,
integrates with OAuth providers, and enforces RBAC policies.

## Architecture
```
src/
  index.ts          # Express app setup and route registration
  jwt.ts            # Token creation, verification, refresh
  session.ts        # Session store (Redis-backed)
  rbac.ts           # Role-based access control middleware
  providers/        # OAuth provider adapters
    google.ts
    github.ts
    base.ts         # Abstract base class for providers
  middleware/
    authenticate.ts # Express middleware to verify JWT
    authorize.ts    # Express middleware to check permissions
  types.ts          # Auth-specific types (also re-exported from shared)
```

## Key Patterns
- All providers extend BaseOAuthProvider (src/providers/base.ts)
- Token refresh uses sliding window: refresh if <25% TTL remaining
- Sessions are stored in Redis with prefix "session:"
- RBAC permissions defined in src/permissions.ts (single source of truth)

## Testing
- Unit tests: colocated as *.test.ts
- Integration tests: __tests__/integration/ (need Redis + PostgreSQL)
- Run: `npm run test -w packages/auth`

## Common Tasks
- Add new OAuth provider: copy src/providers/google.ts, extend BaseOAuthProvider
- Add new permission: update src/permissions.ts, add migration
- Change token TTL: update config in src/config.ts (not hardcoded anywhere)
```

### Level 3: Sub-Module CLAUDE.md

```markdown
# packages/auth/src/providers/CLAUDE.md

## OAuth Provider Adapters

Each file implements one OAuth provider. All extend BaseOAuthProvider.

## Adding a New Provider
1. Create new file: `{provider-name}.ts`
2. Extend BaseOAuthProvider
3. Implement required methods:
   - `getAuthorizationUrl(state: string): string`
   - `exchangeCode(code: string): Promise<OAuthTokens>`
   - `getUserProfile(accessToken: string): Promise<OAuthProfile>`
4. Register in `index.ts` provider map
5. Add provider config to environment variables

## Testing Providers
- Mock the HTTP calls (never hit real OAuth endpoints in tests)
- Test the token exchange error handling
- Test profile mapping to internal User type
```

---

## Context Management Tactics

### Start Sessions Clean

```bash
# When continuing work from a previous session, use /compact
# This summarizes the previous session and frees context space

# In Claude Code interactive mode:
> /compact
# Then continue with your task
```

### Explicitly Limit What AI Reads

```bash
# Tell Claude exactly which files to look at
claude "Read only these files and then implement the feature:
- src/auth/jwt.ts
- src/auth/types.ts
- src/auth/config.ts
Do NOT read other files unless I tell you to."
```

### Pipe Specific Files for Focused Tasks

```bash
# Review a specific module without loading anything else
cat src/auth/jwt.ts src/auth/session.ts | claude -p \
  "Review these auth files for security issues. Focus on:
   - Token validation logic
   - Session expiry handling
   - Error information leakage"

# Analyze types only
find src -name "types.ts" -exec cat {} + | claude -p \
  "Analyze these type definitions for inconsistencies"

# Review recent changes
git diff HEAD~5 -- src/api/ | claude -p \
  "Review these API changes for breaking changes"
```

### Sub-Agent Pattern

When a task spans multiple modules, break it into scoped sub-tasks:

```bash
# Main task: Add audit logging across the platform

# Sub-task 1: Define the audit log schema (scoped to shared)
claude --cwd packages/shared \
  "Create an AuditLog type and a createAuditEntry utility function.
   Read packages/shared/src/types.ts for existing patterns."

# Sub-task 2: Add audit logging to auth (scoped to auth)
claude --cwd packages/auth \
  "Add audit logging for login, logout, and token refresh events.
   Import createAuditEntry from @acme/shared.
   Read src/jwt.ts and src/session.ts for where to add the calls."

# Sub-task 3: Add audit logging to API (scoped to api)
claude --cwd packages/api \
  "Add audit logging middleware that logs all mutating API calls.
   Import createAuditEntry from @acme/shared.
   Read src/middleware/ for existing middleware patterns."
```

### Use Reference Files to Reduce Context

Instead of having Claude read 20 files, create a summary file:

```bash
# Generate a reference file for AI context
claude -p "Read packages/api/src/routes/ and create a summary file at
  docs/api-routes-summary.md that lists:
  - Each route with method, path, and description
  - Request/response types
  - Auth requirements
  Keep it under 200 lines."

# Later, use the summary instead of reading all route files
claude "Read docs/api-routes-summary.md. Now add a new route for
  POST /api/v1/audit-logs that follows the same patterns."
```

---

## Multi-Session Workflows

For large features, plan across multiple sessions. Pass context between them via files.

### Session 1: Plan

```bash
claude "I need to add multi-tenant support to this platform.
Read:
- CLAUDE.md (project overview)
- packages/auth/CLAUDE.md
- packages/api/CLAUDE.md
- packages/shared/src/types.ts

Create a detailed implementation plan at docs/plans/multi-tenant.md:
1. Database schema changes needed
2. Auth changes (tenant-scoped tokens)
3. API changes (tenant middleware)
4. Migration strategy
5. Testing approach

Break it into 5-6 independent work sessions."
```

### Session 2: Implement Shared Types

```bash
claude "Read docs/plans/multi-tenant.md (the plan from session 1).
Implement Step 1: shared types and database schema.
Work in packages/shared/ and packages/api/drizzle/.
After implementing, update the plan file to mark Step 1 as done."
```

### Session 3: Implement Auth Changes

```bash
claude "Read docs/plans/multi-tenant.md (check completed steps).
Implement Step 2: auth changes for tenant-scoped tokens.
Work in packages/auth/.
Read packages/shared/src/types.ts for the new Tenant type from Step 1.
Update the plan file when done."
```

### Session Handoff Pattern

```markdown
# docs/plans/multi-tenant.md (after session 2)

## Implementation Plan

### Step 1: Shared Types & Schema [DONE]
- Created Tenant type in packages/shared/src/types.ts
- Added tenants table migration: packages/api/drizzle/0005_add_tenants.sql
- Added tenant_id column to users table: packages/api/drizzle/0006_users_tenant.sql
- Files modified: packages/shared/src/types.ts, packages/api/src/db/schema.ts

### Step 2: Auth Changes [IN PROGRESS]
- Scope: packages/auth/
- Need to: add tenantId to JWT payload, scope sessions by tenant
- Reference: new Tenant type in packages/shared/src/types.ts

### Step 3: API Middleware [TODO]
...
```

---

## Monorepo Strategies

### Scope Claude Code to a Package

```bash
# Use --cwd to limit Claude Code's working scope
claude --cwd packages/auth "Add rate limiting to the login endpoint"

# This makes Claude Code start in that directory,
# so it reads the local CLAUDE.md and focuses on local files
```

### Per-Package Commands

```bash
# Run tests for a specific package
claude --cwd packages/api "Run the tests and fix any failures"

# Lint a specific package
claude --cwd packages/web "Run the linter and fix all warnings"
```

### Cross-Package Type References

```markdown
# In packages/api/CLAUDE.md, reference shared types explicitly

## Shared Types
This package imports types from @acme/shared:
- User, Tenant, Permission: defined in packages/shared/src/types.ts
- ApiResponse<T>: defined in packages/shared/src/api.ts
- Result<T, E>: defined in packages/shared/src/result.ts

When modifying API endpoints, check if type changes affect @acme/shared.
If yes, update shared types FIRST, then update this package.
```

### Dependency Graph Awareness

```bash
# Help Claude understand package relationships
# Add to root CLAUDE.md:

## Package Dependencies
```
shared  <--  auth  <--  api  <--  web
                   <------------|
```

Build order: shared -> auth -> api -> web
If you change shared, all packages may need updates.
If you change auth, api and web may need updates.
If you change api, only web may need updates.
```

---

## When AI Cannot Help

### Cross-Cutting Concerns

When a change touches 50+ files across multiple modules, AI loses coherence.

```bash
# BAD: Asking AI to do a cross-cutting change in one shot
claude "Rename the User type to Account across the entire codebase"
# Result: misses files, inconsistent renames, breaks imports

# GOOD: AI plans, human executes with IDE tools
claude "I need to rename User to Account across the codebase.
Create a plan listing:
1. All files that reference the User type
2. All database tables/columns that need renaming
3. All API endpoints that use 'user' in URLs
4. Migration steps in order"

# Then use IDE refactoring tools for the actual rename
# (Find and Replace, TypeScript rename symbol, etc.)
```

### Deep Legacy Code

```bash
# When code has no tests, no docs, and complex implicit behavior

# BAD: Asking AI to refactor untested legacy code
claude "Refactor src/legacy/payment-processor.js to TypeScript"
# Result: AI may change behavior it doesn't understand

# GOOD: AI helps you understand first, then you decide
claude "Read src/legacy/payment-processor.js.
List every side effect, every external call, and every implicit behavior.
Then suggest what tests I should write BEFORE any refactoring."

# Write the tests (with AI help), then refactor with safety net
```

### Performance Tuning

```bash
# AI cannot profile your application

# BAD: Asking AI to optimize without data
claude "Make the API faster"

# GOOD: Profile first, then ask AI to optimize specific bottlenecks
# 1. Run your profiler (Node.js: clinic, Python: cProfile, etc.)
# 2. Identify the slow function
# 3. Give AI the specific function and profiling data

claude "This function takes 800ms per call. The profiler shows 90% of
time is in the database query on line 45. The query returns 10K rows
but we only need the first 10. Optimize this."
```

### The AI Plans, Human Executes Pattern

For tasks where AI is useful for thinking but dangerous for doing:

```bash
# Step 1: AI creates the plan
claude "We need to migrate from Express to Fastify.
Create a detailed migration plan:
- What needs to change in each package
- Order of changes to avoid breaking the build
- How to run both frameworks during migration
- Risk assessment for each step
Save to docs/plans/express-to-fastify.md"

# Step 2: Human executes each step, using AI for individual pieces
# The developer follows the plan, asking AI for help on specific steps:
claude --cwd packages/api "Convert src/middleware/auth.ts from Express
middleware to Fastify plugin. Here is the Express version: [paste code]"
```

---

## Real Example: Refactoring a 200K LOC Monolith

A step-by-step approach to breaking a large Node.js monolith into AI-manageable chunks.

### Step 1: Map the Territory

```bash
# Session 1: Understand the structure (don't try to read everything)
claude "This is a 200K LOC Node.js monolith. I need to understand its structure.

Run these commands and analyze the output:
1. find src -type f -name '*.ts' | wc -l  (total files)
2. find src -maxdepth 1 -type d  (top-level directories)
3. cat package.json | jq '.dependencies | keys'  (dependencies)
4. Find the entry point and trace the main initialization

Create a high-level architecture map at docs/architecture.md"
```

### Step 2: Create the CLAUDE.md Hierarchy

```bash
# Session 2: Based on the architecture map, create CLAUDE.md files
claude "Read docs/architecture.md.

Create CLAUDE.md files for:
1. Root: project overview, tech stack, how to run
2. src/api/: API routes and middleware
3. src/services/: Business logic layer
4. src/models/: Data access layer
5. src/utils/: Shared utilities

Each file should describe only its own domain.
Keep each under 50 lines."
```

### Step 3: Identify Extraction Boundaries

```bash
# Session 3: Find what can be extracted into separate packages
claude "Read the CLAUDE.md files and docs/architecture.md.

Analyze the dependency graph between modules:
- Which modules are tightly coupled?
- Which modules have clean boundaries?
- Which modules are used by everything (shared)?

Create a dependency report at docs/dependency-analysis.md
Recommend 3-4 packages to extract first (start with the least coupled)."
```

### Step 4: Extract One Package at a Time

```bash
# Session 4+: Extract one module per session
claude "Read docs/dependency-analysis.md.

We are extracting src/utils/ into packages/shared/.
1. Create the package structure (package.json, tsconfig.json)
2. Move files from src/utils/ to packages/shared/src/
3. Update all imports in the monolith to use @acme/shared
4. Verify the build still works

Do this incrementally. After each file move, check for import errors."
```

### Step 5: Verify at Each Stage

```bash
# After each extraction, verify nothing is broken
claude "Run the full test suite and the build.
If anything fails:
1. Show me the error
2. Explain what broke
3. Fix it
4. Re-run to confirm"
```

### Step 6: Document the New Structure

```bash
# After all extractions, update documentation
claude "Read the current project structure.
Update all CLAUDE.md files to reflect the new monorepo layout.
Update docs/architecture.md with the current state.
List any remaining technical debt in docs/tech-debt.md"
```

### Key Principles for Large Codebase Work

```
1. Never try to load everything at once
   - Scope each session to one module or package
   - Use CLAUDE.md to give AI the map without the territory

2. Use files as session memory
   - Plans, architecture docs, and progress files persist between sessions
   - Update them as you go so the next session has current context

3. Break work into AI-sized chunks
   - Each session should have a clear, bounded goal
   - One module, one feature, one refactoring step

4. AI maps, human navigates
   - Let AI analyze and plan
   - Let humans make architectural decisions
   - Let AI implement within bounded scopes

5. Verify constantly
   - Run tests after every AI change
   - Build after every extraction
   - Never trust "it should work" from AI
```

---

## Summary

Working with large codebases and AI requires discipline:

1. **Layer your CLAUDE.md files**: Each level describes only its own domain
2. **Manage context actively**: Pipe specific files, use --cwd, limit reads
3. **Plan across sessions**: Use files to pass context between sessions
4. **Scope to packages**: In monorepos, work one package at a time
5. **Know AI's limits**: Cross-cutting changes, legacy code, and performance tuning need human hands
6. **Break monoliths into chunks**: Map, plan, extract incrementally, verify constantly
