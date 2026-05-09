# Claude 入门指南

> 从零开始 — 安装 Claude Code，配置环境，完成你的第一个实际任务。

## 目录

- [前置条件](#前置条件)
- [安装](#安装)
- [身份验证](#身份验证)
- [你的第一次会话](#你的第一次会话)
- [理解 Claude Code 的工作方式](#理解-claude-code-的工作方式)
- [你的第一个真实任务](#你的第一个真实任务)
- [基础配置](#基础配置)
- [下一步学什么](#下一步学什么)

---

## 前置条件

安装 Claude Code 之前，确保你有：

- **Node.js 18+** — [下载](https://nodejs.org/)
- **Anthropic API 密钥** — [获取](https://console.anthropic.com/)
- **终端** — 任何现代终端（iTerm2、Windows Terminal 等）
- **Git**（推荐）— Claude Code 在 git 仓库中效果最佳

### 平台支持

| 平台 | 状态 |
|------|------|
| macOS | 完全支持（CLI + 桌面应用） |
| Linux | 完全支持（CLI） |
| Windows | 通过 WSL2 支持（CLI）+ 桌面应用 |

---

## 安装

### 方式 1：npm（推荐）

```bash
npm install -g @anthropic-ai/claude-code
```

### 方式 2：桌面应用

从 [claude.ai/code](https://claude.ai/code) 下载 Mac 或 Windows 版本。

### 方式 3：IDE 扩展

- **VS Code**：在扩展商店搜索 "Claude Code"
- **JetBrains**：在插件商店搜索 "Claude Code"

### 验证安装

```bash
claude --version
```

---

## 身份验证

### 使用 API 密钥

```bash
# 设置 API 密钥（添加到 shell 配置文件以持久化）
export ANTHROPIC_API_KEY=sk-ant-api03-...

# 或者让 Claude Code 在首次运行时提示你
claude
```

### 使用 AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
# 确保 AWS 凭证已配置
```

### 使用 Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=1
# 确保 Google Cloud 凭证已配置
```

---

## 你的第一次会话

### 启动 Claude Code

```bash
# 进入项目目录
cd your-project

# 启动 Claude Code
claude
```

你会看到一个交互式提示符，可以输入消息给 Claude。

### 试试这些入门命令

```
> 这个项目是做什么的？

> 解释一下文件结构

> 这个项目用了哪些依赖？

> 找出代码库中所有的 TODO 注释
```

### 生成 CLAUDE.md

这是**提升 Claude 效果的最重要操作**：

```
> /init
```

Claude 会分析你的项目并生成一个 `CLAUDE.md` 文件，包含：
- 项目概述
- 技术栈
- 常用命令
- 代码规范

检查并编辑生成的文件 — 这将成为 Claude 对你项目的"记忆"。

---

## 理解 Claude Code 的工作方式

### 工具循环

Claude Code 不只是聊天 — 它会**行动**。工作循环如下：

```
你："给注册表单添加输入验证"
                    │
                    ▼
    ┌─────────────────────────────┐
    │  Claude 分析任务             │
    │  并规划执行方案              │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │  读取相关文件                │◄──┐
    │  (Glob, Read, Grep)         │   │
    └──────────────┬──────────────┘   │
                   │                   │
                   ▼                   │
    ┌─────────────────────────────┐   │
    │  做出修改                    │   │ 循环直到
    │  (Edit, Write, Bash)        │   │ 任务完成
    └──────────────┬──────────────┘   │
                   │                   │
                   ▼                   │
    ┌─────────────────────────────┐   │
    │  验证修改                    │───┘
    │  (运行测试、检查输出)        │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │  向你报告结果                │
    └─────────────────────────────┘
```

### 权限提示

Claude 在以下操作前会征求你的同意：
- **写入或编辑文件** — 先展示修改内容
- **运行 Shell 命令** — 先展示命令

你可以批准（`y`）、拒绝（`n`），或永久允许特定操作。

### 上下文窗口

Claude 有大容量上下文窗口（Opus 4.6 最高 1M tokens），但不是无限的。建议：
- 对话变长时使用 `/compact`
- 使用 `/clear` 重新开始
- 用 `CLAUDE.md` 存放持久化上下文，而不是重复说明

---

## 你的第一个真实任务

在任何项目中试试这些实际例子：

### 任务：添加功能

```
> 在 GET /health 添加一个健康检查端点，返回
  { "status": "ok", "timestamp": "<当前 ISO 时间>" }
```

观察 Claude 如何：
1. 搜索项目中现有的路由模式
2. 按照项目规范创建端点
3. 可能会添加测试（如果项目有测试的话）

### 任务：修复 Bug

```
> npm test

（粘贴错误输出）

> 修复这个测试失败
```

### 任务：理解代码

```
> 解释这个项目中身份验证是如何工作的 — 追踪从
  登录请求到 JWT 令牌签发的完整流程
```

### 任务：重构

```
> 将 UserService 类重构为使用依赖注入，
  而不是直接调用数据库
```

---

## 基础配置

### 配置文件位置

| 文件 | 范围 |
|------|------|
| `.claude/settings.json` | 项目级（提交到 git） |
| `~/.claude/settings.json` | 用户全局 |

### 推荐的初始配置

在项目中创建 `.claude/settings.json`：

```jsonc
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      // 添加你的常用命令：
      // "Bash(npm test)",
      // "Bash(npm run lint)"
    ]
  }
}
```

### 模型选择

```bash
# 使用特定模型
claude --model claude-opus-4-6

# 或设置默认值
export ANTHROPIC_MODEL=claude-sonnet-4-6-20250514

# 会话中切换模型
/model
```

| 模型 | 最适合 |
|------|--------|
| Opus 4.6 | 复杂任务、大型重构、架构设计 |
| Sonnet 4.6 | 日常开发、速度和质量平衡 |
| Haiku 4.5 | 快速提问、简单编辑 |

---

## 新手常用模式

### 1. 先了解再行动

```
> 解释一下 [功能] 的当前实现
（先理解代码）

> 现在按照相同的模式添加 [新功能]
（再做修改）
```

### 2. 审查-修复模式

```
> 审查 src/api/auth.ts 是否有潜在问题
（获取 Claude 的分析）

> 修复你发现的问题
（让 Claude 修复）
```

### 3. 测试驱动模式

```
> 为 [功能] 写一个会失败的测试
（先写测试）

> 现在实现功能让测试通过
（再实现）
```

### 4. 管道快速分析

```bash
# 无需进入交互模式的快速分析
git diff | claude -p "这些修改有什么问题吗？"
cat error.log | claude -p "是什么导致了这个错误？"
```

---

## 快捷键参考

| 按键 | 操作 |
|------|------|
| `Enter` | 发送消息 |
| `Shift+Enter` | 换行 |
| `Shift+Tab` | 切换 Plan 模式 |
| `Esc`（1次） | 取消输入 |
| `Esc`（2次） | 中断 Claude |
| `上箭头` | 浏览历史消息 |
| `!command` | 运行 Shell 命令 |

---

## 下一步学什么

上手之后，按顺序学习这些指南：

1. **[Claude Code 精通](02-claude-code-mastery.md)** — 深入了解所有 CLI 功能
2. **[CLAUDE.md 指南](03-claude-md-guide.md)** — 掌握项目配置
3. **[Hooks 与自动化](04-hooks-and-automation.md)** — 自动化工作流
4. **[MCP 服务器](05-mcp-servers.md)** — 扩展 Claude 的能力

或者直接查看 [速查表](../../cheatsheet.md) 快速参考。

---

<p align="center">
  <strong>下一篇：</strong> <a href="02-claude-code-mastery.md">Claude Code 精通</a> — 掌握每一个功能
</p>
