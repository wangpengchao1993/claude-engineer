# 端到端实战：用 AI 构建任务管理器

> 从零到部署的完整过程。使用 Claude Code 和 GSD 框架构建一个生产级 REST API。

## 目录

- [为什么选这个项目](#为什么选这个项目)
- [前置条件](#前置条件)
- [阶段一：初始化](#阶段一初始化)
- [阶段二：需求与规划](#阶段二需求与规划)
- [阶段三：实现](#阶段三实现)
- [阶段四：测试](#阶段四测试)
- [阶段五：代码审查](#阶段五代码审查)
- [阶段六：Git 工作流](#阶段六git-工作流)
- [阶段七：部署](#阶段七部署)
- [总结与经验教训](#总结与经验教训)
- [动手实践清单](#动手实践清单)

---

## 为什么选这个项目

我们选择 **任务管理器 REST API** 是因为它覆盖了实际开发中的所有核心模式：

| 模式 | 在项目中的体现 |
|------|--------------|
| CRUD 操作 | 任务的增删改查 |
| 用户认证 | JWT 注册/登录 |
| 数据库 | SQLite 及数据迁移 |
| 输入验证 | 数据清洗、错误处理 |
| 测试 | 单元测试 + 集成测试 |
| 部署 | Docker + 云平台 |

**我们要构建的接口：**

```
POST   /api/auth/register    - 注册账号
POST   /api/auth/login       - 登录获取 JWT 令牌
GET    /api/tasks            - 获取任务列表
POST   /api/tasks            - 创建任务
GET    /api/tasks/:id        - 获取单个任务
PUT    /api/tasks/:id        - 更新任务
DELETE /api/tasks/:id        - 删除任务
```

**技术栈：** Node.js + Express + SQLite (better-sqlite3) + Jest + Docker

**预计用时：** 使用 AI 辅助约 60-90 分钟（手动开发需要 4-6 小时）

---

## 前置条件

### 必要工具

```bash
# Node.js 18+（检查版本）
node --version

# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# GSD 框架（可选但推荐）
npm install -g gsd-cli

# 验证安装
claude --version
```

### 配置 API 密钥

```bash
# 设置 Anthropic API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."

# 持久化到 shell 配置文件
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

> **费用估算：** 整个项目大约消耗 200K-400K token，费用约 $3-8（取决于使用的模型）。Sonnet 最经济，Opus 最强但最贵。

---

## 阶段一：初始化

### 1.1 创建项目目录

```bash
mkdir task-manager-api && cd task-manager-api
```

### 1.2 用 GSD 初始化

```bash
gsd init
```

GSD 会创建项目骨架：

```
task-manager-api/
  .gsd/
    config.yml        # GSD 配置
    tasks/            # 任务追踪
  CLAUDE.md           # AI 指令文件
  package.json        # （稍后创建）
```

### 1.3 编写 CLAUDE.md

这是 AI 辅助开发中**最重要**的文件。它相当于你和 AI 之间的"合同"，定义了项目的规则和约定。

> 好的 CLAUDE.md = 好的 AI 输出。花 10 分钟写好它，能节省数小时的修改时间。

```markdown
# 任务管理器 API

## 项目概述
带 JWT 认证的任务管理 REST API。
技术栈：Express.js + better-sqlite3 + Jest。

## 技术栈
- 运行时：Node.js 18+
- 框架：Express.js
- 数据库：SQLite（通过 better-sqlite3，文件：./data/tasks.db）
- 认证：JWT (jsonwebtoken + bcryptjs)
- 测试：Jest + supertest
- 验证：express-validator

## 项目结构
```
src/
  index.js          # 入口文件，启动服务器
  app.js            # Express 应用配置
  db/
    init.js         # 数据库初始化和迁移
    connection.js   # 数据库连接单例
  routes/
    auth.js         # /api/auth/* 路由
    tasks.js        # /api/tasks/* 路由
  middleware/
    auth.js         # JWT 验证中间件
    errorHandler.js # 全局错误处理
    validate.js     # 验证中间件
  models/
    user.js         # 用户模型（数据库查询）
    task.js         # 任务模型（数据库查询）
tests/
  auth.test.js      # 认证端点测试
  tasks.test.js     # 任务端点测试
  helpers/          # 测试工具
```

## 编码约定
- 统一使用 async/await
- 所有路由返回 JSON：{ success: boolean, data?: any, error?: string }
- HTTP 状态码：200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error
- 环境变量通过 .env 文件管理（永远不要提交此文件）
- 数据库文件存放在 ./data/ 目录（已加入 gitignore）

## 命令
- `npm run dev` — 使用 nodemon 启动开发服务器
- `npm test` — 运行所有测试
- `npm test -- --watch` — 监听模式运行测试
- `npm start` — 启动生产服务器

## 测试规则
- 每个路由必须有测试
- 使用 supertest 做集成测试
- 使用独立的测试数据库（./data/test.db）
- 每次测试之间清空数据库
```

### 1.4 初始化 Node.js 项目

打开 Claude Code，输入第一个指令：

```
> 初始化这个 Node.js 项目。按照 CLAUDE.md 中列出的依赖创建 package.json，
  建立目录结构，添加一个基本的 Express 服务器，在 GET /health 上返回
  {"status": "ok"}。
```

**Claude 执行的操作：**

```bash
# Claude 运行这些命令：
npm init -y
npm install express better-sqlite3 jsonwebtoken bcryptjs express-validator dotenv cors
npm install -D jest supertest nodemon

# 创建目录结构
# 创建 src/app.js, src/index.js
# 创建 .env.example, .gitignore
# 更新 package.json 的 scripts
```

**验证：**

```bash
npm run dev
# Server running on port 3000

curl http://localhost:3000/health
# {"status":"ok"}
```

---

## 阶段二：需求与规划

### 2.1 定义功能需求

```
> 规划任务管理器 API。将以下功能分解为可实现的任务：
>
> 需要的功能：
> 1. 用户注册（邮箱/密码）
> 2. 用户登录（返回 JWT 令牌）
> 3. JWT 中间件保护路由
> 4. 任务 CRUD（标题、描述、状态、截止日期）
> 5. 任务只对所属用户可见
> 6. 所有端点的输入验证
> 7. 完善的错误处理
> 8. 完整的测试覆盖
>
> 创建按依赖关系排序的任务列表。每个任务要足够小，
> 可以在一次 Claude Code 会话中完成。
```

### 2.2 Claude 的任务分解

Claude 会产出类似这样的计划：

```
任务 1：数据库设置
  - 创建连接模块
  - 创建初始化脚本（users 和 tasks 表）
  - 添加迁移支持

任务 2：用户模型
  - 创建用户模型：create, findByEmail, findById
  - 使用 bcryptjs 做密码哈希

任务 3：认证路由
  - POST /api/auth/register（验证、创建用户、返回 JWT）
  - POST /api/auth/login（验证、校验密码、返回 JWT）

任务 4：认证中间件
  - JWT 验证中间件
  - 将用户信息挂载到 request 对象

任务 5：任务模型
  - 创建任务模型：create, findAll, findById, update, delete
  - 所有查询限定 user_id 作用域

任务 6：任务路由
  - GET /api/tasks（带分页的列表）
  - POST /api/tasks（带验证的创建）
  - GET /api/tasks/:id（获取单个，验证所有权）
  - PUT /api/tasks/:id（带验证的更新）
  - DELETE /api/tasks/:id（删除，验证所有权）

任务 7：错误处理
  - 全局错误处理中间件
  - 统一错误响应格式

任务 8：测试 - 认证
  - 注册测试（成功、重复、无效输入）
  - 登录测试（成功、密码错误、用户不存在）

任务 9：测试 - 任务
  - 所有端点的 CRUD 测试
  - 权限测试（不能访问其他用户的任务）
  - 验证测试

任务 10：完善
  - 请求日志
  - 速率限制
  - CORS 配置
  - Dockerfile
```

> 10 个任务，按依赖关系排序。每个任务独立可完成，方便跟踪进度。

---

## 阶段三：实现

### 任务 1：数据库设置

```
> 实现任务 1：数据库设置。创建 SQLite 连接模块和初始化脚本。
  需要的表：
  - users (id, email, password_hash, created_at)
  - tasks (id, user_id, title, description, status, due_date, created_at, updated_at)
  使用 better-sqlite3，它是同步的 API。
```

**Claude 创建的代码：**

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
    db.pragma('journal_mode = WAL');    // 提高并发性能
    db.pragma('foreign_keys = ON');     // 启用外键约束
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
      status TEXT DEFAULT 'pending'
        CHECK(status IN ('pending', 'in_progress', 'completed')),
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

**验证：** 启动服务器，确认数据库文件被创建且表结构正确。

### 任务 2：用户模型

```
> 实现任务 2：用户模型。创建 src/models/user.js，包含方法：
  - create(email, password) — 哈希密码、插入、返回用户（不含 password_hash）
  - findByEmail(email) — 返回用户（含 password_hash，用于登录验证）
  - findById(id) — 返回用户（不含 password_hash）
```

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
  return db.prepare(
    'SELECT id, email, created_at FROM users WHERE id = ?'
  ).get(id);
}

module.exports = { create, findByEmail, findById };
```

### 任务 3：认证路由

```
> 实现任务 3：认证路由。创建 src/routes/auth.js：
  - POST /register — 验证邮箱格式和密码长度（最少 8 位），创建用户，返回 JWT
  - POST /login — 验证凭据，返回 JWT
  用 express-validator 做验证。JWT 密钥从 process.env.JWT_SECRET 获取。
  令牌 24 小时过期。遵循 CLAUDE.md 中的响应格式。
```

**关键代码：**

```javascript
// src/routes/auth.js
const express = require('express');
const { body, validationResult } = require('express-validator');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const User = require('../models/user');

const router = express.Router();

// POST /api/auth/register — 注册
router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).withMessage('密码至少 8 个字符')
], (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: '输入验证失败',
        details: errors.array()
      });
    }

    const { email, password } = req.body;

    // 检查用户是否已存在
    const existing = User.findByEmail(email);
    if (existing) {
      return res.status(400).json({
        success: false,
        error: '该邮箱已注册'
      });
    }

    const user = User.create(email, password);
    const token = jwt.sign(
      { id: user.id },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.status(201).json({
      success: true,
      data: { user, token }
    });
  } catch (err) {
    next(err);
  }
});

// POST /api/auth/login — 登录
router.post('/login', [
  body('email').isEmail().normalizeEmail(),
  body('password').notEmpty()
], (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, error: '输入验证失败' });
    }

    const { email, password } = req.body;
    const user = User.findByEmail(email);

    if (!user || !bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({
        success: false,
        error: '邮箱或密码错误'
      });
    }

    const token = jwt.sign(
      { id: user.id },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

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

### 任务 4：认证中间件

```
> 实现任务 4：认证中间件。从 Authorization 头提取 JWT（Bearer 方案），
  验证令牌，将用户对象挂载到 req.user。无效则返回 401。
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
      error: '未提供认证令牌'
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = User.findById(decoded.id);

    if (!user) {
      return res.status(401).json({
        success: false,
        error: '用户不存在'
      });
    }

    req.user = user;
    next();
  } catch (err) {
    return res.status(401).json({
      success: false,
      error: '令牌无效或已过期'
    });
  }
}

module.exports = { authenticate };
```

### 任务 5-6：任务模型和路由

这两个任务的实现方式和前面类似。给 Claude 明确的指令：

```
> 实现任务 5 和 6：任务模型和路由。
  模型方法：create, findAll（带分页）, findById, update（部分更新）, delete
  所有查询必须限定 user_id 作用域。
  路由：完整的 CRUD，所有路由需要认证。
  分页默认值：page=1, limit=20。
  必须验证所有权 — 用户只能操作自己的任务。
```

**实现完成后，手动验证：**

```bash
# 注册用户
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# 响应：
# {"success":true,"data":{"user":{"id":1,"email":"test@example.com"},"token":"eyJ..."}}

# 用获得的 token 创建任务
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"title":"买菜","description":"牛奶、鸡蛋、面包","due_date":"2025-12-31"}'

# 响应：
# {"success":true,"data":{"id":1,"user_id":1,"title":"买菜",...}}
```

> 到这一步，API 已经完全可用了。6 个任务用 Claude Code 约 25 分钟完成。

---

## 阶段四：测试

### 4.1 测试基础设施

```
> 搭建测试基础设施。创建 tests/helpers/setup.js：
  1. 使用测试数据库
  2. 所有测试前初始化数据库
  3. 每个测试之间清空所有表
  4. 所有测试后关闭数据库连接
  5. 提供创建测试用户和获取 JWT 令牌的辅助函数
```

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
  const result = db.prepare(
    'INSERT INTO users (email, password_hash) VALUES (?, ?)'
  ).run(email, passwordHash);
  const user = { id: result.lastInsertRowid, email };
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '24h' });
  return { user, token };
}

module.exports = { setupTestDb, cleanTestDb, teardownTestDb, createTestUser };
```

### 4.2 认证测试

```
> 为认证路由编写全面的测试。覆盖：
  - 成功注册
  - 重复邮箱注册
  - 无效邮箱格式
  - 密码太短
  - 成功登录
  - 密码错误
  - 不存在的用户登录
  - 令牌格式验证
```

**Claude 生成的测试（部分）：**

```javascript
// tests/auth.test.js
const request = require('supertest');
const app = require('../src/app');
const { setupTestDb, cleanTestDb, teardownTestDb } = require('./helpers/setup');

beforeAll(() => setupTestDb());
afterEach(() => cleanTestDb());
afterAll(() => teardownTestDb());

describe('POST /api/auth/register', () => {
  it('成功注册新用户', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'new@example.com', password: 'password123' });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.user.email).toBe('new@example.com');
    expect(res.body.data.token).toBeDefined();
    // 确保不泄露密码哈希
    expect(res.body.data.user.password_hash).toBeUndefined();
  });

  it('拒绝重复邮箱', async () => {
    await request(app)
      .post('/api/auth/register')
      .send({ email: 'dup@example.com', password: 'password123' });

    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'dup@example.com', password: 'password456' });

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });

  it('拒绝无效邮箱', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ email: 'not-an-email', password: 'password123' });

    expect(res.status).toBe(400);
  });

  it('拒绝过短的密码', async () => {
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

  it('正确凭据成功登录', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'login@example.com', password: 'password123' });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.token).toBeDefined();
  });

  it('拒绝错误密码', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'login@example.com', password: 'wrongpass123' });

    expect(res.status).toBe(401);
  });

  it('拒绝不存在的用户', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'nobody@example.com', password: 'password123' });

    expect(res.status).toBe(401);
  });
});
```

### 4.3 任务测试

```
> 为任务路由编写全面的测试。覆盖：
  - 创建任务（成功、缺少标题、无效状态）
  - 列表（空列表、有任务、分页、按状态过滤）
  - 获取单个（成功、不存在、其他用户的任务）
  - 更新（成功、部分更新、无效数据、其他用户的任务）
  - 删除（成功、不存在、其他用户的任务）
  - 所有端点拒绝未认证请求
```

### 4.4 运行测试

```bash
npm test
```

**预期输出：**

```
PASS  tests/auth.test.js
  POST /api/auth/register
    ✓ 成功注册新用户 (45 ms)
    ✓ 拒绝重复邮箱 (12 ms)
    ✓ 拒绝无效邮箱 (8 ms)
    ✓ 拒绝过短的密码 (7 ms)
  POST /api/auth/login
    ✓ 正确凭据成功登录 (89 ms)
    ✓ 拒绝错误密码 (85 ms)
    ✓ 拒绝不存在的用户 (3 ms)

PASS  tests/tasks.test.js
  POST /api/tasks
    ✓ 成功创建任务 (15 ms)
    ✓ 拒绝缺少标题 (5 ms)
    ✓ 拒绝无效状态 (5 ms)
    ✓ 拒绝未认证请求 (3 ms)
  GET /api/tasks
    ✓ 返回空数组 (7 ms)
    ✓ 返回用户任务 (12 ms)
    ✓ 分页结果 (14 ms)
    ✓ 按状态过滤 (10 ms)
  ...

Test Suites: 2 passed, 2 total
Tests:       18 passed, 18 total
```

> 所有 18 个测试全部通过。

---

## 阶段五：代码审查

### 5.1 让 AI 审查自己的代码

这是 AI 辅助开发最有价值的环节之一：让 Claude 对自己写的代码进行**批判性审查**。

```
> 审查整个代码库，检查以下方面：
  1. 安全漏洞（SQL 注入、JWT 问题、密码处理）
  2. 错误处理缺口（数据库文件不存在怎么办？）
  3. 性能问题（缺失索引、N+1 查询）
  4. 代码质量（DRY 违反、模式不一致）
  5. 测试中遗漏的边界情况
  请严格审查，我要找到真正的问题。
```

**Claude 通常会发现这些问题：**

```markdown
## 安全问题

### 1. 认证路由缺少速率限制（高危）
现状：/register 和 /login 没有速率限制。
风险：暴力破解登录、批量注册垃圾账号。
修复：添加 express-rate-limit。

### 2. JWT 密钥环境变量缺少校验（中危）
现状：JWT_SECRET 来自 .env，没有启动时校验。
风险：如果未设置，jsonwebtoken 会使用空字符串。
修复：添加启动检查 — 缺少 JWT_SECRET 时直接崩溃。

## 错误处理

### 3. 数据目录不会自动创建（低危）
现状：如果 ./data/ 目录不存在，better-sqlite3 会崩溃。
修复：在数据库初始化前添加 fs.mkdirSync('./data', { recursive: true })。

## 代码质量

### 4. 更新时间戳不会自动更新（低危）
现状：tasks 表的 updated_at 在 PUT 时不会更新。
修复：在更新查询中显式设置 updated_at = datetime('now')。

## 缺失的测试

### 5. 令牌过期未测试
### 6. 并发请求未测试
### 7. SQL 注入尝试未测试（虽然用了参数化查询，但应该测试确认）
```

### 5.2 修复问题

```
> 修复你发现的所有问题。对每个修复：
  1. 实现修复
  2. 如果适用，添加测试
  3. 确认现有测试仍然通过
```

```bash
# 修复后运行测试：
npm test
# 所有 24 个测试通过（新增 6 个边界情况测试）
```

> 让 AI 审查自己的代码，然后修复发现的问题。这是 AI 辅助开发的"杀手锏"。

---

## 阶段六：Git 工作流

### 6.1 初始化 Git

```
> 初始化 git 仓库。创建合适的 Node.js .gitignore。
  提交所有当前文件。不要提交 .env 或 data/*.db。
```

```bash
git init
# 创建 .gitignore：node_modules/, data/*.db, .env, coverage/

git add -A
git commit -m "feat: 初始化任务管理器 API

- Express.js REST API + SQLite 数据库
- JWT 认证（注册/登录）
- 完整的任务 CRUD 及用户作用域
- express-validator 输入验证
- 24 个测试覆盖所有端点
- 认证路由速率限制"
```

### 6.2 功能分支工作流

添加新功能时使用分支：

```
> 创建功能分支，添加按日期范围过滤任务的功能。
  1. 创建分支 feature/date-filter
  2. 在 GET /api/tasks 上添加 due_before 和 due_after 查询参数
  3. 添加新过滤器的测试
  4. 提交并展示 PR 描述
```

```bash
git checkout -b feature/date-filter
# ... 实现功能 ...
# ... 添加测试 ...
git add -A
git commit -m "feat: 添加任务日期范围过滤

- GET /api/tasks 支持 due_before 和 due_after 查询参数
- ISO 8601 日期格式验证
- 新增 3 个日期过滤测试"
```

### 6.3 创建 Pull Request

```bash
gh pr create \
  --title "添加任务日期范围过滤" \
  --body "## 摘要
- 为 GET /api/tasks 添加 due_before 和 due_after 查询参数
- ISO 8601 日期验证
- 3 个新测试

## 测试方案
\`\`\`bash
npm test -- --testPathPattern=tasks
\`\`\`

所有 27 个测试通过。"
```

---

## 阶段七：部署

### 7.1 创建 Dockerfile

```
> 为这个 API 创建生产级 Dockerfile。使用多阶段构建。
  同时创建 docker-compose.yml 用于本地开发。
  以及 .dockerignore 文件。
```

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine

WORKDIR /app

# 创建非 root 用户（安全最佳实践）
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/node_modules ./node_modules
COPY src/ ./src/
COPY package.json ./

# 创建数据目录
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

### 7.2 环境配置

```javascript
// src/config.js — 启动时验证环境变量
require('dotenv').config();

const requiredVars = ['JWT_SECRET'];

for (const varName of requiredVars) {
  if (!process.env[varName]) {
    console.error(`致命错误：缺少必要的环境变量：${varName}`);
    process.exit(1);
  }
}

module.exports = {
  port: parseInt(process.env.PORT || '3000', 10),
  jwtSecret: process.env.JWT_SECRET,
  nodeEnv: process.env.NODE_ENV || 'development',
};
```

### 7.3 部署到云平台

**方案一：Railway（推荐新手使用，操作简单）**

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 设置环境变量
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables set NODE_ENV=production

# 部署
railway up

# 获取公开 URL
railway domain
```

**方案二：Fly.io（适合有经验的开发者）**

```bash
# 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 启动（自动创建 fly.toml）
fly launch --name task-manager-api

# 设置密钥
fly secrets set JWT_SECRET=$(openssl rand -hex 32)

# 部署
fly deploy

# 检查状态
fly status
```

**方案三：Render（免费套餐可用）**

在 Render 控制台创建 Web Service，连接 GitHub 仓库，设置环境变量即可。

### 7.4 验证部署

```bash
API_URL="https://task-manager-api.up.railway.app"

# 健康检查
curl $API_URL/health
# {"status":"ok"}

# 注册
curl -X POST $API_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"prod@example.com","password":"securepass123"}'

# 部署成功！
```

---

## 总结与经验教训

### 时间对比

| 阶段 | AI 辅助用时 | 手动估计用时 |
|------|-----------|------------|
| 初始化 | 5 分钟 | 20 分钟 |
| 规划 | 10 分钟 | 30 分钟 |
| 实现（6 个任务） | 25 分钟 | 120 分钟 |
| 测试 | 15 分钟 | 60 分钟 |
| 代码审查 + 修复 | 10 分钟 | 40 分钟 |
| Git 工作流 | 5 分钟 | 10 分钟 |
| 部署 | 15 分钟 | 30 分钟 |
| **总计** | **约 85 分钟** | **约 310 分钟** |

> 效率提升约 3.6 倍。最大的时间节省在实现和测试阶段。

### Token 消耗估算

```
阶段 1-2（初始化 + 规划）：  约 30K tokens
阶段 3（实现）：              约 150K tokens
阶段 4（测试）：              约 80K tokens
阶段 5（代码审查）：           约 40K tokens
阶段 6-7（Git + 部署）：      约 30K tokens
────────────────────────────────────────
总计：                        约 330K tokens
Sonnet 预估费用：              约 $2.50
Opus 预估费用：                约 $12.00
```

### 做得好的地方

1. **CLAUDE.md 是最大的功臣** — 清晰的项目结构和约定让 Claude 几乎不偏离方向。每次响应都符合我们定义的模式。

2. **任务分解值得投入** — 将项目拆为 10 个小任务，让每次 AI 交互都聚焦且可预测。

3. **AI 代码审查发现了真实 Bug** — 缺少速率限制和启动验证是真正的生产环境问题。

4. **测试给了信心** — 有 24 个测试通过，重构时毫无顾虑。

### 可以改进的地方

1. **仍需人工验证** — 不要盲目信任 AI 输出。运行代码，阅读代码。

2. **上下文窗口管理** — 大项目中需要适时开启新会话，避免上下文退化。

3. **数据库选择** — SQLite 适合演示，生产环境建议用 PostgreSQL。

4. **错误信息需要更友好** — AI 倾向于使用通用错误信息，需要推动它写出对用户友好的提示。

### 核心原则

```
1. 从 CLAUDE.md 开始 — 它是你和 AI 的合同
2. 先计划再编码 — 10 分钟的规划能节省数小时
3. 小任务，大成果 — 每次 AI 交互只做一个功能
4. 测试一切 — AI 生成的代码同样需要验证
5. 严格审查 — 让 AI 找自己代码的缺陷
6. 频繁提交 — 小而原子的提交，清晰的提交信息
```

---

## 动手实践清单

按照这个清单构建你自己的版本：

- [ ] 安装前置工具（Node.js、Claude Code）
- [ ] 创建项目目录
- [ ] 编写 CLAUDE.md（包含项目约定）
- [ ] 初始化项目（`npm init`，安装依赖）
- [ ] 规划：将功能拆解为 8-12 个小任务
- [ ] 实现任务 1：数据库设置
- [ ] 实现任务 2：用户模型
- [ ] 实现任务 3：认证路由
- [ ] 实现任务 4：认证中间件
- [ ] 实现任务 5：任务模型
- [ ] 实现任务 6：任务路由（CRUD）
- [ ] 实现任务 7：错误处理
- [ ] 编写认证测试（至少 7 个用例）
- [ ] 编写任务测试（至少 12 个用例）
- [ ] 运行所有测试 — 全部通过？
- [ ] AI 代码审查 — 修复所有发现的问题
- [ ] Git 初始化 + 首次提交
- [ ] 创建 Dockerfile
- [ ] 部署到 Railway/Fly.io/Render
- [ ] 用 curl 测试已部署的 API
- [ ] 庆祝！你在 2 小时内用 AI 构建了一个生产级 API。

---

## 扩展项目

完成基础项目后，挑战这些扩展功能：

| 扩展功能 | 难度 | 学到的技能 |
|---------|------|-----------|
| 任务分类/标签 | 简单 | 多对多关系 |
| 全文搜索 | 中等 | SQLite FTS5 |
| 文件附件 | 中等 | 文件上传、存储 |
| WebSocket 通知 | 困难 | 实时通信、ws 库 |
| 团队协作 | 困难 | 角色、权限、共享 |
| GraphQL API | 中等 | apollo-server、schema 设计 |

```
> 为任务管理器添加全文搜索。使用 SQLite FTS5。
  任务应该可以按标题和描述搜索。
  添加 GET /api/tasks/search?q=keyword 端点。
```

---

*下一篇指南：[CI/CD 集成](./12-cicd-integration.md) — 将 AI 引入你的部署流水线。*

---

[← 上一章：高级工作流](10-advanced-workflows.md) | [目录](../../README_zh.md) | [下一章：CI/CD 集成 →](12-cicd-integration.md)
