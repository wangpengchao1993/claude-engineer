# Claude Agent SDK

> 用 Claude Agent SDK 构建生产级 AI Agent — 工具使用、护栏、多 Agent 编排。

## 目录

- [什么是 Agent SDK？](#什么是-agent-sdk)
- [快速开始](#快速开始)
- [定义工具](#定义工具)
- [Agent 配置](#agent-配置)
- [护栏（Guardrails）](#护栏guardrails)
- [多 Agent 编排](#多-agent-编排)
- [模式与最佳实践](#模式与最佳实践)

---

## 什么是 Agent SDK？

Claude Agent SDK 提供了构建 AI Agent 的框架：

- **使用工具** 与真实世界交互（数据库、API、文件系统）
- **推理** 多步骤问题
- **遵循护栏** 在定义的边界内工作
- **编排** 多个专业 Agent

---

## 快速开始

```bash
# 安装
pip install claude-agent-sdk    # Python
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
```

### 最小 Agent

```python
from claude_agent_sdk import Agent, tool

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    from datetime import datetime
    return datetime.now().isoformat()

@tool
def calculate(expression: str) -> str:
    """安全地计算数学表达式。"""
    import ast
    result = eval(compile(ast.parse(expression, mode='eval'), '<string>', 'eval'))
    return str(result)

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[get_current_time, calculate],
    system_prompt="你是一个有时钟和计算器的助手。",
)

result = agent.run("现在几点？2 的 32 次方是多少？")
print(result)
```

---

## 定义工具

### 基础工具

```python
@tool
def search_products(query: str, category: str = None, max_results: int = 10) -> list[dict]:
    """搜索产品目录。

    Args:
        query: 搜索关键词
        category: 可选的分类过滤（电子产品、服装等）
        max_results: 最大返回数量（默认 10）
    """
    results = db.products.search(query, category=category, limit=max_results)
    return [{"id": p.id, "name": p.name, "price": p.price} for p in results]
```

### 异步工具

```python
@tool
async def fetch_url(url: str) -> str:
    """获取网页内容。"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 工具错误处理

```python
from claude_agent_sdk import tool, ToolError

@tool
def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """在账户间转账。"""
    if amount <= 0:
        raise ToolError("金额必须为正数")
    if amount > 10000:
        raise ToolError("超过 10,000 的转账需要人工审批")
    result = bank.transfer(from_account, to_account, amount)
    return {"transaction_id": result.id, "status": "completed"}
```

---

## Agent 配置

```python
agent = Agent(
    model="claude-sonnet-4-6-20250514",
    max_tokens=4096,
    temperature=0.7,
    system_prompt="...",
    tools=[tool1, tool2, tool3],
    max_turns=30,
    thinking={"type": "enabled", "budget_tokens": 5000},
)
```

### 动态系统提示

```python
def build_prompt(ctx: dict) -> str:
    return f"""你是 {ctx['company']} 的客服。
    客户计划：{ctx['plan']}
    账号年龄：{ctx['account_age_days']} 天
    根据客户历史调整你的语气和深度。"""

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=support_tools,
    system_prompt=build_prompt(user_ctx),
)
```

---

## 护栏（Guardrails）

### 输入护栏

```python
from claude_agent_sdk import InputGuardrail

def check_pii(message: str) -> str | None:
    """阻止包含信用卡号的消息。"""
    import re
    if re.search(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', message):
        return "请不要分享信用卡号。我可以通过安全门户帮你更新支付信息。"
    return None  # None 表示允许

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=support_tools,
    input_guardrails=[InputGuardrail(check_pii)],
)
```

### 输出护栏

```python
from claude_agent_sdk import OutputGuardrail

def check_no_internal_info(response: str) -> str | None:
    """确保 Agent 不泄露内部信息。"""
    blocked = ["internal-api", "admin-panel", "secret-key"]
    for term in blocked:
        if term in response.lower():
            return "抱歉，我无法分享该信息。让我用其他方式帮你。"
    return None
```

---

## 多 Agent 编排

### 交接模式

```python
from claude_agent_sdk import Agent, handoff

# 专业 Agent
billing_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_balance, process_refund],
    system_prompt="你处理计费问题和退款。",
)

technical_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_logs, restart_service],
    system_prompt="你处理技术问题和调试。",
)

# 路由 Agent
router = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[
        handoff(billing_agent, "转接到计费支持"),
        handoff(technical_agent, "转接到技术支持"),
    ],
    system_prompt="你是前台。判断用户问题类型并转接到合适的专家。",
)

result = router.run("我的 API 一直返回 503 错误")
```

### 流水线模式

```python
async def process_document(document: str) -> dict:
    # 步骤 1：提取数据（用快速模型）
    extractor = Agent(model="claude-haiku-4-5-20251001", tools=[],
                      system_prompt="从文档中提取结构化数据，返回 JSON。")
    extracted = await extractor.run(f"提取关键字段：\n{document}")

    # 步骤 2：验证和丰富
    validator = Agent(model="claude-sonnet-4-6-20250514",
                      tools=[lookup_company, verify_address],
                      system_prompt="验证和丰富提取的数据。")
    validated = await validator.run(f"验证：\n{extracted}")

    # 步骤 3：生成报告
    reporter = Agent(model="claude-sonnet-4-6-20250514", tools=[],
                     system_prompt="从数据生成简洁的商业报告。")
    return {"report": await reporter.run(f"生成报告：\n{validated}")}
```

---

## 模式与最佳实践

### 1. 工具要专注

```python
# 差：一个万能工具
@tool
def do_everything(action: str, params: dict) -> dict: ...

# 好：单一职责
@tool
def search_orders(customer_id: str) -> list[dict]: ...
@tool
def cancel_order(order_id: str, reason: str) -> dict: ...
```

### 2. 写详细的工具描述

```python
@tool
def search_knowledge_base(query: str) -> list[dict]:
    """搜索公司知识库。

    使用时机：
    - 用户问你不知道答案的产品问题
    - 用户需要功能的分步操作说明

    不要使用：
    - 账户相关问题（用 get_account）
    - 计费问题（用 check_billing）
    """
```

### 3. 为每个 Agent 选对模型

| Agent 角色 | 推荐模型 |
|-----------|---------|
| 路由/分类 | Haiku 4.5（快速、便宜） |
| 数据提取 | Haiku 4.5 |
| 业务逻辑 | Sonnet 4.6 |
| 复杂推理 | Opus 4.6 |

---

<p align="center">
  <strong>下一篇：</strong> <a href="09-prompt-engineering.md">Prompt 工程</a> — 从 Claude 获得最佳结果
</p>
