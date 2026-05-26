# Claude Code 精通

> 掌握 Claude Code CLI 的每一个功能 — 用 Claude 做软件工程最强大的方式。

## 目录

- [什么是 Claude Code？](#什么是-claude-code)
- [安装](#安装)
- [核心概念](#核心概念)
- [交互模式](#交互模式)
- [非交互模式](#非交互模式)
- [上下文管理](#上下文管理)
- [权限系统](#权限系统)
- [Plan 模式](#plan-模式)
- [子 Agent](#子-agent)
- [使用 Git](#使用-git)
- [使用测试](#使用测试)
- [IDE 集成](#ide-集成)
- [高级技巧](#高级技巧)

---

## 什么是 Claude Code？

Claude Code 是 Anthropic 官方的 CLI 工具，将 Claude 变成 AI 驱动的软件工程助手。它可以：

- 读取、写入和编辑项目中的文件
- 运行 Shell 命令
- 搜索代码库
- 管理 Git 操作
- 通过 MCP 服务器扩展能力
- 启动并行子 Agent 处理复杂任务

支持 CLI、桌面应用（Mac/Windows）、Web 应用（claude.ai/code）和 IDE 扩展（VS Code、JetBrains）。

---

## 安装

```bash
# 通过 npm 安装（推荐）
npm install -g @anthropic-ai/claude-code

# 设置 API 密钥
export ANTHROPIC_API_KEY=sk-ant-...

# 验证安装
claude --version

# 开始使用
claude
```

### 首次运行

首次启动时，Claude Code 会：
1. 检测项目结构
2. 读取现有的 `CLAUDE.md` 文件
3. 启动交互式会话

**建议**：立即运行 `/init` 为项目生成 `CLAUDE.md`，这会大幅提升 Claude 对代码库的理解。

---

## 核心概念

### Claude Code 的思维方式

Claude Code 采用**基于工具的架构**：

1. 你提供提示（任务、问题或指令）
2. Claude 分析任务并决定使用哪些工具
3. 执行工具（读文件、搜索、编辑、运行命令）
4. 循环直到任务完成
5. 向你报告结果

### 可用工具

| 工具 | 功能 |
|------|------|
| **Read** | 读取文件内容 |
| **Write** | 创建新文件 |
| **Edit** | 精确编辑现有文件 |
| **Glob** | 按模式查找文件 |
| **Grep** | 搜索文件内容 |
| **Bash** | 执行 Shell 命令 |
| **Agent** | 启动子 Agent 并行工作 |

加上你配置的 MCP 服务器提供的工具。

---

## 交互模式

默认模式 — 与 Claude 对话：

```bash
claude
```

### 有效的交互式提示

**具体说明你想要什么：**

```
差：  "修复 bug"
好：  "登录端点在邮箱包含 '+' 时返回 500 — 修复 src/auth/validator.ts 中的验证逻辑"
```

**需要时提供上下文：**

```
"我正在开发用户设置页面。React 组件在
src/components/Settings.tsx，API 处理器在 src/api/settings.ts。
添加一个'修改密码'功能，要有正确的验证。"
```

**使用渐进式指令：**

将复杂任务拆分为步骤：
1. "首先，读取当前的认证实现并解释它是如何工作的"
2. "现在按照相同的模式添加 OAuth2 支持"
3. "为新的 OAuth2 流程编写测试"

### 对话管理

```bash
# 恢复上次对话
claude -c

# 上下文变大时使用 /compact
/compact

# 清除并重新开始
/clear

# 检查 Token 使用量
/cost
```

---

## 非交互模式

适合脚本、CI/CD 和自动化：

```bash
# 使用 print 模式的简单查询
claude -p "这个项目是做什么的？"

# 管道输入进行分析
cat error.log | claude -p "总结这些错误"
git diff --staged | claude -p "审查这些变更"

# JSON 输出用于程序化使用
claude -p "列出所有 API 端点" --output-format json

# 限制 Agent 轮次以获得可预测的执行
claude -p "运行测试" --max-turns 5

# 链式命令
git diff HEAD~1 | claude -p "写一个 commit message" | git commit -F -
```

### 非交互模式的使用场景

- **CI/CD**：PR 的自动化代码审查
- **Git hooks**：提交前验证
- **脚本**：批量处理文件
- **流水线**：大型自动化工作流的一部分

---

## 上下文管理

### 上下文如何工作

Claude Code 有上下文窗口（Opus 4.6 最高 1M tokens）。随着对话增长，上下文会被填满。管理好上下文是高效使用的关键。

### CLAUDE.md — 持久化上下文

最重要的上下文机制。Claude 自动读取：

1. 项目根目录的 `CLAUDE.md`（通过 git 与团队共享）
2. 子目录中的 `CLAUDE.md`（目录级上下文）
3. `~/.claude/CLAUDE.md`（个人全局配置）

**CLAUDE.md 中应该放什么：**
- 项目概述和技术栈
- 常用命令（构建、测试、lint）
- 代码规范和模式
- 需要避免的事项
- 架构概述

详见 [CLAUDE.md 指南](03-claude-md-guide.md)。

### 上下文压缩

上下文窗口满时，使用 `/compact` 压缩对话并保留关键信息。Claude 会：
1. 总结到目前为止的对话
2. 保留重要的代码片段和决策
3. 释放上下文用于新工作

**技巧**：使用带有总结提示的 `/compact` 来保留特定信息：
```
/compact 聚焦在我们讨论的认证变更上
```

---

## 权限系统

Claude Code 在可能有破坏性的操作前会请求权限。有三种权限模式：

| 模式 | 行为 |
|------|------|
| **Default** | 写入和命令前询问 |
| **Plan** | 计划批准前只读 |
| **Bypass** | 不提示权限（谨慎使用） |

### 配置权限

在 `.claude/settings.json` 中：

```jsonc
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

**最佳实践**：从默认权限开始，为频繁使用的命令（如测试和 lint）添加 `allow` 规则。

---

## Plan 模式

Plan 模式让 Claude 先思考再行动。用 **Shift+Tab** 切换。

### 何时使用 Plan 模式

- 跨多个文件的复杂重构
- 架构决策
- 你想先审查方案的任务
- 不确定最佳解决方案时

### 工作流程

1. **开启**：按 `Shift+Tab`
2. **Claude 规划**：读取代码，分析任务，提出方案
3. **你审查**：批准、修改或重新引导
4. **关闭**：按 `Shift+Tab` 让 Claude 执行
5. **Claude 实现**：按照批准的方案执行

### Plan 模式技巧

- 对复杂任务的首次迭代使用它
- 让 Claude 考虑替代方案："提出 2-3 种不同的方案"
- 方案确定后，退出 Plan 模式并说"执行方案"

---

## 子 Agent

Claude 可以启动并行子 Agent 处理复杂任务，相当于多个 Claude 实例同时工作。

### 子 Agent 类型

| 类型 | 用途 | 使用场景 |
|------|------|----------|
| **Explore** | 快速代码库搜索和分析 | "查找所有使用了废弃 API 的地方" |
| **Plan** | 设计实现方案 | "规划数据库迁移" |
| **General** | 多步骤复杂任务 | "在 20 个文件中重构认证" |

### 你不需要做什么特别的事

Claude 自动决定何时使用子 Agent。但你可以引导它：

```
"同时检查三个服务（认证、支付、通知）的错误处理是否正确"
```

Claude 可能会启动多个搜索 Agent 并行覆盖不同区域。

---

## 使用 Git

Claude Code 擅长 Git 操作：

```
"审查最近 3 次提交并总结变更"
"为暂存的修改写一个 commit message"
"为这个分支上的所有变更创建一个 PR"
"解决 src/api.ts 中的合并冲突"
```

### Commit 消息

Claude 会遵循仓库的规范。为了最佳效果，在 `CLAUDE.md` 中包含几个示例：

```markdown
## Git 规范
- 使用约定式提交：feat(scope): 描述
- 标题行不超过 72 个字符
- 非琐碎变更需要包含正文
```

---

## 使用测试

```
# 运行并修复测试
"运行测试并修复所有失败"

# 为现有代码写测试
"为 UserService 类写测试"

# 测试驱动开发
"为 [功能] 写一个会失败的测试，然后实现功能"
```

**技巧**：在 `CLAUDE.md` 中包含测试命令：

```markdown
## 测试
- `npm test` — 运行所有测试
- `npm test -- --watch` — 监视模式
- `npm test -- path/to/file` — 运行特定文件
```

---

## IDE 集成

### VS Code

安装 Claude Code 扩展：
- 内联与 Claude 对话
- 高亮代码并提问
- 终端集成

### JetBrains

适用于 IntelliJ、PyCharm、WebStorm 等 JetBrains IDE。

---

## 高级技巧

### 1. 使用适当的自主级别

- **探索性任务**：让 Claude 自由运行
- **关键变更**：先用 Plan 模式
- **生产代码**：审查每一个变更

### 2. 给 Claude 足够的上下文

- 保持 `CLAUDE.md` 更新
- 在提示中引用具体文件
- 解释请求背后的"为什么"

### 3. 迭代而不是过度指定

不要写 500 字的提示，先简单开始再迭代：
1. "给 API 添加一个缓存层"
2. [审查 Claude 的方案]
3. "改用 Redis 而不是内存缓存"

### 4. 让 Claude 处理枯燥的部分

Claude 擅长：
- 模板代码生成
- 编写测试
- 跨多文件重构
- 文档撰写
- 迁移脚本
- 配置文件

### 5. 用管道处理快速任务

```bash
# 快速代码审查
git diff | claude -p "有什么问题吗？"

# 生成文档
cat src/api.ts | claude -p "生成 markdown 格式的 API 文档"

# 格式转换
cat data.csv | claude -p "转换为 JSON"

# 解释错误
npm test 2>&1 | claude -p "解释为什么这些测试失败了"
```

### 6. 自定义系统提示用于脚本

```bash
claude -p "审查安全问题" \
  --system-prompt "你是安全审计员。只关注 OWASP Top 10 漏洞。" \
  < src/auth.ts
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| "上下文窗口已满" | 使用 `/compact` 压缩 |
| Claude 做出错误假设 | 改善你的 `CLAUDE.md` |
| 响应慢 | 试试 `/fast` 模式或较小的模型 |
| 权限被拒绝 | 检查 `.claude/settings.json` 权限配置 |
| MCP 服务器无法连接 | 运行 `claude mcp list` 验证配置 |

---

<p align="center">
  <strong>下一篇：</strong> <a href="03-claude-md-guide.md">CLAUDE.md 指南</a> — 掌握项目级配置
</p>

---

[← 上一章：Claude 入门](01-getting-started.md) | [目录](../../README_zh.md) | [下一章：CLAUDE.md 指南 →](03-claude-md-guide.md)
