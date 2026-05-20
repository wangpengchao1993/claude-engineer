# End-to-End Project: Building a Task Manager with AI

> A complete walkthrough from zero to deployed app, using Claude Code and the GSD framework to build a production-ready REST API.
> 端到端实战：用 AI 构建任务管理器 — 从零到部署的完整过程。

## Table of Contents

- [Why This Project](#why-this-project)
- [Prerequisites](#prerequisites)
- [Phase 1: Initialize](#phase-1-initialize)
- [Phase 2: Requirements and Planning](#phase-2-requirements-and-planning)
- [Phase 3: Implementation](#phase-3-implementation)
- [Phase 4: Testing](#phase-4-testing)
- [Phase 5: Code Review](#phase-5-code-review)
- [Phase 6: Git Workflow](#phase-6-git-workflow)
- [Phase 7: Deployment](#phase-7-deployment)
- [Recap and Lessons Learned](#recap-and-lessons-learned)
- [Try It Yourself Checklist](#try-it-yourself-checklist)

---

## Why This Project

We chose a **Task Manager REST API** because it hits every pattern you encounter in real work:

| Pattern | How it appears |
|---------|---------------|
| CRUD operations | Tasks: create, read, update, delete |
| Authentication | JWT-based user signup/login |
| Database | SQLite with migrations |
| Validation | Input sanitization, error handling |
| Testing | Unit + integration tests |
| Deployment | Docker + cloud platform |

> 为什么选这个项目？因为它涵盖了真实开发中的所有常见模式：CRUD、认证、数据库、验证、测试、部署。

**What you'll build:**

```
POST   /api/auth/register    - Create account / 注册
POST   /api/auth/login       - Get JWT token / 登录获取令牌
GET    /api/tasks            - List user's tasks / 获取任务列表
POST   /api/tasks            - Create task / 创建任务
GET    /api/tasks/:id        - Get single task / 获取单个任务
PUT    /api/tasks/:id        - Update task / 更新任务
DELETE /api/tasks/:id        - Delete task / 删除任务
```

**Tech stack:** Node.js + Express + SQLite (via better-sqlite3) + Jest + Docker

**Estimated time with AI:** 60-90 minutes (vs 4-6 hours manually)

---

## Prerequisites

### Tools Required

```bash
# Node.js 18+ (check version / 检查版本)
node --version

# Claude Code (install if needed / 如未安装则安装)
npm install -g @anthropic-ai/claude-code

# GSD framework (optional but recommended / 可选但推荐)
npm install -g gsd-cli

# Verify Claude Code works / 验证 Claude Code 可用
claude --version
```

### API Key Setup

```bash
# Set your Anthropic API key / 设置 API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."

# Or add to your shell profile for persistence / 或添加到 shell 配置文件
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

> **Cost estimate / 费用估算:** This entire project uses approximately 200K-400K tokens, costing $3-8 depending on the model used.

---

## Phase 1: Initialize

### Step 1.1: Create Project Directory

```bash
mkdir task-manager-api && cd task-manager-api
```

### Step 1.2: Initialize with GSD

```bash
gsd init
```

GSD creates the project scaffold:

```
task-manager-api/
  .gsd/
    config.yml        # GSD configuration / GSD 配置
    tasks/            # Task tracking / 任务跟踪
  CLAUDE.md           # AI instructions / AI 指令文件
  package.json        # (will be created)
```

### Step 1.3: Set Up CLAUDE.md

This is the most important file for AI-assisted development. It tells Claude *how* to work in your project.

> CLAUDE.md 是 AI 辅助开发中最重要的文件。它告诉 Claude 如何在你的项目中工作。

```markdown
# Task Manager API

## Project Overview
REST API for task management with JWT authentication.
Built with Express.js, better-sqlite3, and Jest.

## Tech Stack
- Runtime: Node.js 18+
- Framework: Express.js
- Database: SQLite via better-sqlite3 (file: ./data/tasks.db)
- Auth: JWT (jsonwebtoken + bcryptjs)
- Testing: Jest + supertest
- Validation: express-validator

## Project Structure
```
src/
  index.js          # Entry point, server startup
  app.js            # Express app configuration
  db/
    init.js         # Database initialization and migrations
    connection.js   # Database connection singleton
  routes/
    auth.js         # /api/auth/* routes
    tasks.js        # /api/tasks/* routes
  middleware/
    auth.js         # JWT verification middleware
    errorHandler.js # Global error handler
    validate.js     # Validation middleware
  models/
    user.js         # User model (DB queries)
    task.js         # Task model (DB queries)
tests/
  auth.test.js      # Auth endpoint tests
  tasks.test.js     # Task endpoint tests
  helpers/          # Test utilities
```

## Conventions
- Use async/await everywhere
- All routes return JSON: { success: boolean, data?: any, error?: string }
- HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error
- Environment variables via .env file (never commit this)
- Database file stored in ./data/ directory (gitignored)

## Commands
- `npm run dev` — Start dev server with nodemon
- `npm test` — Run all tests
- `npm test -- --watch` — Run tests in watch mode
- `npm start` — Start production server

## Testing Rules
- Every route must have tests
- Use supertest for integration tests
- Use a separate test database (./data/test.db)
- Clean database between test runs
```

### Step 1.4: Initialize Node.js Project

Open Claude Code and start:

```
> Initialize this Node.js project. Set up package.json with the dependencies
  listed in CLAUDE.md, create the directory structure, and add a basic Express
  server that returns {"status": "ok"} on GET /health.
```

**Claude's response** (summarized):

```bash
# Claude runs these commands:
npm init -y
npm install express better-sqlite3 jsonwebtoken bcryptjs express-validator dotenv cors
npm install -D jest supertest nodemon

# Creates directory structure
# Creates src/app.js, src/index.js
# Creates .env.example, .gitignore
# Updates package.json scripts
```

**Verify it works:**

```bash
npm run dev
# Server running on port 3000

curl http://localhost:3000/health
# {"status":"ok"}
```

> 验证：启动服务器后，访问 /health 端点应返回 `{"status":"ok"}`。

---

## Phase 2: Requirements and Planning

### Step 2.1: Define Features with GSD

```bash
gsd plan
```

Or use Claude Code directly:

```
> Plan the task manager API. Break down into implementable tasks:
>
> Features needed:
> 1. User registration with email/password
> 2. User login returning JWT token
> 3. JWT middleware for protected routes
> 4. CRUD operations for tasks (title, description, status, due_date)
> 5. Tasks belong to authenticated user only
> 6. Input validation on all endpoints
> 7. Proper error handling
> 8. Full test coverage
>
> Create a task list ordered by dependency. Each task should be small enough
> to implement in one Claude Code session.
```

### Step 2.2: Claude's Task Breakdown

Claude produces something like this:

```
Task 1: Database Setup
  - Create connection module
  - Create init script with users and tasks tables
  - Add migration support

Task 2: User Model
  - Create user model with: create, findByEmail, findById
  - Password hashing with bcryptjs

Task 3: Auth Routes
  - POST /api/auth/register (validate, create user, return JWT)
  - POST /api/auth/login (validate, verify password, return JWT)

Task 4: Auth Middleware
  - JWT verification middleware
  - Attach user to request object

Task 5: Task Model
  - Create task model with: create, findAll, findById, update, delete
  - All queries scoped to user_id

Task 6: Task Routes
  - GET /api/tasks (list with pagination)
  - POST /api/tasks (create with validation)
  - GET /api/tasks/:id (get single, verify ownership)
  - PUT /api/tasks/:id (update with validation)
  - DELETE /api/tasks/:id (delete, verify ownership)

Task 7: Error Handling
  - Global error handler middleware
  - Consistent error response format
  - Handle database errors, validation errors, auth errors

Task 8: Tests - Auth
  - Registration tests (success, duplicate, invalid input)
  - Login tests (success, wrong password, missing user)

Task 9: Tests - Tasks
  - CRUD tests for all endpoints
  - Authorization tests (can't access other user's tasks)
  - Validation tests

Task 10: Polish
  - Add request logging
  - Add rate limiting
  - Add CORS configuration
  - Create Dockerfile
```

> Claude 将项目分解为 10 个有序任务，每个任务足够小，可以在一次会话中完成。

---

## Phase 3: Implementation

### Task 1: Database Setup

```
> Implement Task 1: Database Setup. Create the SQLite connection module and
  initialization script. Tables needed:
  - users (id, email, password_hash, created_at)
  - tasks (id, user_id, title, description, status, due_date, created_at, updated_at)
  Use better-sqlite3. Make it synchronous (that's how better-sqlite3 works).
```

**Claude creates:**

```javascript
// src/db/connection.js
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = process.env.NODE_ENV === 'test'
  ? path.join(__dirname, '../../data/test.db')
  : path.join(__dirname, '../../data/tasks.db');

let db;

function getDb() {
  if (!db) {
    db = new Database(dbPath);
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
  }
  return db;
}

function closeDb() {
  if (db) {
    db.close();
    db = null;
  }
}

module.exports = { getDb, closeDb };
```

```javascript
// src/db/init.js
const { getDb } = require('./connection');

function initializeDatabase() {
  const db = getDb();

  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      description TEXT DEFAULT '',
      status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed')),
      due_date DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
  `);
}

module.exports = { initializeDatabase };
```

**Quick verification:**

```
> Start the server and verify the database is created. Show me the schema.
```

> 快速验证：启动服务器并确认数据库已创建，检查表结构。

### Task 2: User Model

```
> Implement Task 2: User Model. Create src/models/user.js with methods:
  - create(email, password) — hash password, insert, return user (without password_hash)
  - findByEmail(email) — return user with password_hash (for login verification)
  - findById(id) — return user without password_hash
```

**Claude creates the model:**

```javascript
// src/models/user.js
const bcrypt = require('bcryptjs');
const { getDb } = require('../db/connection');

const SALT_ROUNDS = 10;

function create(email, password) {
  const db = getDb();
  const passwordHash = bcrypt.hashSync(password, SALT_ROUNDS);

  const stmt = db.prepare(
    'INSERT INTO users (email, password_hash) VALUES (?, ?)'
  );

  const result = stmt.run(email, passwordHash);
  return { id: result.lastInsertRowid, email };
}

function findByEmail(email) {
  const db = getDb();
  return db.prepare('SELECT * FROM users WHERE email = ?').get(email);
}

function findById(id) {
  const db = getDb();
  return db.prepare('SELECT id, email, created_at FROM users WHERE id = ?').get(id);
}

module.exports = { create, findByEmail, findById };
```

### Task 3: Auth Routes

```
> Implement Task 3: Auth Routes. Create src/routes/auth.js with:
  - POST /register — validate email format + password min 8 chars, create user, return JWT
  - POST /login — validate credentials, return JWT
  Use express-validator for validation. JWT secret from process.env.JWT_SECRET.
  Token expires in 24 hours. Follow the response format in CLAUDE.md.
```

**Key output from Claude:**

```javascript
// src/routes/auth.js
const express = require('express');
const { body, validationResult } = require('express-validator');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const User = require('../models/user');

const router = express.Router();

// POST /api/auth/register / 注册
router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters')
], (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array()
      });
    }

    const { email, password } = req.body;

    // Check if user exists
    const existing = User.findByEmail(email);
    if (existing) {
      return res.status(400).json({
        success: false,
        error: 'Email already registered'
      });
    }

    const user = User.create(email, password);
    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '24h' });

    res.status(201).json({
      success: true,
      data: { user, token }
    });
  } catch (err) {
    next(err);
  }
});

// POST /api/auth/login / 登录
router.post('/login', [
  body('email').isEmail().normalizeEmail(),
  body('password').notEmpty()
], (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, error: 'Validation failed' });
    }

    const { email, password } = req.body;
    const user = User.findByEmail(email);

    if (!user || !bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({ success: false, error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '24h' });

    res.json({
      success: true,
      data: {
        user: { id: user.id, email: user.email },
        token
      }
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
```

### Task 4: Auth Middleware

```
> Implement Task 4: Auth Middleware. Create src/middleware/auth.js.
  Extract JWT from Authorization header (Bearer scheme).
  Verify token, attach user object to req.user. Return 401 if invalid.
```

```javascript
// src/middleware/auth.js
const jwt = require('jsonwebtoken');
const User = require('../models/user');

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      success: false,
      error: 'No token provided'
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = User.findById(decoded.id);

    if (!user) {
      return res.status(401).json({ success: false, error: 'User not found' });
    }

    req.user = user;
    next();
  } catch (err) {
    return res.status(401).json({ success: false, error: 'Invalid token' });
  }
}

module.exports = { authenticate };
```

### Task 5: Task Model

```
> Implement Task 5: Task Model. Create src/models/task.js with methods:
  - create(userId, { title, description, status, due_date })
  - findAll(userId, { page, limit, status }) — with pagination
  - findById(id, userId) — scoped to user
  - update(id, userId, updates) — partial update
  - delete(id, userId) — return boolean success
```

### Task 6: Task Routes

```
> Implement Task 6: Task Routes. Create src/routes/tasks.js.
  All routes require authentication. Use express-validator for input validation.
  Pagination defaults: page=1, limit=20.
  Include ownership verification — users can only access their own tasks.
```

**At this point, the API is functional. Test manually:**

```bash
# Register a user / 注册用户
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Response:
# {"success":true,"data":{"user":{"id":1,"email":"test@example.com"},"token":"eyJ..."}}

# Create a task (use the token from above) / 创建任务
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread","due_date":"2025-12-31"}'

# Response:
# {"success":true,"data":{"id":1,"user_id":1,"title":"Buy groceries",...}}
```

> 到此为止，API 已经可以工作了。可以用 curl 手动测试注册、登录和创建任务。

---

## Phase 4: Testing

### Step 4.1: Test Setup

```
> Set up the test infrastructure. Create tests/helpers/setup.js that:
  1. Uses the test database
  2. Initializes the database before all tests
  3. Cleans all tables between tests
  4. Closes the database connection after all tests
  5. Provides a helper to create a test user and get a JWT token
```

**Claude creates:**

```javascript
// tests/helpers/setup.js
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret-key';

const { getDb, closeDb } = require('../../src/db/connection');
const { initializeDatabase } = require('../../src/db/init');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

function setupTestDb() {
  initializeDatabase();
}

function cleanTestDb() {
  const db = getDb();
  db.exec('DELETE FROM tasks');
  db.exec('DELETE FROM users');
}

function teardownTestDb() {
  closeDb();
}

function createTestUser(email = 'test@example.com', password = 'password123') {
  const db = getDb();
  const passwordHash = bcrypt.hashSync(password, 10);
  const result = db.prepare('INSERT INTO users (email, password_hash) VALUES (?, ?)').run(email, passwordHash);
  const user = { id: result.lastInsertRowid, email };
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '24h' });
  return { user, token };
}

module.exports = { setupTestDb, cleanTestDb, teardownTestDb, createTestUser };
```

### Step 4.2: Auth Tests

```
> Write comprehensive tests for auth routes. Cover:
  - Successful registration
  - Duplicate email registration
  - Invalid email format
  - Password too short
  - Successful login
  - Login with wrong password
  - Login with non-existent email
  - Token format validation
```

**Claude generates tests:**

```javascript
// tests/auth.test.js
const request = require('supertest');
const app = require('../src/app');
const { setupTestDb, cleanTestDb, teardownTestDb } = require('./helpers/setup');

beforeAll(() => setupTestDb());
afterEach(() => cleanTestDb());
afterAll(() => teardownTestDb());

describe('POST /api/auth/register', () => {
  it('should register a new user', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'new@example.com', password: 'password123' });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.user.email).toBe('new@example.com');
    expect(res.body.data.token).toBeDefined();
    expect(res.body.data.user.password_hash).toBeUndefined(); // Never expose hash
  });

  it('should reject duplicate email', async () => {
    await request(app)
      .post('/api/auth/register')
      .send({ email: 'dup@example.com', password: 'password123' });

    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'dup@example.com', password: 'password456' });

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });

  it('should reject invalid email', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'not-an-email', password: 'password123' });

    expect(res.status).toBe(400);
  });

  it('should reject short password', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'test@example.com', password: '123' });

    expect(res.status).toBe(400);
  });
});

describe('POST /api/auth/login', () => {
  beforeEach(async () => {
    await request(app)
      .post('/api/auth/register')
      .send({ email: 'login@example.com', password: 'password123' });
  });

  it('should login with valid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'login@example.com', password: 'password123' });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.token).toBeDefined();
  });

  it('should reject wrong password', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'login@example.com', password: 'wrongpass123' });

    expect(res.status).toBe(401);
  });

  it('should reject non-existent user', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'nobody@example.com', password: 'password123' });

    expect(res.status).toBe(401);
  });
});
```

### Step 4.3: Task Tests

```
> Write comprehensive tests for task routes. Cover:
  - Create task (success, missing title, invalid status)
  - List tasks (empty, with tasks, pagination, filter by status)
  - Get single task (success, not found, wrong user)
  - Update task (success, partial update, invalid data, wrong user)
  - Delete task (success, not found, wrong user)
  - All endpoints reject unauthenticated requests
```

### Step 4.4: Run Tests

```bash
npm test
```

**Expected output:**

```
PASS  tests/auth.test.js
  POST /api/auth/register
    ✓ should register a new user (45 ms)
    ✓ should reject duplicate email (12 ms)
    ✓ should reject invalid email (8 ms)
    ✓ should reject short password (7 ms)
  POST /api/auth/login
    ✓ should login with valid credentials (89 ms)
    ✓ should reject wrong password (85 ms)
    ✓ should reject non-existent user (3 ms)

PASS  tests/tasks.test.js
  POST /api/tasks
    ✓ should create a task (15 ms)
    ✓ should reject missing title (5 ms)
    ✓ should reject invalid status (5 ms)
    ✓ should reject unauthenticated request (3 ms)
  GET /api/tasks
    ✓ should return empty array (7 ms)
    ✓ should return user tasks (12 ms)
    ✓ should paginate results (14 ms)
    ✓ should filter by status (10 ms)
  ...

Test Suites: 2 passed, 2 total
Tests:       18 passed, 18 total
```

> 运行 `npm test`，所有 18 个测试应全部通过。

---

## Phase 5: Code Review

### Step 5.1: AI Reviews Its Own Code

This is where AI-assisted development gets powerful. Ask Claude to critically review everything:

> 这是 AI 辅助开发最强大的地方。让 Claude 批判性地审查自己写的代码。

```
> Review the entire codebase for:
  1. Security vulnerabilities (SQL injection, JWT issues, password handling)
  2. Error handling gaps (what happens if the database file is missing?)
  3. Performance issues (missing indexes, N+1 queries)
  4. Code quality (DRY violations, inconsistent patterns)
  5. Missing edge cases in tests
  Be brutally honest. I want to find real issues.
```

**Claude's typical findings:**

```markdown
## Security Issues Found

### 1. Missing Rate Limiting on Auth Routes (HIGH)
Current state: No rate limiting on /register and /login.
Risk: Brute force attacks on login, spam accounts on register.
Fix: Add express-rate-limit.

### 2. JWT Secret from Environment (MEDIUM)
Current state: JWT_SECRET comes from .env with no fallback validation.
Risk: If JWT_SECRET is missing, jsonwebtoken uses empty string.
Fix: Add startup check — crash if JWT_SECRET is not set.

## Error Handling Gaps

### 3. Database Directory Not Auto-Created (LOW)
Current state: If ./data/ directory doesn't exist, better-sqlite3 crashes.
Fix: Add fs.mkdirSync('./data', { recursive: true }) before database init.

## Code Quality

### 4. Timestamp Update Not Automatic (LOW)
Current state: updated_at on tasks table isn't updated on PUT.
Fix: Add explicit updated_at = datetime('now') in update query.

## Missing Tests

### 5. Token Expiration Not Tested
### 6. Concurrent Request Handling Not Tested
### 7. SQL Injection Attempts Not Tested (even though parameterized queries are used, test to confirm)
```

### Step 5.2: Fix the Issues

```
> Fix all the issues you found. For each fix:
  1. Implement the fix
  2. Add a test if applicable
  3. Verify existing tests still pass
```

**Claude implements fixes one by one:**

```bash
# After fixes:
npm test
# All 24 tests pass (6 new tests added for edge cases)
```

---

## Phase 6: Git Workflow

### Step 6.1: Initialize Git

```
> Initialize a git repository. Create a proper .gitignore for Node.js.
  Make an initial commit with all current files. Do NOT commit .env or data/*.db.
```

**Claude runs:**

```bash
git init
# Creates .gitignore with: node_modules/, data/*.db, .env, coverage/

git add -A
git commit -m "feat: initial task manager API with auth and CRUD

- Express.js REST API with SQLite database
- JWT authentication (register/login)
- Full CRUD for tasks with user scoping
- Input validation with express-validator
- 24 tests covering all endpoints
- Rate limiting on auth routes"
```

### Step 6.2: Feature Branch Workflow

For additional features, use branches:

```
> Create a feature branch and add task filtering by date range.
  1. Create branch feature/date-filter
  2. Add query params: due_before, due_after on GET /api/tasks
  3. Add tests for the new filter
  4. Commit and show me the PR description
```

**Claude's workflow:**

```bash
git checkout -b feature/date-filter
# ... implements the feature ...
# ... adds tests ...
git add -A
git commit -m "feat: add date range filtering for tasks

- GET /api/tasks now accepts due_before and due_after query params
- Dates validated as ISO 8601 format
- Added 3 tests for date filtering"
```

### Step 6.3: Create a Pull Request

```
> Create a PR for this branch. Write a clear description with:
  - Summary of changes
  - How to test
  - Screenshots of test output
```

```bash
gh pr create \
  --title "Add date range filtering for tasks" \
  --body "## Summary
- Added due_before and due_after query parameters to GET /api/tasks
- ISO 8601 date validation
- 3 new tests

## Test Plan
\`\`\`bash
npm test -- --testPathPattern=tasks
\`\`\`

## Test Output
All 27 tests passing."
```

> 使用 `gh pr create` 创建 Pull Request，包含清晰的描述和测试说明。

---

## Phase 7: Deployment

### Step 7.1: Create Dockerfile

```
> Create a production Dockerfile for this API. Use multi-stage build.
  Also create docker-compose.yml for local development.
  And create a .dockerignore file.
```

**Claude creates:**

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine

WORKDIR /app

# Create non-root user / 创建非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/node_modules ./node_modules
COPY src/ ./src/
COPY package.json ./

# Create data directory / 创建数据目录
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

USER appuser

EXPOSE 3000
ENV NODE_ENV=production

CMD ["node", "src/index.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - NODE_ENV=production
      - PORT=3000
    volumes:
      - task-data:/app/data
    restart: unless-stopped

volumes:
  task-data:
```

### Step 7.2: Environment Configuration

```
> Create environment configs for dev, staging, and production.
  Use .env files with appropriate defaults. Add a config validation
  module that crashes on startup if required vars are missing.
```

```javascript
// src/config.js
require('dotenv').config();

const requiredVars = ['JWT_SECRET'];

for (const varName of requiredVars) {
  if (!process.env[varName]) {
    console.error(`FATAL: Missing required environment variable: ${varName}`);
    process.exit(1);
  }
}

module.exports = {
  port: parseInt(process.env.PORT || '3000', 10),
  jwtSecret: process.env.JWT_SECRET,
  nodeEnv: process.env.NODE_ENV || 'development',
};
```

### Step 7.3: Deploy to Railway

```
> Help me deploy this to Railway. What do I need?
```

**Claude's instructions:**

```bash
# Install Railway CLI / 安装 Railway CLI
npm install -g @railway/cli

# Login / 登录
railway login

# Initialize project / 初始化项目
railway init

# Set environment variables / 设置环境变量
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables set NODE_ENV=production

# Deploy / 部署
railway up

# Get public URL / 获取公开 URL
railway domain
```

**Alternative: Deploy to Fly.io**

```bash
# Install flyctl / 安装 flyctl
curl -L https://fly.io/install.sh | sh

# Login / 登录
fly auth login

# Launch (creates fly.toml) / 启动
fly launch --name task-manager-api

# Set secrets / 设置密钥
fly secrets set JWT_SECRET=$(openssl rand -hex 32)

# Deploy / 部署
fly deploy

# Check status / 检查状态
fly status
```

### Step 7.4: Verify Deployment

```bash
# Test the deployed API / 测试已部署的 API
API_URL="https://task-manager-api.up.railway.app"

# Health check / 健康检查
curl $API_URL/health

# Register / 注册
curl -X POST $API_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"prod@example.com","password":"securepass123"}'

# 🎉 It works! / 部署成功！
```

---

## Recap and Lessons Learned

### Timeline

| Phase | Time (with AI) | Time (manual estimate) |
|-------|----------------|----------------------|
| Initialize | 5 min | 20 min |
| Planning | 10 min | 30 min |
| Implementation (6 tasks) | 25 min | 120 min |
| Testing | 15 min | 60 min |
| Code Review + Fixes | 10 min | 40 min |
| Git Workflow | 5 min | 10 min |
| Deployment | 15 min | 30 min |
| **Total** | **~85 min** | **~310 min** |

> 用 AI 辅助开发，总时间约 85 分钟，手动开发估计需要 310 分钟。效率提升约 3.6 倍。

### Token Usage Estimate

```
Phase 1-2 (Init + Plan):     ~30K tokens
Phase 3 (Implementation):    ~150K tokens
Phase 4 (Testing):           ~80K tokens
Phase 5 (Code Review):       ~40K tokens
Phase 6-7 (Git + Deploy):    ~30K tokens
─────────────────────────────────────────
Total:                        ~330K tokens
Estimated cost (Sonnet):      ~$2.50
Estimated cost (Opus):        ~$12.00
```

### What Went Well

1. **CLAUDE.md was the game changer** — Having clear project structure and conventions meant Claude rarely went off track. Every response matched our patterns.

2. **Task decomposition paid off** — Breaking the project into 10 small tasks kept each AI interaction focused and predictable.

3. **AI code review caught real bugs** — The missing rate limiter and startup validation were legitimate production issues.

4. **Tests gave confidence** — With 24 tests passing, refactoring was fearless.

> CLAUDE.md 是关键 — 清晰的项目结构和约定让 Claude 几乎不会偏离方向。

### What Could Be Better

1. **Manual verification still needed** — Don't blindly trust AI output. Run the code. Read the code.

2. **Context window management** — On larger projects, you'll need to start new sessions to avoid context degradation.

3. **Database choice** — SQLite is great for demos but you'd want PostgreSQL for real production apps.

4. **Error messages could be more helpful** — AI tends to use generic error messages. Push for user-friendly ones.

### Key Principles Learned

```
1. Start with CLAUDE.md — it's your AI contract
2. Plan before coding — even 10 minutes of planning saves hours
3. Small tasks, big results — one feature per AI interaction
4. Test everything — AI-generated code needs verification too
5. Review ruthlessly — ask AI to find flaws in its own work
6. Commit often — small, atomic commits with clear messages
```

> 关键原则：从 CLAUDE.md 开始、先计划再编码、小任务大成果、测试一切、严格审查、频繁提交。

---

## Try It Yourself Checklist

Use this checklist to build your own version:

- [ ] Install prerequisites (Node.js, Claude Code)
- [ ] Create project directory
- [ ] Write CLAUDE.md with your project's conventions
- [ ] Initialize project (`npm init`, install dependencies)
- [ ] Plan: Break features into 8-12 small tasks
- [ ] Implement Task 1: Database setup
- [ ] Implement Task 2: User model
- [ ] Implement Task 3: Auth routes
- [ ] Implement Task 4: Auth middleware
- [ ] Implement Task 5: Task model
- [ ] Implement Task 6: Task routes (CRUD)
- [ ] Implement Task 7: Error handling
- [ ] Write auth tests (aim for 7+ test cases)
- [ ] Write task tests (aim for 12+ test cases)
- [ ] Run all tests — all green?
- [ ] AI code review — fix all findings
- [ ] Git init + first commit
- [ ] Create Dockerfile
- [ ] Deploy to Railway/Fly.io/Render
- [ ] Test deployed API with curl
- [ ] Celebrate! You built a production API with AI in under 2 hours.

> 按照清单一步步完成。你可以在 2 小时内用 AI 构建一个生产级 API！

---

## Extend the Project

Once you've completed the base project, try these extensions:

| Extension | Difficulty | New Skills |
|-----------|-----------|------------|
| Add task categories/tags | Easy | Many-to-many relationships |
| Add task search (full text) | Medium | SQLite FTS5 |
| Add file attachments | Medium | File upload, storage |
| Add WebSocket notifications | Hard | Real-time, ws library |
| Add team collaboration | Hard | Roles, permissions, sharing |
| Add GraphQL API | Medium | apollo-server, schema design |

```
> Add full-text search to the task manager. Use SQLite FTS5.
  Tasks should be searchable by title and description.
  Add GET /api/tasks/search?q=keyword endpoint.
```

> 完成基础项目后，尝试添加扩展功能来挑战自己。

---

*Next guide: [CI/CD Integration](./12-cicd-integration.md) — Take AI into your deployment pipeline.*
