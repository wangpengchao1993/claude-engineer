# OpenAI Agents SDK — OpenAI's Official Agent Framework / OpenAI 官方 Agent 框架

> **Released**: March 2025 | **Language**: Python | **License**: MIT
>
> **发布时间**: 2025年3月 | **语言**: Python | **许可证**: MIT

---

## What is it? / 这是什么？

OpenAI Agents SDK is OpenAI's **lightweight, official framework** for building AI agents.
Think of it as the **"official way"** to build agents with OpenAI models.
It provides a simple **Agent -> Tool -> Handoff** pattern — no complex abstractions needed.

OpenAI Agents SDK 是 OpenAI 官方推出的**轻量级 Agent 框架**。
你可以把它理解为使用 OpenAI 模型构建智能体的**"官方方式"**。
它提供了一个简单的 **Agent -> Tool -> Handoff** 模式 — 不需要复杂的抽象。

```
You define Agent  →  Add Tools  →  Runner.run()  →  Handle Handoffs
你定义 Agent     →  添加工具    →  Runner.run()  →  处理交接
```

---

## When to Use / 什么时候用

**Good fit / 适合的场景:**

- Building agents powered by OpenAI models (GPT-4o, o3, etc.)
  使用 OpenAI 模型（GPT-4o、o3 等）构建智能体
- Need handoff between multiple agents (e.g., triage → specialist)
  需要多个智能体之间交接（如：分诊 → 专家）
- Want official SDK support backed by OpenAI
  想要 OpenAI 官方支持的 SDK
- Simple agent workflows without heavy orchestration
  简单的 Agent 工作流，不需要重度编排

**Not a good fit / 不适合的场景:**

- Using non-OpenAI models (Claude, Gemini, Llama) — this SDK is OpenAI-only
  使用非 OpenAI 模型（Claude、Gemini、Llama）— 此 SDK 仅支持 OpenAI
- Need complex graph workflows with cycles and conditionals — use LangGraph instead
  需要带循环和条件的复杂图工作流 — 请使用 LangGraph
- Want model-agnostic code that works across providers — use LiteLLM
  想要跨提供商的模型无关代码 — 请使用 LiteLLM
- Need a full multi-agent team simulation — use CrewAI
  需要完整的多智能体团队模拟 — 请使用 CrewAI

---

## Core Concepts / 核心概念

| Concept / 概念 | Analogy / 类比 | Description / 描述 |
|---|---|---|
| **Agent** | Worker / 工人 | An AI with a name, instructions, and tools. 一个拥有名称、指令和工具的AI。 |
| **Tool** (`function_tool`) | Skill / 技能 | A Python function the agent can call. 智能体可以调用的 Python 函数。 |
| **Runner** | Manager / 经理 | Executes the agent loop — sends messages, calls tools, handles handoffs. 执行 Agent 循环 — 发送消息、调用工具、处理交接。 |
| **Handoff** | Delegation / 委托 | Pass control from one agent to another. 将控制权从一个智能体传递给另一个。 |
| **Guardrail** | Safety check / 安全检查 | Validates input/output before or after the agent runs. 在运行前后验证输入/输出。 |

---

## Quick Start / 快速开始

```bash
# Install the SDK / 安装 SDK
pip install openai-agents

# Set your API key / 设置 API 密钥
export OPENAI_API_KEY="your-key-here"

# Run the example / 运行示例
python simple_agent.py

# Run tests (no API key needed) / 运行测试（不需要 API 密钥）
pytest test_openai_agents.py -v
```

> **Note / 注意**: You need an OpenAI API key to run the agent.
> Tests use mocks and do NOT require a real API key.
>
> 运行智能体需要 OpenAI API 密钥。
> 测试使用 mock，不需要真实的 API 密钥。

---

## How It Works / 工作原理

```
Step 1: Define agents with instructions and tools
        定义带有指令和工具的 Agent

Step 2: Runner.run() starts the agent loop
        Runner.run() 启动 Agent 循环

Step 3: Agent receives user message, decides to call tools or respond
        Agent 接收用户消息，决定调用工具还是直接回复

Step 4: If handoff is needed, control passes to another agent
        如果需要交接，控制权传递给另一个 Agent

Step 5: Loop continues until final response
        循环继续直到最终回复
```

```python
from agents import Agent, Runner, function_tool

# Step 1: Define a tool / 定义工具
@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: 22C, sunny"

# Step 2: Define an agent / 定义 Agent
agent = Agent(
    name="Weather Bot",
    instructions="You help users check the weather.",
    tools=[get_weather],
)

# Step 3: Run it / 运行
result = Runner.run_sync(agent, "What's the weather in Tokyo?")
print(result.final_output)
```

---

## Comparison with Claude Agent SDK / 与 Claude Agent SDK 的对比

| Feature / 特性 | OpenAI Agents SDK | Claude Agent SDK |
|---|---|---|
| **Provider / 提供商** | OpenAI only / 仅 OpenAI | Anthropic only / 仅 Anthropic |
| **Pattern / 模式** | Agent + Tool + Handoff | Agent + Tool + Handoff |
| **Multi-agent / 多智能体** | Handoff between agents / 智能体交接 | Handoff between agents / 智能体交接 |
| **Safety / 安全** | Guardrails / 护栏 | Built-in safety / 内置安全 |
| **Async support / 异步** | Yes (asyncio) / 是 | Yes (asyncio) / 是 |
| **Complexity / 复杂度** | Low — minimal abstractions / 低 — 最少抽象 | Low — minimal abstractions / 低 — 最少抽象 |
| **Best for / 最适合** | OpenAI model users / OpenAI 用户 | Claude model users / Claude 用户 |

Both SDKs follow a similar philosophy: **keep it simple, let the model do the work**.
The main difference is which model provider they support.

两个 SDK 遵循类似的理念：**保持简单，让模型来做主要工作**。
主要区别在于支持的模型提供商不同。

---

## Learn More / 了解更多

- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python) — Source code and docs / 源代码和文档
- [OpenAI Agents Documentation](https://openai.github.io/openai-agents-python/) — Official guide / 官方指南
- [OpenAI Blog: Introducing Agents SDK](https://openai.com/index/new-tools-for-building-agents/) — Announcement / 发布公告
- [OpenAI Cookbook](https://cookbook.openai.com/) — Practical examples / 实用示例
