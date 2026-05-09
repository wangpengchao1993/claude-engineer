# 高级工作流

> 结合 Claude Code、API、Hooks 和多 Agent 策略的真实自动化模式。

## 目录

- [自动化代码审查流水线](#自动化代码审查流水线)
- [测试驱动开发工作流](#测试驱动开发工作流)
- [文档生成](#文档生成)
- [迁移助手](#迁移助手)
- [事件响应 Agent](#事件响应-agent)
- [持续代码质量](#持续代码质量)
- [发布管理](#发布管理)

---

## 自动化代码审查流水线

### GitHub Actions 审查 Bot

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Claude 审查
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            审查这个 PR：
            1. Bug 和逻辑错误
            2. 安全漏洞
            3. 性能问题
            4. 新功能是否缺少测试
```

### 自定义分类审查脚本

```bash
#!/bin/bash
# scripts/review-pr.sh
BASE_BRANCH="${1:-main}"
DIFF=$(git diff "origin/$BASE_BRANCH...HEAD")

echo "## 安全审查"
echo "$DIFF" | claude -p \
  --system-prompt "你是安全审计员。只关注安全问题。" \
  "审查这个 diff 的安全漏洞。"

echo "## 逻辑审查"
echo "$DIFF" | claude -p \
  --system-prompt "你是高级开发者。只关注 bug。" \
  "审查这个 diff 的逻辑错误。"
```

---

## 测试驱动开发工作流

### 用 Claude Code 做 TDD

```
步骤 1："为 [功能描述] 写一个会失败的测试"
        Claude 写测试 → 测试失败 → 确认测试正确

步骤 2："现在写最少的代码让测试通过"
        Claude 实现 → 测试通过

步骤 3："保持测试通过的同时重构"
        Claude 重构 → 运行测试 → 确认通过
```

---

## 文档生成

### 从代码生成 API 文档

```bash
#!/bin/bash
ROUTES=$(find src/api -name "*.ts" -o -name "*.py" | sort)

echo "# API 文档" > docs/api.md
echo "生成于 $(date -I)" >> docs/api.md

for route_file in $ROUTES; do
    cat "$route_file" | claude -p \
      --system-prompt "生成 Markdown API 文档。包含：方法、路径、描述、请求体、响应格式、错误码。" \
      "记录这个文件中的所有 API 端点。" >> docs/api.md
done
```

### 变更日志生成

```bash
#!/bin/bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")
COMMITS=$(git log "$LAST_TAG"..HEAD --oneline)

echo "$COMMITS" | claude -p \
  --system-prompt "生成面向用户的变更日志。分组：新功能、Bug 修复、破坏性变更。简洁明了。" \
  "从这些提交生成变更日志："
```

---

## 迁移助手

### 数据库迁移

```
"我需要迁移 users 表：
1. 添加 'display_name' 列（varchar 255，可空）
2. 用 first_name + ' ' + last_name 填充
3. 填充后改为非空
4. 在 display_name 上添加索引

生成 Alembic 迁移文件，包含升级和降级。
同时生成数据迁移脚本，要能安全处理 1000 万+ 行的表（批量处理）。"
```

### 框架迁移

```bash
#!/bin/bash
# 逐文件将 Express 路由迁移到 Fastify
find src/routes -name "*.ts" | while read file; do
    echo "迁移：$file"
    claude -p "将这个 Express 路由文件转换为 Fastify。
保持业务逻辑不变。只输出转换后的文件。" < "$file" > "${file}.new"

    diff "$file" "${file}.new" | head -50
    echo "替换 $file？(y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then mv "${file}.new" "$file"; else rm "${file}.new"; fi
done
```

---

## 事件响应 Agent

### 值班助手

```python
from claude_agent_sdk import Agent, tool

@tool
def check_service_health(service: str) -> dict:
    """检查服务的健康端点。"""
    ...

@tool
def get_recent_logs(service: str, lines: int = 100) -> str:
    """获取服务的最近日志。"""
    ...

@tool
def get_metrics(service: str, metric: str) -> dict:
    """查询 Prometheus 指标。"""
    ...

incident_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_service_health, get_recent_logs, get_metrics],
    system_prompt="""你是值班事件响应助手。

    调查步骤：
    1. 先检查服务健康状态
    2. 查看最近日志中的错误
    3. 检查关键指标（错误率、延迟、CPU、内存）
    4. 识别根本原因
    5. 建议修复步骤

    总是解释你的推理。""",
)

result = incident_agent.run("API 返回 503 错误。10 分钟前开始有用户报告。")
```

---

## 持续代码质量

### Pre-Commit 质量门

```bash
#!/bin/bash
# .git/hooks/pre-commit
DIFF=$(git diff --cached)
if [ -n "$DIFF" ]; then
    RESULT=$(echo "$DIFF" | claude -p \
      --max-turns 1 \
      --system-prompt "快速质量检查。只标记严重问题：安全漏洞、明显 bug、数据丢失风险。没问题就说 'PASS'。" \
      "快速审查：")

    if [[ "$RESULT" != *"PASS"* ]]; then
        echo "质量检查发现问题："
        echo "$RESULT"
        exit 1
    fi
fi
```

### 定期代码健康检查

```bash
#!/bin/bash
# 每周通过 cron 运行
REPORT="reports/health-$(date -I).md"
echo "# 代码健康报告 — $(date -I)" > "$REPORT"

echo "## TODO 待办" >> "$REPORT"
grep -rn "TODO\|FIXME\|HACK" src/ 2>/dev/null | \
  claude -p "按紧急程度分类（严重/中等/低）并总结。" >> "$REPORT"

echo "## 测试覆盖率" >> "$REPORT"
npm test -- --coverage 2>&1 | \
  claude -p "总结测试覆盖率。标出覆盖率低于 50% 的文件。" >> "$REPORT"
```

---

## 发布管理

### 自动发布说明

```bash
#!/bin/bash
VERSION="$1"
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
COMMITS=$(git log "${LAST_TAG}..HEAD" --oneline --no-merges)

NOTES=$(echo "$COMMITS" | claude -p \
  --system-prompt "生成专业的发布说明。包含：亮点、新功能、Bug 修复、破坏性变更。面向用户的语言。" \
  "生成 $VERSION 版本的发布说明：")

echo "$NOTES"
echo "创建发布 $VERSION？(y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    echo "$NOTES" | gh release create "$VERSION" --title "$VERSION" --notes-file -
fi
```

---

## 组合模式

真正的力量来自组合这些工作流：

```
1. 创建功能分支
2. 开发者用 Claude Code 工作（交互式）
3. Pre-commit hook 做快速质量检查
4. 自动生成 PR 描述
5. CI 运行 Claude 审查 + 测试
6. 合并时自动生成变更日志
7. 发布时自动生成发布说明
```

每一步以不同方式使用 Claude — 交互式、脚本化和 CI 集成 — 创造无缝的开发体验。

---

<p align="center">
  <strong>回到起点：</strong> <a href="01-getting-started.md">入门指南</a>
</p>
