# 多 Agent 模式

> 编排多个 Claude Agent 完成复杂任务 — 并行执行、专业化分工和工作流组合。

## 目录

- [什么是多 Agent 模式？](#什么是多-agent-模式)
- [Claude Code 子 Agent](#claude-code-子-agent)
- [Agent 模式](#agent-模式)
- [真实案例](#真实案例)
- [构建自定义多 Agent 系统](#构建自定义多-agent-系统)
- [最佳实践](#最佳实践)

---

## 什么是多 Agent 模式？

多 Agent 模式使用多个 Claude 实例协同工作，每个都有特定的角色或关注领域：

- **并行性** — 多个 Agent 同时工作
- **专业化** — 每个 Agent 专注于擅长的领域
- **上下文隔离** — 每个 Agent 有自己的上下文窗口
- **可扩展** — 处理单个 Agent 无法完成的大型任务

---

## Claude Code 子 Agent

Claude Code 内置了多 Agent 能力。给 Claude 复杂任务时，它会自动启动**子 Agent**：

### 内置 Agent 类型

| 类型 | 用途 | 示例 |
|------|------|------|
| **Explore** | 快速代码库搜索和分析 | "查找所有废弃 API 的使用" |
| **Plan** | 设计实现方案 | "规划数据库迁移" |
| **General** | 多步骤复杂任务 | "在 20 个文件中重构认证" |

### 实际工作方式

```
你："搜索整个代码库的 SQL 注入漏洞并修复"

Claude 内部：
├── Agent 1 (Explore): 搜索 src/api/ 中的原始 SQL
├── Agent 2 (Explore): 搜索 src/services/ 中的查询构建
├── Agent 3 (Explore): 搜索 src/repositories/ 中的 ORM 使用
│
└── 主 Agent: 收集发现，逐一修复漏洞
```

---

## Agent 模式

### 模式 1：扇出/扇入

多个 Agent 并行工作，结果合并。

```
                    ┌── Agent: 审查认证代码 ──────┐
                    │                              │
任务 ──► 分发器 ───┼── Agent: 审查 API 端点 ─────┼──► 合并器 ──► 结果
                    │                              │
                    └── Agent: 审查数据层 ─────────┘
```

**适用场景**：大型代码库的代码审查、安全审计、迁移分析。

### 模式 2：流水线

Agent 顺序工作，每个基于前一个的结果。

```
任务 ──► Agent 1: 分析 ──► Agent 2: 规划 ──► Agent 3: 实现 ──► 结果
```

**适用场景**：复杂功能实现。

### 模式 3：专家路由

路由 Agent 根据任务类型委派给专业 Agent。

```
                     ┌── 前端 Agent (React/CSS) ──────┐
任务 ──► 路由器 ────┼── 后端 Agent (API/DB) ─────────┼──► 结果
                     └── DevOps Agent (CI/CD) ────────┘
```

### 模式 4：审查者/验证者

一个 Agent 执行，另一个审查。

```
任务 ──► 执行 Agent ──► 审查 Agent ──► 通过？──► 结果
              │                          │
              └──────── 修改 ◄───────────┘
```

---

## 真实案例

### 全代码库审计

```
"对整个代码库进行安全审计。检查：
1. 所有数据库查询中的 SQL 注入
2. 所有模板渲染中的 XSS 漏洞
3. 中间件中的认证绕过
4. API 响应中的敏感数据泄露

按严重性组织结果。"
```

### 大规模重构

```
"我们要从 Express 迁移到 Fastify。应用有 40+ 个路由文件。
对每个文件：
1. 转换 Express 路由语法到 Fastify
2. 更新中间件引用
3. 转换 req/res 到 Fastify request/reply

先做计划，再执行。"
```

---

## 构建自定义多 Agent 系统

### 使用 Claude API

```python
import anthropic
import asyncio

client = anthropic.Anthropic()

async def run_agent(system_prompt: str, task: str) -> str:
    """运行一个专门的 Agent。"""
    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

async def fan_out_review(code: str):
    """多角度并行审查。"""
    tasks = [
        run_agent("你是安全专家。只审查安全漏洞。", f"审查：\n{code}"),
        run_agent("你是性能专家。只审查性能瓶颈。", f"审查：\n{code}"),
        run_agent("你是资深开发者。只审查逻辑错误。", f"审查：\n{code}"),
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 使用 Shell 脚本

```bash
#!/bin/bash
# 并行审查多个文件
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(ts|py)$')

for file in $FILES; do
    cat "$file" | claude -p "安全审查这个文件" &
    cat "$file" | claude -p "性能审查这个文件" &
done
wait
echo "所有审查完成。"
```

---

## 最佳实践

1. **角色清晰** — 每个 Agent 有单一、明确的职责
2. **减少通信** — Agent 独立工作效果最好
3. **适当粒度** — 大多数任务 2-5 个 Agent 就够了
4. **优雅降级** — 设计容错，一个 Agent 失败不影响整体
5. **模型匹配** — 简单任务用 Haiku，复杂推理用 Opus

---

<p align="center">
  <strong>下一篇：</strong> <a href="07-api-and-sdk.md">API 与 SDK</a> — 用 Claude 构建应用
</p>

---

[← 上一章：MCP 服务器](05-mcp-servers.md) | [目录](../../README_zh.md) | [下一章：API 与 SDK →](07-api-and-sdk.md)
