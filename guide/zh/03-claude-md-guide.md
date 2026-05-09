# CLAUDE.md 指南 — 项目配置最佳实践

> `CLAUDE.md` 是让 Claude 理解你项目的最强大方式。本指南涵盖从基础到高级的所有模式。

## 目录

- [什么是 CLAUDE.md？](#什么是-claudemd)
- [工作原理](#工作原理)
- [必备章节](#必备章节)
- [编写有效的指令](#编写有效的指令)
- [高级模式](#高级模式)
- [按目录配置](#按目录配置)
- [真实案例](#真实案例)
- [常见错误](#常见错误)

---

## 什么是 CLAUDE.md？

`CLAUDE.md` 是一个特殊的 Markdown 文件，Claude Code 在每次会话开始时自动读取。把它看作**项目级的系统提示** — 它告诉 Claude：

- 项目是什么，如何工作
- 使用哪些命令来构建、测试和 lint
- 遵循什么代码规范
- 什么是不应该做的

**影响**：一个写得好的 `CLAUDE.md` 可以减少 80%+ 的重复指令，并大幅提升代码质量。

---

## 工作原理

### 文件位置和优先级

Claude 从多个位置加载 `CLAUDE.md` 文件：

| 位置 | 范围 | 何时使用 |
|------|------|----------|
| `~/.claude/CLAUDE.md` | 全局（所有项目） | 个人偏好、全局工具 |
| `./CLAUDE.md` | 项目根目录 | 项目特定配置（提交到 git） |
| `./src/CLAUDE.md` | 子目录 | 模块级覆盖 |
| `./.claude/CLAUDE.md` | 项目（隐藏） | 不想提交的配置 |

所有文件会被合并 — 子目录文件是添加而非替换父文件。

---

## 必备章节

每个 CLAUDE.md 至少应包含这些章节：

### 1. 项目概述

```markdown
## 项目概述
TaskFlow 是一个用 FastAPI 和 PostgreSQL 构建的任务管理 API。
它为 Web 前端（React）和移动应用（React Native）提供服务。
API 遵循 REST 规范，使用 JWT 认证。
```

### 2. 技术栈

```markdown
## 技术栈
- Python 3.12 + FastAPI
- PostgreSQL 16 + SQLAlchemy 2.0（异步）
- Alembic 做数据库迁移
- pytest 做测试
- Ruff 做代码检查和格式化
- Docker Compose 做本地开发
```

### 3. 命令

```markdown
## 命令
- `make dev` — 启动开发服务器（端口 8000）
- `make test` — 运行所有测试
- `make test-unit` — 只运行单元测试
- `make test-integration` — 运行集成测试（需要数据库）
- `make lint` — 运行 ruff 检查
- `make fmt` — 用 ruff 自动格式化
- `make migrate` — 运行数据库迁移
```

**为什么**：Claude 需要准确知道如何构建、测试和 lint 你的项目。错误的命令 = 浪费时间。

### 4. 代码规范

```markdown
## 代码规范
- 所有函数必须有类型注解
- I/O 操作使用 async def
- 文档字符串：Google 风格，公共函数必须有
- 错误处理：抛出 src/exceptions.py 中的自定义异常
- 日志：使用 structlog，不用 print() 或标准库 logging
- 测试：arrange-act-assert 模式
```

### 5. 架构

```markdown
## 架构
src/
├── api/          # FastAPI 路由处理器（薄层）
├── services/     # 业务逻辑（所有逻辑在这里）
├── models/       # SQLAlchemy 模型
├── schemas/      # Pydantic 请求/响应模式
├── repositories/ # 数据库查询
└── utils/        # 共享工具

tests/ 镜像 src/ 结构
```

---

## 编写有效的指令

### 具体而非模糊

```markdown
# 差 — 太模糊
遵循错误处理的最佳实践。

# 好 — 具体可执行
错误处理规则：
- API 端点：在路由处理器中捕获异常，返回适当的 HTTP 状态码
- 服务层：抛出 src/exceptions.py 中的领域特定异常
- 永远不要捕获宽泛的 Exception — 捕获具体类型
- 总是在重新抛出前用 structlog 记录错误
```

### 使用祈使句

```markdown
# 差
如果能为新功能写测试就好了。

# 好
为所有新功能编写测试。测试文件放在 tests/ 中，镜像 src/ 的结构。
完成前运行 `make test` 进行验证。
```

### 非显而易见的规则要说明原因

```markdown
## 重要说明
- 永远不要使用 `datetime.now()` — 使用 `datetime.utcnow()`
  （服务器在多个时区运行，本地时间会导致 bug）
- 金额始终使用 `Decimal`，永远不用 `float`
  （2024 年因为浮点舍入导致过一次计费事故）
```

---

## 高级模式

### 条件指令

用标题来限定指令的适用范围：

```markdown
## 处理 API 路由时
- 遵循 src/api/ 中的现有模式
- 总是为端点添加 OpenAPI 描述
- 用 Pydantic schema 验证请求体

## 处理数据库模型时
- 模型变更后运行 `make migrate-create NAME=描述性名称`
- 永远不修改已有的迁移文件
- 为 WHERE 子句中使用的列添加索引

## 编写测试时
- 使用 tests/conftest.py 中的 fixture
- 集成测试必须使用测试数据库（不用 mock）
- 使用 `clean_db` fixture 在测试间重置数据库状态
```

### 禁止修改区域

```markdown
## 不要修改
- `src/generated/` — 自动生成的代码，会被覆盖
- `migrations/versions/` — 永远不要编辑已有的迁移
- `.env.production` — 生产环境密钥
- `vendor/` — 第三方依赖
```

---

## 按目录配置

用子目录 `CLAUDE.md` 文件提供模块级上下文：

### 示例：`src/api/CLAUDE.md`

```markdown
# API 路由

所有路由处理器遵循此模式：
1. 验证输入（Pydantic 自动完成）
2. 调用对应的 service 函数
3. 将 service 结果转换为响应 schema
4. 返回适当的状态码

路由处理器应该很薄 — 不要在这里放业务逻辑。
所有业务逻辑属于 src/services/。
```

### 示例：`tests/CLAUDE.md`

```markdown
# 测试

- 使用 conftest.py 中的 pytest fixture
- 工厂函数在 tests/factories.py
- 运行特定测试：`pytest tests/path/to/test.py::test_name -v`
- 需要数据库的测试用 `@pytest.mark.integration` 标记
```

---

## 真实案例

### 全栈 Web 应用

```markdown
# CLAUDE.md — 电商平台

## 概述
全栈电商平台，Next.js 前端 + Node.js/Express 后端。
Turborepo 管理的 Monorepo。

## 技术栈
- 前端：Next.js 14 (App Router)，TypeScript，Tailwind CSS
- 后端：Express.js，TypeScript，Prisma ORM
- 数据库：PostgreSQL 15
- 缓存：Redis
- Monorepo：Turborepo + pnpm workspaces

## 命令
- `pnpm dev` — 启动所有应用
- `pnpm test` — 运行所有测试
- `pnpm lint` — 检查所有包
- `pnpm --filter @app/api test` — 只测试 API

## 规范
- 函数式组件 + hooks（不用 class 组件）
- 默认使用 Server Components
- API 返回 `{ data: T }` 或 `{ error: { message, code } }`
- 用 Zod 做运行时验证
```

---

## 常见错误

### 1. 内容过多
```markdown
# 差 — Claude 不需要小说
这个项目始于 2019 年，当时我们的创始团队发现...

# 好 — 只写事实
## 概述
任务管理 API。FastAPI + PostgreSQL。服务 Web 和移动客户端。
```

### 2. 信息过时
如果 CLAUDE.md 写的是 `npm test` 但项目用的是 `pnpm test`，Claude 会运行错误的命令。**保持更新。**

### 3. 缺少命令
最有影响的部分是**命令**。如果 Claude 不知道怎么运行测试或 lint，它要么猜测要么跳过。

### 4. 忽略文件
很多开发者创建 CLAUDE.md 后就忘了。把它当文档对待 — 项目变化时更新它。

---

## 模板

我们提供即用模板：

- [通用模板](../../templates/CLAUDE.md)
- [Python 模板](../../templates/CLAUDE-python.md)
- [TypeScript 模板](../../templates/CLAUDE-typescript.md)
- [Rust 模板](../../templates/CLAUDE-rust.md)

---

<p align="center">
  <strong>下一篇：</strong> <a href="04-hooks-and-automation.md">Hooks 与自动化</a> — 自动化工作流
</p>
