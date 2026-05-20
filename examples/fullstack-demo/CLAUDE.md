# Task Manager -- CLAUDE.md

## Project Overview

A fullstack task management application with an Express.js REST API backend,
React 18 frontend, and SQLite database. Users can create, update, complete,
and delete tasks. Tasks support titles, descriptions, due dates, priority
levels, and tags.

## Tech Stack

- **Backend**: Express.js 4.x on Node.js 20 LTS
- **Frontend**: React 18 + Vite 5
- **Database**: SQLite via better-sqlite3 (file: `backend/data/tasks.db`)
- **Auth**: JWT tokens (access + refresh), stored in httpOnly cookies
- **Testing**: Jest + supertest (backend), Vitest + React Testing Library (frontend)
- **Linting**: ESLint 8 with Prettier, shared config in root `.eslintrc.json`
- **Containerization**: Docker + docker-compose

## Commands

```bash
# Development / 开发
cd backend && npm run dev        # Start backend with nodemon on :3001
cd frontend && npm run dev       # Start frontend with Vite on :5173

# Testing / 测试
cd backend && npm test           # Run Jest tests (unit + integration)
cd backend && npm run test:watch # Jest in watch mode
cd frontend && npm test          # Run Vitest tests
cd frontend && npm run test:ui   # Vitest with UI

# Single test file / 单个测试文件
cd backend && npx jest tests/tasks.test.js
cd frontend && npx vitest run src/components/TaskList.test.jsx

# Linting / 代码检查
npm run lint                     # ESLint across entire project
npm run lint:fix                 # Auto-fix lint issues

# Build / 构建
cd frontend && npm run build     # Production build to frontend/dist/

# Database / 数据库
cd backend && npm run db:migrate # Run pending migrations
cd backend && npm run db:seed    # Seed sample data
cd backend && npm run db:reset   # Drop and recreate (dev only)

# Docker / Docker
docker-compose up                # Start all services
docker-compose up --build        # Rebuild and start
```

## Architecture

### Backend (`backend/src/`)

```
src/
├── index.js              # App entry, middleware setup, route mounting
├── routes/
│   ├── tasks.js          # GET/POST/PUT/DELETE /api/tasks
│   ├── auth.js           # POST /api/auth/login, /api/auth/refresh
│   └── health.js         # GET /api/health
├── models/
│   └── task.js           # Data access layer -- all SQL lives here
├── middleware/
│   ├── auth.js           # verifyToken, requireAuth
│   ├── errors.js         # centralErrorHandler, AppError class
│   ├── validate.js       # Request validation via Joi schemas
│   └── rateLimiter.js    # express-rate-limit config
├── db/
│   ├── connection.js     # SQLite connection singleton
│   ├── schema.sql        # Initial schema
│   └── migrate.js        # Sequential migration runner
├── utils/
│   └── logger.js         # pino logger instance
└── config.js             # Environment-based configuration
```

### Frontend (`frontend/src/`)

```
src/
├── main.jsx              # ReactDOM.createRoot entry
├── App.jsx               # Router setup, global providers
├── components/
│   ├── TaskList.jsx      # Displays tasks, handles filtering/sorting
│   ├── TaskForm.jsx      # Create + edit form with validation
│   ├── TaskCard.jsx      # Single task display card
│   ├── Header.jsx        # Navigation bar
│   └── ui/               # Reusable primitives (Button, Input, Modal)
├── hooks/
│   ├── useTasks.js       # CRUD operations, caching, optimistic updates
│   ├── useAuth.js        # Login state, token refresh
│   └── useDebounce.js    # Input debouncing
├── api/
│   └── client.js         # Axios instance with interceptors
├── pages/
│   ├── Dashboard.jsx     # Main task list page
│   ├── Login.jsx         # Authentication page
│   └── NotFound.jsx      # 404 page
├── context/
│   └── AuthContext.jsx   # Auth state provider
└── styles/
    └── index.css         # Tailwind CSS entry
```

## Code Conventions

### General

- Use **ES modules** (`import`/`export`) everywhere, not CommonJS
- Prefer `const` over `let`; never use `var`
- Use **async/await** instead of raw Promises or callbacks
- All functions must have JSDoc comments with `@param` and `@returns`
- File names: `camelCase.js` for utilities, `PascalCase.jsx` for components
- Maximum line length: 100 characters

### Backend Specific

- Route handlers are thin -- business logic goes in models or service functions
- All SQL lives in `models/*.js` -- never write SQL in route files
- Use parameterized queries exclusively -- never interpolate user input into SQL
- Every route must validate input with a Joi schema before processing
- Error responses always use `AppError` class from `middleware/errors.js`
- Log all errors with context via the pino logger, never `console.log`

### Frontend Specific

- Functional components only -- no class components
- State management: React Context + `useReducer` for global state, `useState` for local
- Data fetching: custom hooks in `hooks/` directory, not in components
- Props: destructure in function signature, define PropTypes for all components
- CSS: Tailwind utility classes, no inline styles, no CSS modules
- Tests: prefer `userEvent` over `fireEvent`, query by role/label not test IDs

### API Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": { "page": 1, "total": 42 }
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": [...]
  }
}
```

### Database Conventions

- Table names: `snake_case`, plural (`tasks`, `user_sessions`)
- Column names: `snake_case` (`created_at`, `due_date`)
- Always include `id` (INTEGER PRIMARY KEY), `created_at`, `updated_at`
- Soft-delete with `deleted_at` column, never hard-delete user data
- Migrations are numbered sequentially: `001_create_tasks.sql`, `002_add_tags.sql`

## Important Patterns

### Error Handling

```javascript
// In routes -- throw AppError, middleware catches it
// 在路由中 -- 抛出 AppError，由中间件捕获
throw new AppError('Task not found', 404, 'TASK_NOT_FOUND');
```

### Authentication Flow

1. Client sends credentials to `POST /api/auth/login`
2. Server returns access token (15 min) + refresh token (7 days) in httpOnly cookies
3. Client includes cookies automatically on subsequent requests
4. `verifyToken` middleware validates on every protected route
5. Client calls `POST /api/auth/refresh` before access token expires

### Optimistic Updates (Frontend)

The `useTasks` hook updates the UI immediately, then syncs with the server.
On failure, it reverts to the previous state and shows an error toast.

## Things to Avoid

- **Do not** add new npm dependencies without discussing first
- **Do not** modify migration files that have already been applied
- **Do not** store secrets in code -- use environment variables via `config.js`
- **Do not** use `any` type annotations (we use JSDoc for type safety)
- **Do not** write raw SQL outside of `models/` directory
- **Do not** use `dangerouslySetInnerHTML` in React components
- **Do not** disable ESLint rules with inline comments
- **Do not** commit `.env` files or the `tasks.db` database file
- **Do not** use `setTimeout` or `setInterval` for business logic
- **Do not** add backend dependencies to the frontend package or vice versa

## Environment Variables

```bash
# Backend (.env)
PORT=3001                          # Server port / 服务端口
NODE_ENV=development               # Environment / 环境
JWT_SECRET=<random-string>         # Token signing key / 令牌签名密钥
JWT_REFRESH_SECRET=<random-string> # Refresh token key / 刷新令牌密钥
DB_PATH=./data/tasks.db            # SQLite file path / 数据库路径
LOG_LEVEL=debug                    # Pino log level / 日志级别

# Frontend (.env)
VITE_API_URL=http://localhost:3001 # Backend URL / 后端地址
```

## Notes

- The SQLite database file is created automatically on first run
- Backend auto-restarts on file changes via nodemon in dev mode
- Frontend hot-reloads via Vite HMR
- Tests use an in-memory SQLite database, not the development database
- Docker compose mounts `backend/data/` as a volume for database persistence
