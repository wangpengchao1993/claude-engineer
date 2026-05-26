# 调试 AI 生成的代码

> AI 写代码很快，但不总是正确的。学会识别常见的 AI 错误，高效修复它们，并建立预防机制。

## 目录

- [常见 AI 错误类型](#常见-ai-错误类型)
- [检测策略](#检测策略)
- [恢复策略](#恢复策略)
- [预防模式](#预防模式)
- [当 AI 卡住时](#当-ai-卡住时)
- [实战调试案例](#实战调试案例)

---

## 常见 AI 错误类型

### 1. 幻觉 API

AI 自信地使用了实际不存在的函数、模块或方法。

```typescript
// AI 写了这段代码 — 看起来合理，但 crypto.timingSafeCompare 不存在
import crypto from 'crypto';

function verifyToken(provided: string, expected: string): boolean {
  return crypto.timingSafeCompare(provided, expected);  // ❌ 不是真实函数
}

// 实际函数是 crypto.timingSafeEqual，而且需要 Buffer
import crypto from 'crypto';

function verifyToken(provided: string, expected: string): boolean {
  return crypto.timingSafeEqual(             // ✅ 正确的函数名
    Buffer.from(provided),                   // ✅ 需要 Buffer 转换
    Buffer.from(expected)
  );
}
```

**为什么会发生**：AI 在大量代码样本上训练，会混淆相似的 API。

**如何捕获**：TypeScript 编译器、IDE 悬停提示、`tsc --noEmit`、测试执行。

### 2. 过时语法

AI 使用了已弃用或已移除的旧版本写法。

```jsx
// AI 用旧式 React 类组件写了弃用的生命周期方法
class UserProfile extends React.Component {
  componentWillMount() {              // ❌ 自 React 16.3 起弃用
    this.fetchUser();
  }

  componentWillReceiveProps(next) {   // ❌ 自 React 16.3 起弃用
    if (next.userId !== this.props.userId) {
      this.fetchUser(next.userId);
    }
  }
}

// 现代写法
function UserProfile({ userId }: { userId: string }) {
  useEffect(() => {                   // ✅ 现代 Hook
    fetchUser(userId);
  }, [userId]);                       // ✅ 依赖数组处理变更
}
```

**为什么会发生**：训练数据包含各个时代的代码。旧模式出现频率更高。

**如何捕获**：Lint 规则（react-hooks/exhaustive-deps）、框架文档、弃用警告。

### 3. 逻辑错误

代码编译并运行，但产生错误的结果。

```python
# AI 写了一个分页函数
def get_page(items: list, page: int, per_page: int = 10) -> list:
    start = page * per_page         # ❌ 差一错误：第 1 页跳过了前面的项目
    end = start + per_page
    return items[start:end]

# 第 1 页返回第 10-19 项，而不是第 0-9 项！

# 正确版本
def get_page(items: list, page: int, per_page: int = 10) -> list:
    start = (page - 1) * per_page   # ✅ 第 1 页从索引 0 开始
    end = start + per_page
    return items[start:end]
```

**为什么会发生**：AI 生成看起来合理的代码，但没有在脑中"运行"它。差一错误、错误的比较运算符和反转条件很常见。

**如何捕获**：使用边界值的单元测试、手动跟踪执行、测试驱动开发。

### 4. 遗漏边界情况

AI 处理了正常路径，但忘记了 null、空输入、错误和边界情况。

```python
# AI 写了用户查找
def get_user_display_name(user_id: str, db: Database) -> str:
    user = db.find_user(user_id)
    return f"{user.first_name} {user.last_name}"  # ❌ 如果 user 是 None？
                                                    # ❌ 如果名字是 None？

# 健壮版本
def get_user_display_name(user_id: str, db: Database) -> str:
    user = db.find_user(user_id)
    if user is None:                               # ✅ 处理用户不存在
        return "未知用户"
    first = user.first_name or ""                   # ✅ 处理 None 名字
    last = user.last_name or ""
    name = f"{first} {last}".strip()
    return name if name else "未命名用户"            # ✅ 处理两者都为空
```

**常见遗漏的边界情况**：
```
- None/null/undefined 值
- 空字符串、空数组、空对象
- 零、负数
- 非常大的输入（内存、超时）
- Unicode 字符（名字中的 emoji、RTL 文本）
- 并发访问（竞态条件）
- 网络失败（超时、DNS、TLS 错误）
- 文件系统错误（权限、磁盘满、文件不存在）
```

### 5. 不一致的模式

AI 在同一文件或项目中混合不同的编码风格。

```typescript
// AI 在一个文件中生成了混合模式的代码
class UserService {
  // 模式 1：回调风格
  getUser(id: string, callback: (err: Error, user: User) => void) {
    db.find(id, callback);
  }

  // 模式 2：Promise 风格
  updateUser(id: string, data: Partial<User>): Promise<User> {
    return db.update(id, data);
  }

  // 模式 3：async/await 风格
  async deleteUser(id: string): Promise<void> {
    await db.delete(id);
  }
}

// 一致的版本 — 选择一种模式并坚持
class UserService {
  async getUser(id: string): Promise<User> {
    return await db.find(id);
  }

  async updateUser(id: string, data: Partial<User>): Promise<User> {
    return await db.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await db.delete(id);
  }
}
```

**如何捕获**：代码审查、ESLint 一致性规则、项目级 CLAUDE.md 风格指南。

### 6. 过度工程

AI 添加了不必要的抽象、模式或复杂性。

```typescript
// AI 被要求"添加一个日志记录器"，结果创建了一整个框架
interface LogStrategy { log(msg: string): void; }
class ConsoleLogStrategy implements LogStrategy { /* ... */ }
class FileLogStrategy implements LogStrategy { /* ... */ }
class LogStrategyFactory { /* ... */ }
class LoggerBuilder { /* ... */ }
class Logger {
  private strategy: LogStrategy;
  private static instance: Logger;
  // ... 又 200 行
}

// 实际需要的
import pino from 'pino';
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });
export default logger;
```

**为什么会发生**：AI 训练数据包含企业级模式、设计模式教程和教科书示例。它默认选择"全面"而非"简单"。

**如何预防**：明确说明 — "用简单方法"、"不超过 30 行"、"使用现有库"。

### 7. 依赖混淆

AI 导入了错误的包、错误的版本或不存在的包。

```python
# AI 写了这个导入
from sklearn.ensemble import GradientBoostedClassifier  # ❌ 类名错误

# 正确
from sklearn.ensemble import GradientBoostingClassifier  # ✅

# AI 建议了一个不存在的包（或恶意包）
pip install python-jwt        # ❌ 不是那个流行的
pip install PyJWT             # ✅ 广泛使用的 JWT 库

# AI 混淆了包版本
import { serve } from '@hono/node-server'    # 在 Hono v3+ 中工作
import { Hono } from 'hono'                  # 但 AI 写了 Hono v2 的模式
```

**如何捕获**：`pip install` / `npm install` 错误、运行时导入错误、lock 文件审查。

---

## 检测策略

### 类型检查

捕获幻觉 API 和错误签名的最快方法。

```bash
# TypeScript
npx tsc --noEmit
# 捕获：错误的方法名、错误的参数类型、缺失的属性

# Python
mypy src/ --strict
# 或
pyright src/

# Go
go vet ./...
```

**让 Claude 运行类型检查**：
```
"运行 tsc --noEmit 并修复你刚才更改的文件中的任何类型错误"
```

### 代码检查（Linting）

捕获弃用模式、风格违规和潜在 bug。

```bash
# JavaScript/TypeScript
npx eslint src/ --fix

# Python
ruff check src/ --fix
# 或
flake8 src/

# Go
golangci-lint run
```

**专业技巧**：在 CLAUDE.md 中添加 lint 检查：
```markdown
## 每次更改后
- 运行 `npm run lint` 检查问题
- 运行 `npm run typecheck` 验证类型
```

### 测试驱动开发（TDD）

先写测试，再让 AI 实现。测试能立即捕获 bug。

```bash
# 第 1 步：自己写测试（或先让 AI 写测试）
"为计算运费的函数编写测试。
 超过 $50 免运费，$50 以下固定 $5.99，不允许负价格。"

# 第 2 步：让 AI 实现
"现在实现 calculateShipping 函数使这些测试通过"

# 第 3 步：运行测试
npm test

# 如果测试失败，AI 看到失败信息可以修复
"测试失败了 — 修复实现"
```

### AI 自我审查

让 Claude 用新的视角审查自己的代码。

```bash
# AI 写完代码后
"现在审查你刚才写的代码。检查：
 - 缺失的错误处理
 - 未覆盖的边界情况
 - 安全问题
 - 性能问题
 列出每个问题及 文件:行号 和建议修复。"

# 或使用第二个 Claude 实例
cat src/auth/*.ts | claude "审查这段认证代码的安全问题"
```

### 静态分析

专门工具捕获安全和质量问题。

```bash
# 安全扫描
semgrep --config auto src/          # 多语言安全模式
bandit -r src/                       # Python 安全检查
npm audit                            # Node.js 依赖漏洞

# 代码质量
sonarqube-scanner                    # 全面质量分析

# 复杂度分析
npx complexity-report src/           # 圈复杂度
radon cc src/ -a                     # Python 复杂度
```

### 运行时测试

有些 bug 只在运行时出现。

```bash
# 集成测试
npm run test:integration

# 冒烟测试（访问真实端点）
curl -s http://localhost:3000/health | jq .

# 负载测试（发现性能问题）
k6 run load-test.js

# 手动测试
npm run dev
# 然后手动测试功能
```

---

## 恢复策略

### 查看变更

修复之前，先理解 AI 改了什么。

```bash
# 查看所有变更（已暂存和未暂存）
git diff

# 查看特定文件的变更
git diff src/auth/login.ts

# 查看哪些文件变了
git diff --name-only

# 与特定提交比较
git diff HEAD~3
```

### 回滚前先保存

```bash
# 暂存当前变更（可恢复）
git stash
# 之后：git stash pop（恢复）

# 创建备份分支
git checkout -b backup/ai-changes
git add -A && git commit -m "backup: 调试前备份 AI 变更"
git checkout main
```

### 回滚特定文件

```bash
# 将一个文件恢复到上次提交
git checkout HEAD -- src/auth/login.ts

# 恢复多个特定文件
git checkout HEAD -- src/auth/login.ts src/auth/middleware.ts

# 保留部分变更，回滚其他
git add src/auth/login.ts        # 暂存你想保留的文件
git checkout HEAD -- .            # 回滚其他所有内容
```

### Claude Code 内置撤销

```bash
# 让 Claude 撤销上一次更改
"撤销上一次更改"

# 撤销特定更改
"只回滚对认证模块的更改"

# 带说明的撤销
"撤销数据库迁移的更改 — 之前的 schema 是正确的"
```

### 会话重置

当对话上下文被错误假设污染时：

```bash
# 清除对话，重新开始
/clear

# 或带特定指令的压缩
/compact 忘掉我们尝试的认证方案，那是错的。保留数据库 schema 讨论。

# 开始全新会话
# 退出并重启 claude
```

### 选择性回滚

```bash
# 查看提交历史
git log --oneline -10

# 回滚特定提交（创建一个新的反向提交）
git revert abc1234

# 只挑选好的提交
git cherry-pick def5678 ghi9012

# 交互式：取消暂存特定块
git reset HEAD src/auth/login.ts    # 取消暂存文件
git add -p src/auth/login.ts        # 只暂存你想要的块
```

---

## 预防模式

### 1. 小任务（5 分钟为单位）

最有效的预防策略。小变更容易验证。

```bash
# 差：一个庞大的提示
"构建完整的认证系统，包括 JWT、刷新令牌、
 密码重置、邮箱验证、OAuth2 和速率限制"

# 好：连续的小任务
"创建 User 模型，包含 email、passwordHash 和 createdAt 字段"
# 验证 → 提交

"添加 POST /auth/register 端点，使用哈希密码创建用户"
# 验证 → 提交

"添加 POST /auth/login 端点，返回 JWT"
# 验证 → 提交

"添加 JWT 中间件，在受保护的路由上验证令牌"
# 验证 → 提交
```

**规则**：如果你不能在 5 分钟内验证输出，任务就太大了。

### 2. 规格先行

先写规格说明，再写代码。Superpowers/Spec-Kit 模式：

```bash
# 第 1 步：写规格
"为密码重置流程写一个技术规格。包括：
 - API 端点
 - 数据库变更
 - 邮件模板
 - 安全考虑
 - 边界情况
 保存到 specs/password-reset.md"

# 第 2 步：自己审查规格

# 第 3 步：按规格实现
"按照 specs/password-reset.md 实现密码重置流程。
 从数据库迁移开始。"
```

### 3. TDD（红-绿-重构）

```bash
# 红：写一个失败的测试
"为 PasswordResetService 编写测试。测试：
 - 生成重置令牌（应该是 URL 安全的，1 小时后过期）
 - 使用有效令牌（应该返回成功，使令牌失效）
 - 使用过期令牌（应该返回错误）
 - 使用令牌两次（第二次应该返回错误）
 不要写实现。"

# 绿：实现以通过测试
"现在实现 PasswordResetService 使所有测试通过"

# 重构：清理
"重构 PasswordResetService — 在不破坏测试的情况下简化"
```

### 4. 增量提交

每个验证过的任务后都提交。这创建了安全的回滚点。

```bash
# 每个小任务后：
git add src/models/user.ts
git commit -m "add User model with email and password fields"

# 如果下一个 AI 变更破坏了什么：
git diff                                # 查看变更
git checkout HEAD -- src/models/user.ts # 只回滚那个文件
```

**提交策略**：
```
任务 1：添加模型     → 验证 → 提交
任务 2：添加路由     → 验证 → 提交
任务 3：添加中间件   → 验证 → 提交
任务 4：添加测试     → 验证 → 提交

如果任务 3 出了问题，你可以回滚到任务 2 之后的状态。
```

### 5. 每一步都审查

不要等到最后才审查所有 AI 输出。

```bash
# 每次 AI 更改后：
# 1. 阅读差异
git diff

# 2. 问自己：
#    - 这有意义吗？
#    - 有明显的边界情况吗？
#    - 符合我们的模式吗？

# 3. 让 AI 自我审查
"审查你刚才做的更改。有什么问题吗？"

# 4. 运行测试
npm test

# 只有到这一步后：才进入下一个任务
```

---

## 当 AI 卡住时

### 提供更多上下文

当 AI 给出错误答案时，通常是缺少上下文。

```bash
# 差：没有上下文
"修复认证 bug"

# 好：完整上下文
"/api/login 端点在密码包含特殊字符的用户登录时返回 500。
 错误信息如下：

 TypeError: Cannot read property 'hash' of undefined
   at AuthService.login (src/services/auth.ts:45)

 第 45 行的 bcrypt.hash 调用收到 undefined，因为 password 字段
 在到达 service 之前被 URL 解码了。

 相关文件：
 - src/routes/auth.ts（路由处理器）
 - src/services/auth.ts（登录服务）
 - src/middleware/parser.ts（请求体解析中间件）"
```

### 切换模型

复杂问题有时需要更强的模型。

```bash
# 如果 Sonnet 搞不定
/model claude-opus-4-20250514

# 然后重新提供完整上下文
"我在调试 WebSocket 连接管理器中的竞态条件。
 当两个客户端同时使用相同的用户 ID 连接时..."
```

### 分解问题

```bash
# 而不是：
"修复认证系统"

# 分解它：
"首先，只解释当前认证流程做了什么。
 读取 src/auth/ 并逐步描述流程。"

# 然后：
"问题在第 3 步。令牌刷新发生在旧令牌失效之前。
 只修复 src/auth/refresh.ts 中的令牌失效时序。"
```

### 展示示例

```bash
# 而不是描述你想要什么：
"格式化 API 响应保持一致"

# 展示一个例子：
"将所有 API 响应格式化为如下示例：

 成功：{ status: 'ok', data: { ... }, meta: { timestamp: '...' } }
 错误：{ status: 'error', error: { code: 'NOT_FOUND', message: '...' } }

 应用到 src/routes/ 中的所有路由处理器"
```

### 重置上下文

```bash
# 当对话在兜圈子时
/compact

# 或完全重新开始
/clear

# 然后清晰地重新陈述问题
"重新开始。我需要修复 src/auth/refresh.ts 中的一个 bug。
 问题：注销后刷新令牌仍被接受。
 预期：POST /auth/logout 后，刷新令牌应该被拒绝。"
```

---

## 实战调试案例

### 场景：AI 生成了有问题的认证代码

你让 Claude "为 Express API 添加 JWT 认证"。代码编译通过，但登录总是返回 401。

#### 第 1 步：复现 Bug

```bash
# 启动开发服务器
npm run dev

# 尝试登录
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# 响应：{ "error": "Invalid credentials" }
# 但你知道这个用户存在于数据库中！
```

#### 第 2 步：阅读 AI 生成的代码

```bash
# 让 Claude 解释它写的代码
"读取 src/auth/login.ts 并逐步解释登录流程"
```

Claude 解释了流程。你注意到：

```typescript
// src/auth/login.ts — AI 生成的代码
async function login(email: string, password: string) {
  const user = await db.users.findOne({ email });
  if (!user) return null;

  // AI 用了 bcrypt.compare 但参数顺序错了
  const valid = await bcrypt.compare(user.passwordHash, password);
  //                                 ^^^^^^^^^^^^^^^^   ^^^^^^^^
  //                                 应该是：(password, user.passwordHash)
  return valid ? generateToken(user) : null;
}
```

#### 第 3 步：定位 Bug

```bash
"src/auth/login.ts 第 8 行的 bcrypt.compare 调用参数顺序错了。
 第一个参数应该是明文密码，第二个应该是哈希值。修复这个。"
```

#### 第 4 步：验证修复

```bash
# Claude 修复了代码。验证：
git diff src/auth/login.ts

# 你看到：
# -  const valid = await bcrypt.compare(user.passwordHash, password);
# +  const valid = await bcrypt.compare(password, user.passwordHash);

# 再次测试
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# 响应：{ "token": "eyJhbG..." }  ✅ 可以了！
```

#### 第 5 步：检查类似问题

```bash
"搜索整个认证模块中的其他 bcrypt 调用。
 确保它们的参数顺序都正确。"
```

#### 第 6 步：添加测试防止回归

```bash
"为 login 函数编写测试，覆盖：
 - 有效凭证返回令牌
 - 错误密码返回 null
 - 不存在的用户返回 null
 - email 字段中的 SQL 注入被安全处理"
```

#### 第 7 步：提交修复

```bash
git add src/auth/login.ts src/auth/__tests__/login.test.ts
git commit -m "fix: correct bcrypt.compare argument order in login"
```

#### 第 8 步：复盘

哪里出了问题，下次如何预防：

```
根本原因：AI 调换了 bcrypt.compare 的参数
检测方式：手动测试（本来可以更早发现）

下次的预防措施：
1. 在实现之前先写登录测试（TDD）
2. 让 AI 自我审查安全关键代码
3. 添加到 CLAUDE.md：
   "bcrypt.compare 参数为 (明文, 哈希) — 不是反过来"
4. 小任务：将"添加用户模型"和"添加登录"和"添加 JWT"分开
```

---

## 快速参考

### AI Bug 检测清单

```
每次 AI 代码生成后：
  □ 能编译吗？（tsc --noEmit, mypy, go vet）
  □ 通过 lint 了吗？（eslint, ruff, golangci-lint）
  □ 现有测试仍然通过吗？（npm test）
  □ 新代码有测试吗？
  □ 你读了 diff 吗？（git diff）
  □ 边界情况处理了吗？（null、空、错误、边界）
  □ 导入了正确的包/版本吗？
  □ 编码风格与项目一致吗？
```

### 各语言常见 AI 错误

```
TypeScript:
  - 在需要具体类型的地方用了 any
  - 缺少 null 检查（strictNullChecks）
  - 模块系统搞错（import vs require）
  - 忘记 await 异步函数

Python:
  - 缩进错误（混用 tab 和空格）
  - 可变默认参数（def foo(items=[])）
  - 不处理异常（裸 except:）
  - 字符串格式化搞混（% vs .format vs f-string）

Go:
  - 忽略错误返回值（_, _ = someFunc()）
  - Goroutine 泄漏（没有 context 取消）
  - 竞态条件（缺少 mutex）
  - 接口的 nil 检查不正确

React:
  - useEffect 缺少依赖数组
  - 过期闭包
  - 没有 memoize 昂贵计算
  - 直接修改 state
```

### 恢复命令速查表

```bash
# 查看变更
git diff                          # 所有变更
git diff --name-only              # 只显示变更的文件
git log --oneline -5              # 最近的提交

# 保存当前状态
git stash                         # 暂存变更
git stash pop                     # 恢复暂存的变更

# 回滚变更
git checkout HEAD -- <file>       # 回滚一个文件
git checkout HEAD -- .            # 回滚所有文件
git revert <commit>               # 反向提交（安全）

# Claude Code
"撤销上一次更改"                   # 撤销 AI 的上次编辑
"回滚认证模块的更改"              # 选择性撤销
/clear                            # 重置对话
/compact                          # 压缩上下文
```

---

## 总结

```
最常见的 AI bug：
  1. 幻觉 API（错误的函数名）
  2. 过时语法（弃用的模式）
  3. 逻辑错误（差一、比较错误）
  4. 遗漏边界情况（null、空、错误）

最佳检测工具：
  1. 类型检查器（tsc, mypy）— 捕获幻觉 API
  2. 测试（特别是 TDD）— 捕获逻辑错误
  3. 代码审查（读 diff！）— 捕获其他所有问题

最佳预防：
  1. 小任务（5 分钟为单位，每个都验证）
  2. TDD（先写测试）
  3. 增量提交（安全回滚点）
  4. 清晰的提示（具体上下文，不要模糊请求）

卡住时：
  1. 更多上下文（错误信息、文件路径）
  2. 更强模型（升级到 Opus）
  3. 更小的问题（分解它）
  4. 重新开始（/clear, /compact）
```

> 上一篇：[成本优化与模型选择](13-cost-and-model-selection.md)

---

## AI 产出质量退化检测

AI 不是一成不变的——模型更新、prompt 变化、项目演进都可能导致 AI 输出质量下降。

### 建立基线

首次大规模使用 AI 时，记录以下基线指标：
- 首次 CI 通过率（AI 生成的代码 push 后 CI 一次通过的比例）
- Review 修改率（AI 代码在 review 中被修改的比例）
- 上线后 bug 率（AI 代码上线 7 天内发现的 bug 数量）

### 持续监控

按周/月统计这些指标。如果趋势恶化：
1. **检查 CLAUDE.md** — 最近有没有改动导致上下文质量下降
2. **检查模型版本** — 是否有自动升级影响了输出
3. **检查项目变化** — 代码库变大后，AI 可能需要更精确的上下文引导

## AI 代码事故响应

当 AI 生成的代码导致生产事故时：

### 追溯流程

1. **定位问题代码** — `git blame` 找到引入变更的 commit
2. **确认 AI 参与** — 检查 commit message 是否有 `Co-Authored-By: Claude` 或 AI 标记
3. **回溯会话** — 如果有日志，找到当时的 prompt 和 AI 的推理过程
4. **根因分析** — 是 prompt 不够精确？是 CLAUDE.md 缺少约束？还是 AI 的固有局限？

### 复盘模板

```markdown
## AI 代码事故复盘

### 事故概述
- 时间/影响范围/持续时长

### 根因
- AI 生成了什么有问题的代码
- 为什么 AI 会生成这样的代码（prompt/上下文/模型局限）
- 为什么 review 没有发现

### 改进措施
- CLAUDE.md 补充什么约束
- CI 增加什么检查
- Review 流程如何调整
```

---

[← 上一章：成本与模型选择](13-cost-and-model-selection.md) | [目录](../../README_zh.md) | [下一章：团队协作 →](15-team-workflows.md)
