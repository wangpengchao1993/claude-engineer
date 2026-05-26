# 团队 AI 协作工作流

> 将 AI 融入团队开发流程的实用工作流：角色分配、PR 生命周期、共享配置、新人入职、代码责任归属与知识共享。

## 目录

- [团队中的 AI 角色](#团队中的-ai-角色)
- [AI 参与的 PR 工作流](#ai-参与的-pr-工作流)
- [共享 CLAUDE.md 管理](#共享-claudemd-管理)
- [新开发者入职](#新开发者入职)
- [代码责任与审查](#代码责任与审查)
- [知识共享](#知识共享)
- [应避免的反模式](#应避免的反模式)

---

## 团队中的 AI 角色

AI 在团队工作流中扮演三种不同角色。为每种场景选择正确的角色是高效协作的关键。

### AI 作为编写者

开发者描述任务，Claude Code 编写实现。

```bash
# 开发者提供意图，AI 编写代码
claude "创建一个 Express 限流中间件：
- 使用滑动窗口算法
- 在 Redis 中存储状态
- 返回 429 状态码和 Retry-After 头
- 支持按路由配置"
```

适用场景：模板代码、规格明确的功能、CRUD 操作、测试生成。

### AI 作为审查者

开发者编写代码，Claude Code 在 PR 之前审查。

```bash
# 提交前审查暂存的变更
git diff --staged | claude "审查这个 diff，关注：
- 安全问题
- 性能问题
- 遗漏的边界情况
- 违反 CLAUDE.md 中约定的地方"
```

适用场景：发现 bug、执行标准、安全审查、文档缺口。

### AI 作为结对编程伙伴

开发者与 AI 交互协作，在人工决策和 AI 执行之间交替。

```bash
# 交互式会话，开发者引导方向
claude
> 我们来重构支付模块。先给我看看当前结构。
> 好，我想把 Stripe 逻辑提取到单独的适配器中。先从接口开始。
> 不错。现在实现适配器。保留旧代码中的错误映射。
> 为我们讨论的错误场景添加测试。
```

适用场景：复杂重构、架构决策、探索性工作、学习新代码库。

### 角色选择矩阵

| 场景 | AI 角色 | 人工角色 |
|------|---------|----------|
| 新 CRUD 端点 | 编写者 | 审查输出 |
| 安全敏感代码 | 审查者 | 编写代码 |
| 复杂重构 | 结对编程 | 引导决策 |
| Bug 调查 | 结对编程 | 确认诊断 |
| 编写测试 | 编写者 | 验证覆盖率 |
| 性能优化 | 审查者 | 性能分析和实现 |

---

## AI 参与的 PR 工作流

### 完整的 PR 生命周期

推荐的流程在多个阶段集成 AI，同时不移除人工判断。

```
开发者                    Claude Code              GitHub                  团队
    |                         |                       |                     |
    |--- 描述任务 ----------->|                       |                     |
    |<-- 实现 + 测试 ---------|                       |                     |
    |--- 本地审查 ----------->|                       |                     |
    |<-- 修复问题 ------------|                       |                     |
    |                         |                       |                     |
    |--- git push ------------|---------------------> |                     |
    |                         |                       |--- CI 运行 -------->|
    |                         |<-- 自动审查 (GH Action) ---|                |
    |                         |--- 发布评论 ---------->|                     |
    |                         |                       |--- 通知团队 -------->|
    |                         |                       |                     |
    |                         |                       |<-- 人工审查 ---------|
    |                         |                       |    （同时审查 AI     |
    |                         |                       |     的审查意见）     |
    |                         |                       |                     |
    |<-- 处理反馈 ------------|                       |<-- 批准/请求修改 ---|
    |--- 推送修复 ----------->|---------------------> |                     |
    |                         |                       |<-- 合并 ----------- |
```

### AI 审查的 GitHub Action

```yaml
# .github/workflows/ai-review.yml
name: AI 代码审查
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 获取差异
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > /tmp/pr-diff.txt

      - name: 运行 Claude Code 审查
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cat /tmp/pr-diff.txt | claude -p \
            "审查这个 PR diff。关注：
             1. Bug 和逻辑错误
             2. 安全漏洞
             3. 性能问题
             4. 缺失的测试
             以 GitHub PR 审查评论格式输出。" \
            > /tmp/review.md

      - name: 发布审查评论
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('/tmp/review.md', 'utf8');
            await github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: review,
              event: 'COMMENT'
            });
```

### 人工审查 AI 的审查

审查 AI 生成的审查意见时，检查以下几点：

```markdown
## AI 审查检查清单（供人工审查者使用）

- [ ] AI 的审查是否识别了真实问题（不是误报）？
- [ ] AI 的建议是否确实优于原始代码？
- [ ] AI 是否遗漏了明显的问题？
- [ ] AI 的评论是否可操作（不是模糊的）？
- [ ] AI 是否理解了业务上下文？
```

---

## 共享 CLAUDE.md 管理

### 三层配置架构

团队需要共享约定（提交到仓库）和个人偏好（gitignore 排除）。使用分层方法。

```
项目根目录/
  CLAUDE.md                          # 团队级别（提交到仓库）
  packages/
    auth/
      CLAUDE.md                      # 模块级别（提交到仓库）
    api/
      CLAUDE.md                      # 模块级别（提交到仓库）
  .claude/
    settings.json                    # 共享工具权限（提交到仓库）
    settings.local.json              # 个人偏好（gitignore 排除）
```

### 根目录 CLAUDE.md：团队约定

```markdown
# 项目：Acme 平台

## 技术栈
- TypeScript 5.x, Node.js 20 LTS
- React 18 + Next.js 14 (App Router)
- PostgreSQL 16 + Drizzle ORM
- Redis 用于缓存和限流

## 编码约定
- 使用命名导出，禁止默认导出
- 所有函数必须有 JSDoc，包含 @param 和 @returns
- 错误处理：使用 Result<T, E> 模式，库代码中禁止 throw
- 数据库查询：始终通过 Drizzle 使用参数化查询
- API 响应：始终使用 src/lib/api 中的 ApiResponse<T> 包装器

## 测试
- 单元测试：Vitest，以 *.test.ts 形式放在同级目录
- 集成测试：放在 __tests__/ 目录中
- 新代码最低 80% 分支覆盖率

## Git
- 约定式提交：feat|fix|chore|docs(scope): 消息
- PR 标题遵循提交约定
- Squash 合并到 main
```

### 模块级 CLAUDE.md

```markdown
# packages/auth/CLAUDE.md

## 用途
认证和授权模块。处理 JWT 令牌、会话管理、OAuth 提供商和 RBAC。

## 关键文件
- src/jwt.ts：令牌创建和验证
- src/providers/：OAuth 提供商适配器（Google、GitHub）
- src/rbac.ts：基于角色的访问控制中间件
- src/session.ts：会话存储（Redis 后端）

## 本模块特定约定
- 所有令牌过期值来自配置，禁止硬编码
- OAuth 密钥仅从环境变量加载
- RBAC 权限仅在 src/permissions.ts 中定义
- 始终使用 AuthError 类处理认证相关错误
```

### 个人设置（gitignore 排除）

```jsonc
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(docker compose *)"
    ]
  }
}
```

### 保持配置同步

```bash
# 添加到 CI 流水线：验证 CLAUDE.md 一致性
# scripts/validate-claude-md.sh

#!/bin/bash
set -e

# 检查根目录 CLAUDE.md 是否存在
if [ ! -f "CLAUDE.md" ]; then
  echo "错误：缺少根目录 CLAUDE.md"
  exit 1
fi

# 检查所有包是否有 CLAUDE.md
for pkg in packages/*/; do
  if [ ! -f "${pkg}CLAUDE.md" ]; then
    echo "警告：${pkg} 缺少 CLAUDE.md"
  fi
done

# 检查常见问题
if grep -r "API_KEY\|SECRET\|PASSWORD" CLAUDE.md packages/*/CLAUDE.md 2>/dev/null; then
  echo "错误：CLAUDE.md 文件中发现潜在密钥"
  exit 1
fi

echo "CLAUDE.md 验证通过"
```

---

## 新开发者入职

### 第一天：了解代码库

```bash
# 新开发者要做的第一件事
claude "向我解释这个代码库。涵盖：
1. 这个项目做什么？
2. 它的结构如何？
3. 主要入口点在哪里？
4. 如何在本地运行？
5. 测试在哪里？"
```

### 第一天：了解约定

```bash
# 指向 CLAUDE.md
claude "阅读仓库中的 CLAUDE.md 文件并总结：
1. 团队遵循哪些编码约定？
2. 预期的测试模式是什么？
3. 提到了哪些常见陷阱？"
```

### 第一周：引导式任务

```bash
# 在 AI 指导下修复小 bug
claude "我是这个代码库的新人。帮我修复 issue #234。
引导我完成：
1. bug 可能在哪里
2. 如何重现
3. 修复方案
4. 需要添加哪些测试"
```

```bash
# 在 AI 结对下完成第一个功能
claude "我需要给 API 添加一个 /health 端点。
先给我看看代码库中类似的端点，
然后帮我遵循相同的模式。"
```

### 入职检查清单模板

```markdown
## 使用 Claude Code 的新开发者入职清单

### 环境搭建（第 1 天）
- [ ] 克隆仓库并安装依赖
- [ ] 运行 `claude "解释这个代码库"` 获取概览
- [ ] 阅读根目录 CLAUDE.md 了解团队约定
- [ ] 设置个人 .claude/settings.local.json
- [ ] 运行测试套件 `claude "运行所有测试并解释失败原因"`

### 初始任务（第 1 周）
- [ ] 使用 Claude Code 作为结对编程伙伴修复小 bug
- [ ] 为测试不足的模块添加测试
- [ ] 按照现有模式创建小功能

### 融入团队（第 2 周）
- [ ] 使用团队检查清单审查一个 AI 生成的 PR
- [ ] 在 Claude Code 辅助下创建你的第一个 PR
- [ ] 为你负责的代码添加模块级 CLAUDE.md
```

---

## 代码责任与审查

### 谁对 AI 编写的代码负责？

触发 AI 的开发者负责。始终如此。

```
规则：谁提示的，谁负责。

- 你在提交前审查它
- 你确保它通过测试
- 你在后续负责维护
- 你在代码审查中回答相关问题
```

### AI 生成 PR 的审查检查清单

AI 生成的代码与人工代码有不同的失败模式。使用此检查清单。

```markdown
## AI 生成 PR 审查检查清单

### 正确性
- [ ] 是否真正解决了所述问题？
- [ ] 是否处理了边界情况（null、空值、边界值）？
- [ ] 是否与现有代码正确集成？
- [ ] 错误消息是否有帮助（不是通用的）？

### 模式
- [ ] 是否遵循项目已有的模式？
- [ ] 是否有不必要的抽象（AI 喜欢过度设计）？
- [ ] 是否使用项目现有的工具函数（而非重新实现）？
- [ ] 导入是否来自正确的内部包？

### 安全
- [ ] 没有硬编码的密钥或凭证
- [ ] 存在输入验证
- [ ] SQL 查询已参数化
- [ ] 认证检查已到位

### 测试
- [ ] 测试覆盖了实际行为（不只是正常路径）
- [ ] 测试断言有意义（不只是"不抛异常"）
- [ ] Mock 是真实的（不是过度简化的）
- [ ] 存在边界情况测试

### AI 特有问题
- [ ] 没有虚构的 API 或不存在的方法
- [ ] 没有来自训练数据的过时模式
- [ ] 没有解释显而易见代码的多余注释
- [ ] 没有应该实现但留为 "TODO" 的占位项
```

### 何时拒绝 AI 代码

在以下情况应拒绝并重写：

```
1. AI 虚构了依赖中不存在的 API
2. 方法根本不对（代码正确但方案错误）
3. 重新实现了代码库中已有的功能
4. 安全关键代码需要逐行人工编写
5. 代码正确但不可维护（过于巧妙）
6. 测试 Mock 不反映真实行为
```

---

## 知识共享

### 将会话用作文档

```bash
# 在复杂的调试会话后，捕获发现
claude "总结我们这次会话做了什么：
- bug 是什么？
- 根本原因是什么？
- 修复方案是什么？
- 未来应该注意什么？
写成事后分析文档。"
```

### 记录架构决策

```bash
# 使用 Claude Code 创建 ADR（架构决策记录）
claude "我们刚决定将内部 API 从 REST 切换到 GraphQL。
创建一个 ADR 文档，包含：
- 背景：为什么考虑这个
- 决策：我们选择了什么
- 后果：什么会改变
- 迁移计划：如何实施
按照 docs/adr/ 中的 ADR 模板。"
```

### AI 效果团队回顾

每月跟踪以下指标：

```markdown
## AI 效果回顾模板

### 指标
- AI 辅助创建的 PR 数量：___
- 需要大量人工返工的 PR 数量：___
- AI PR 与人工 PR 的平均审查轮次：___
- 预估节省时间（小时/周/开发者）：___

### 有效的方面
- AI 节省最多时间的任务类型
- 值得分享的提示词或工作流

### 无效的方面
- AI 适得其反的任务类型
- 本月常见的失败模式

### 行动项
- 更新 CLAUDE.md 加入新约定
- 在团队 wiki 分享有效的提示词
- 调整特定任务类型的 AI 角色选择
```

---

## 应避免的反模式

### 1. 盲目信任 AI 输出

```bash
# 错误：不审查就接受所有内容
claude "实现支付流程" && git add -A && git commit -m "feat: payments"

# 正确：提交前审查
claude "实现支付流程"
# 开发者逐行阅读生成的代码
# 开发者手动运行测试
# 开发者在理解代码后才提交
git add -A && git commit -m "feat: 添加基于 Stripe 的支付流程"
```

### 2. AI 成为拐杖

```
团队过度依赖 AI 的迹象：
- 开发者无法解释自己提交的代码
- 没人在合并前阅读 AI 输出
- "Claude 写的"在代码审查中成为可接受的回答
- 测试覆盖率很高但测试抓不到真正的 bug
- 新开发者跳过学习代码库（"直接问 Claude"）
```

### 3. 不审查 AI 输出

```bash
# "氛围编程"陷阱——不理解就上线
# 这会导致：
# - 生产环境中的安全漏洞
# - 测试抓不到的隐微 bug
# - 没人理解的技术债务
# - 没人能调试的线上事故

# 解决方案：建立团队规则
# "如果你无法向审查者解释每一行代码，你就不能合并。"
```

### 4. 团队中 AI 使用方式不一致

```
问题：每个开发者使用 AI 的方式不同，导致代码风格不一致。

解决方案：通过 CLAUDE.md 标准化
- 所有人使用相同的约定
- 相同的审查检查清单
- 常见任务使用相同的提示模式
- 定期团队同步，改进 AI 工作流
```

### 5. 因为"AI 生成的"就跳过测试验证

```bash
# 错误：信任 AI 测试而不验证
claude "为用户服务添加测试"
# 不检查测试是否真的测了什么就合并

# 正确：验证测试质量
claude "为用户服务添加测试"
# 手动审查：断言是否检查了真实行为？
# 变异测试：代码被破坏时测试是否会失败？
# 覆盖率：边界情况是否真的被覆盖？
```

### 6. 所有事情都用 AI

```
不是每个任务都适合用 AI。知道什么时候该自己动手：

- 一行修复：打字比描述更快
- 命名：人类更擅长领域特定命名
- UX 决策：AI 不了解你的用户
- 架构：AI 可以提议，但人必须决定
- 代码审查文化：AI 是补充而非替代人工审查
```

---

## 总结

高效的团队 AI 协作需要：

1. **角色明确**：知道何时让 AI 编写、审查或结对
2. **结构化 PR 流程**：AI 在多个阶段辅助，人工始终做决定
3. **共享配置**：分层 CLAUDE.md 保持团队一致
4. **用心的入职流程**：AI 加速学习但不能替代学习
5. **责任文化**：提示者负责代码
6. **持续改进**：跟踪和回顾 AI 效果
7. **健康的怀疑态度**：审查一切，不盲目信任

---

[← 上一章：调试 AI 代码](14-debugging-ai-code.md) | [目录](../../README_zh.md) | [下一章：安全合规 →](16-security-compliance.md)
