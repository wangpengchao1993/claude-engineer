# 大型代码库的 AI 管理

> 在 100K+ 行代码的项目中有效使用 Claude Code 的策略：上下文管理、CLAUDE.md 分层、多会话工作流、Monorepo 模式，以及了解 AI 何时无法帮忙。

## 目录

- [上下文挑战](#上下文挑战)
- [CLAUDE.md 分层策略](#claudemd-分层策略)
- [上下文管理技巧](#上下文管理技巧)
- [多会话工作流](#多会话工作流)
- [Monorepo 策略](#monorepo-策略)
- [AI 无法帮忙的场景](#ai-无法帮忙的场景)
- [实战案例：重构 200K 行 Node.js 单体应用](#实战案例重构-200k-行-nodejs-单体应用)

---

## 上下文挑战

大型代码库无法装进 AI 上下文窗口。一个 100K+ 行代码的项目可能有数千个文件，而 Claude Code 在单次会话中只能容纳其中一小部分。

```
典型项目规模 vs 上下文：
- 小型项目（5K 行）：   轻松容纳，AI 可以看到所有内容
- 中型项目（20K 行）：  小心使用可以容纳，聚焦相关模块
- 大型项目（100K 行）： 无法容纳，必须使用选择性策略
- 单体应用（500K+ 行）：需要严格的作用域和多会话工作

解决方案不是把所有东西都塞进上下文。
解决方案是为每个任务给 AI 正确的上下文。
```

### 为什么"全部读取"行不通

```bash
# 错误：尝试加载整个代码库
claude "读取 src/ 中的所有文件，然后重构 auth 模块"
# 结果：上下文被无关代码填满，AI 失去焦点

# 正确：有目标的上下文加载
claude "读取 src/auth/ 和 src/types/auth.ts，然后重构令牌刷新逻辑"
# 结果：AI 恰好拥有它需要的内容
```

---

## CLAUDE.md 分层策略

大型代码库的关键是 CLAUDE.md 文件的层级结构。每个层级只描述自己的领域。

### 三层层级结构

```
项目根目录/
  CLAUDE.md                           # 第 1 层：项目概览
  packages/
    auth/
      CLAUDE.md                       # 第 2 层：Auth 模块详情
      src/
        providers/
          CLAUDE.md                   # 第 3 层：OAuth 提供商细节
    api/
      CLAUDE.md                       # 第 2 层：API 模块详情
    web/
      CLAUDE.md                       # 第 2 层：前端详情
    shared/
      CLAUDE.md                       # 第 2 层：共享工具
```

### 第 1 层：根目录 CLAUDE.md（项目概览）

```markdown
# Acme 平台

## 架构
由 Turborepo 管理的 4 个包的 Monorepo：
- packages/auth：认证服务（Express, JWT, OAuth）
- packages/api：REST API 网关（Express, OpenAPI）
- packages/web：面向客户的 SPA（React, Vite）
- packages/shared：共享类型和工具

## 技术栈
- 语言：TypeScript 5.4（严格模式）
- 运行时：Node.js 20 LTS
- 数据库：PostgreSQL 16 via Drizzle ORM
- 缓存：Redis 7
- 队列：BullMQ
- CI：GitHub Actions

## 关键约定
- 仅使用命名导出（不用默认导出）
- 错误处理使用 Result<T, E> 模式（见 packages/shared/src/result.ts）
- 所有 API 端点使用 zod 验证（见 packages/api/src/validation/）
- 数据库迁移在 packages/api/drizzle/

## 如何运行
- `npm run dev`：以开发模式启动所有包
- `npm run test`：运行所有测试
- `npm run build`：构建所有包

## 模块负责人
- auth: @alice
- api: @bob
- web: @carol
- shared: @dave
```

### 第 2 层：模块 CLAUDE.md

```markdown
# packages/auth/CLAUDE.md

## 用途
处理所有认证和授权。签发 JWT、管理会话、
集成 OAuth 提供商，并执行 RBAC 策略。

## 架构
```
src/
  index.ts          # Express 应用设置和路由注册
  jwt.ts            # 令牌创建、验证、刷新
  session.ts        # 会话存储（Redis 后端）
  rbac.ts           # 基于角色的访问控制中间件
  providers/        # OAuth 提供商适配器
    google.ts
    github.ts
    base.ts         # 提供商抽象基类
  middleware/
    authenticate.ts # 验证 JWT 的 Express 中间件
    authorize.ts    # 检查权限的 Express 中间件
  types.ts          # Auth 特定类型（也从 shared 重新导出）
```

## 关键模式
- 所有提供商继承 BaseOAuthProvider（src/providers/base.ts）
- 令牌刷新使用滑动窗口：TTL 剩余 <25% 时刷新
- 会话存储在 Redis 中，前缀为 "session:"
- RBAC 权限在 src/permissions.ts 中定义（唯一事实来源）

## 测试
- 单元测试：以 *.test.ts 放在同级目录
- 集成测试：__tests__/integration/（需要 Redis + PostgreSQL）
- 运行：`npm run test -w packages/auth`

## 常见任务
- 添加新 OAuth 提供商：复制 src/providers/google.ts，继承 BaseOAuthProvider
- 添加新权限：更新 src/permissions.ts，添加迁移
- 更改令牌 TTL：更新 src/config.ts 中的配置（没有硬编码）
```

### 第 3 层：子模块 CLAUDE.md

```markdown
# packages/auth/src/providers/CLAUDE.md

## OAuth 提供商适配器

每个文件实现一个 OAuth 提供商。全部继承 BaseOAuthProvider。

## 添加新提供商
1. 创建新文件：`{provider-name}.ts`
2. 继承 BaseOAuthProvider
3. 实现必需方法：
   - `getAuthorizationUrl(state: string): string`
   - `exchangeCode(code: string): Promise<OAuthTokens>`
   - `getUserProfile(accessToken: string): Promise<OAuthProfile>`
4. 在 `index.ts` 的提供商映射中注册
5. 将提供商配置添加到环境变量

## 测试提供商
- Mock HTTP 调用（测试中永远不调用真实 OAuth 端点）
- 测试令牌交换的错误处理
- 测试 profile 到内部 User 类型的映射
```

---

## 上下文管理技巧

### 干净地开始会话

```bash
# 从之前的会话继续工作时，使用 /compact
# 这会总结之前的会话并释放上下文空间

# 在 Claude Code 交互模式中：
> /compact
# 然后继续你的任务
```

### 明确限制 AI 读取的内容

```bash
# 精确告诉 Claude 该看哪些文件
claude "只读取这些文件然后实现功能：
- src/auth/jwt.ts
- src/auth/types.ts
- src/auth/config.ts
除非我告诉你，不要读取其他文件。"
```

### 为专注任务管道传递特定文件

```bash
# 审查特定模块而不加载其他内容
cat src/auth/jwt.ts src/auth/session.ts | claude -p \
  "审查这些 auth 文件的安全问题。关注：
   - 令牌验证逻辑
   - 会话过期处理
   - 错误信息泄露"

# 只分析类型定义
find src -name "types.ts" -exec cat {} + | claude -p \
  "分析这些类型定义的不一致之处"

# 审查最近的变更
git diff HEAD~5 -- src/api/ | claude -p \
  "审查这些 API 变更是否有破坏性更改"
```

### 子代理模式

当任务跨越多个模块时，将其拆分为有作用域的子任务：

```bash
# 主任务：在整个平台添加审计日志

# 子任务 1：定义审计日志 schema（作用域限定在 shared）
claude --cwd packages/shared \
  "创建 AuditLog 类型和 createAuditEntry 工具函数。
   阅读 packages/shared/src/types.ts 了解现有模式。"

# 子任务 2：在 auth 中添加审计日志（作用域限定在 auth）
claude --cwd packages/auth \
  "为登录、登出和令牌刷新事件添加审计日志。
   从 @acme/shared 导入 createAuditEntry。
   阅读 src/jwt.ts 和 src/session.ts 确定在哪里添加调用。"

# 子任务 3：在 API 中添加审计日志（作用域限定在 api）
claude --cwd packages/api \
  "添加记录所有变更 API 调用的审计日志中间件。
   从 @acme/shared 导入 createAuditEntry。
   阅读 src/middleware/ 了解现有的中间件模式。"
```

### 使用参考文件减少上下文

不必让 Claude 读取 20 个文件，可以创建一个摘要文件：

```bash
# 为 AI 上下文生成参考文件
claude -p "阅读 packages/api/src/routes/ 并在
  docs/api-routes-summary.md 创建摘要文件，列出：
  - 每个路由的方法、路径和描述
  - 请求/响应类型
  - 认证要求
  控制在 200 行以内。"

# 之后使用摘要而不是读取所有路由文件
claude "阅读 docs/api-routes-summary.md。现在添加一个新路由
  POST /api/v1/audit-logs，遵循相同的模式。"
```

---

## 多会话工作流

对于大型功能，跨多个会话规划。通过文件在会话之间传递上下文。

### 会话 1：规划

```bash
claude "我需要为这个平台添加多租户支持。
阅读：
- CLAUDE.md（项目概览）
- packages/auth/CLAUDE.md
- packages/api/CLAUDE.md
- packages/shared/src/types.ts

在 docs/plans/multi-tenant.md 创建详细实施计划：
1. 需要的数据库 schema 变更
2. Auth 变更（租户作用域的令牌）
3. API 变更（租户中间件）
4. 迁移策略
5. 测试方法

分成 5-6 个独立的工作会话。"
```

### 会话 2：实现共享类型

```bash
claude "阅读 docs/plans/multi-tenant.md（会话 1 的计划）。
实现步骤 1：共享类型和数据库 schema。
在 packages/shared/ 和 packages/api/drizzle/ 中工作。
实现后，更新计划文件标记步骤 1 为已完成。"
```

### 会话 3：实现 Auth 变更

```bash
claude "阅读 docs/plans/multi-tenant.md（检查已完成的步骤）。
实现步骤 2：租户作用域令牌的 auth 变更。
在 packages/auth/ 中工作。
阅读 packages/shared/src/types.ts 了解步骤 1 中的新 Tenant 类型。
完成后更新计划文件。"
```

### 会话交接模式

```markdown
# docs/plans/multi-tenant.md（会话 2 之后）

## 实施计划

### 步骤 1：共享类型和 Schema [已完成]
- 在 packages/shared/src/types.ts 中创建了 Tenant 类型
- 添加了 tenants 表迁移：packages/api/drizzle/0005_add_tenants.sql
- 为 users 表添加了 tenant_id 列：packages/api/drizzle/0006_users_tenant.sql
- 修改的文件：packages/shared/src/types.ts, packages/api/src/db/schema.ts

### 步骤 2：Auth 变更 [进行中]
- 范围：packages/auth/
- 需要：在 JWT payload 中添加 tenantId，按租户作用域管理会话
- 参考：packages/shared/src/types.ts 中的新 Tenant 类型

### 步骤 3：API 中间件 [待办]
...
```

---

## Monorepo 策略

### 将 Claude Code 限定到单个包

```bash
# 使用 --cwd 限制 Claude Code 的工作范围
claude --cwd packages/auth "为登录端点添加限流"

# 这使 Claude Code 从该目录启动，
# 因此它读取本地 CLAUDE.md 并聚焦本地文件
```

### 按包执行命令

```bash
# 为特定包运行测试
claude --cwd packages/api "运行测试并修复所有失败"

# 对特定包进行代码检查
claude --cwd packages/web "运行 linter 并修复所有警告"
```

### 跨包类型引用

```markdown
# 在 packages/api/CLAUDE.md 中明确引用共享类型

## 共享类型
此包从 @acme/shared 导入类型：
- User, Tenant, Permission：定义在 packages/shared/src/types.ts
- ApiResponse<T>：定义在 packages/shared/src/api.ts
- Result<T, E>：定义在 packages/shared/src/result.ts

修改 API 端点时，检查类型变更是否影响 @acme/shared。
如果是，先更新共享类型，然后更新本包。
```

### 依赖图感知

```bash
# 帮助 Claude 理解包之间的关系
# 添加到根目录 CLAUDE.md：

## 包依赖关系
```
shared  <--  auth  <--  api  <--  web
                   <------------|
```

构建顺序：shared -> auth -> api -> web
如果修改 shared，所有包可能需要更新。
如果修改 auth，api 和 web 可能需要更新。
如果修改 api，只有 web 可能需要更新。
```

---

## AI 无法帮忙的场景

### 横切关注点

当一个变更涉及 50+ 个文件跨多个模块时，AI 会失去连贯性。

```bash
# 错误：要求 AI 一次完成横切变更
claude "在整个代码库中将 User 类型重命名为 Account"
# 结果：遗漏文件、不一致的重命名、破坏导入

# 正确：AI 规划，人工用 IDE 工具执行
claude "我需要在代码库中将 User 重命名为 Account。
创建一个计划，列出：
1. 所有引用 User 类型的文件
2. 所有需要重命名的数据库表/列
3. 所有 URL 中使用 'user' 的 API 端点
4. 按顺序的迁移步骤"

# 然后用 IDE 重构工具进行实际重命名
# （查找替换、TypeScript 重命名符号等）
```

### 深度遗留代码

```bash
# 当代码没有测试、没有文档，有复杂的隐式行为时

# 错误：要求 AI 重构未测试的遗留代码
claude "将 src/legacy/payment-processor.js 重构为 TypeScript"
# 结果：AI 可能改变它不理解的行为

# 正确：AI 先帮你理解，然后你来决定
claude "阅读 src/legacy/payment-processor.js。
列出每个副作用、每个外部调用和每个隐式行为。
然后建议在任何重构之前我应该编写哪些测试。"

# 编写测试（可以用 AI 辅助），然后在安全网下重构
```

### 性能调优

```bash
# AI 无法分析你的应用性能

# 错误：在没有数据的情况下要求 AI 优化
claude "让 API 更快"

# 正确：先做性能分析，然后要求 AI 优化具体瓶颈
# 1. 运行你的分析器（Node.js: clinic, Python: cProfile 等）
# 2. 识别慢函数
# 3. 给 AI 具体的函数和分析数据

claude "这个函数每次调用需要 800ms。分析器显示 90% 的时间
花在第 45 行的数据库查询上。查询返回 10K 行但我们只需要
前 10 行。优化这个。"
```

### AI 规划、人工执行模式

对于 AI 适合思考但不适合动手的任务：

```bash
# 步骤 1：AI 创建计划
claude "我们需要从 Express 迁移到 Fastify。
创建详细的迁移计划：
- 每个包需要改什么
- 变更顺序以避免破坏构建
- 如何在迁移期间同时运行两个框架
- 每个步骤的风险评估
保存到 docs/plans/express-to-fastify.md"

# 步骤 2：人工执行每个步骤，用 AI 辅助具体部分
# 开发者按照计划，对具体步骤请求 AI 帮助：
claude --cwd packages/api "将 src/middleware/auth.ts 从 Express
中间件转换为 Fastify 插件。这是 Express 版本：[粘贴代码]"
```

---

## 实战案例：重构 200K 行 Node.js 单体应用

将大型 Node.js 单体应用拆分为 AI 可管理的块的分步方法。

### 步骤 1：勘察地形

```bash
# 会话 1：了解结构（不要试图读取所有内容）
claude "这是一个 200K 行的 Node.js 单体应用。我需要了解它的结构。

运行这些命令并分析输出：
1. find src -type f -name '*.ts' | wc -l  （总文件数）
2. find src -maxdepth 1 -type d  （顶层目录）
3. cat package.json | jq '.dependencies | keys'  （依赖）
4. 找到入口点并追踪主初始化流程

在 docs/architecture.md 创建高层架构图"
```

### 步骤 2：创建 CLAUDE.md 层级

```bash
# 会话 2：基于架构图，创建 CLAUDE.md 文件
claude "阅读 docs/architecture.md。

为以下目录创建 CLAUDE.md 文件：
1. 根目录：项目概览、技术栈、如何运行
2. src/api/：API 路由和中间件
3. src/services/：业务逻辑层
4. src/models/：数据访问层
5. src/utils/：共享工具

每个文件只描述自己的领域。
每个控制在 50 行以内。"
```

### 步骤 3：识别提取边界

```bash
# 会话 3：找出可以提取为单独包的内容
claude "阅读 CLAUDE.md 文件和 docs/architecture.md。

分析模块之间的依赖图：
- 哪些模块紧密耦合？
- 哪些模块有清晰的边界？
- 哪些模块被所有地方使用（共享）？

在 docs/dependency-analysis.md 创建依赖报告
推荐先提取的 3-4 个包（从耦合度最低的开始）。"
```

### 步骤 4：每次提取一个包

```bash
# 会话 4+：每个会话提取一个模块
claude "阅读 docs/dependency-analysis.md。

我们正在将 src/utils/ 提取到 packages/shared/。
1. 创建包结构（package.json, tsconfig.json）
2. 将文件从 src/utils/ 移动到 packages/shared/src/
3. 更新单体应用中的所有导入使用 @acme/shared
4. 验证构建仍然正常

增量进行。每次文件移动后，检查导入错误。"
```

### 步骤 5：每个阶段验证

```bash
# 每次提取后，验证没有破坏
claude "运行完整的测试套件和构建。
如果有任何失败：
1. 显示错误
2. 解释什么坏了
3. 修复它
4. 重新运行确认"
```

### 步骤 6：记录新结构

```bash
# 所有提取完成后，更新文档
claude "阅读当前项目结构。
更新所有 CLAUDE.md 文件以反映新的 Monorepo 布局。
更新 docs/architecture.md 为当前状态。
在 docs/tech-debt.md 列出剩余的技术债务。"
```

### 大型代码库工作的关键原则

```
1. 永远不要一次加载所有内容
   - 每个会话限定在一个模块或包
   - 使用 CLAUDE.md 给 AI 地图而不是全部领土

2. 用文件作为会话记忆
   - 计划、架构文档和进度文件在会话间持久存在
   - 随着进展更新它们，让下一个会话有当前上下文

3. 将工作拆分为 AI 大小的块
   - 每个会话应有明确、有界的目标
   - 一个模块、一个功能、一个重构步骤

4. AI 绘制地图，人类导航
   - 让 AI 分析和规划
   - 让人类做架构决策
   - 让 AI 在有界范围内实现

5. 持续验证
   - 每次 AI 变更后运行测试
   - 每次提取后构建
   - 永远不要相信 AI 的"应该可以正常工作"
```

---

## 总结

在大型代码库中使用 AI 需要纪律：

1. **分层 CLAUDE.md 文件**：每个层级只描述自己的领域
2. **主动管理上下文**：管道传递特定文件、使用 --cwd、限制读取
3. **跨会话规划**：使用文件在会话间传递上下文
4. **按包限定范围**：在 Monorepo 中，一次处理一个包
5. **了解 AI 的局限**：横切变更、遗留代码和性能调优需要人工动手
6. **增量拆分单体应用**：勘察、规划、增量提取、持续验证
