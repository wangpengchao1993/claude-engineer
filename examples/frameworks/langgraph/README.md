# LangGraph — Production-Grade Agent Orchestration / 生产级 Agent 编排框架

> By the LangChain team | Python & TypeScript
>
> 由 LangChain 团队开发 | 支持 Python 和 TypeScript

---

## What is LangGraph? / 什么是 LangGraph？

LangGraph is a framework for building **stateful, multi-step agent workflows as graphs**.
Think of it as a **"flowchart for AI"** — you define **nodes** (actions) and **edges**
(transitions), and the AI follows the flow.

LangGraph 是一个用于构建**有状态、多步骤 Agent 工作流**的框架，工作流以**图（Graph）**的形式表达。
你可以把它想象成一张 **"AI 流程图"**——你定义**节点**（动作）和**边**（转换），AI 就按照流程执行。

Unlike simple chains, LangGraph gives you **full control** over how your agent reasons,
acts, and recovers from errors — making it ideal for production applications.

与简单链式调用不同，LangGraph 让你**完全掌控** Agent 的推理、行动和错误恢复流程，
非常适合生产环境中的应用。

---

## When to Use LangGraph / 何时使用 LangGraph

| Use LangGraph when... / 适合场景 | Don't use LangGraph when... / 不适合场景 |
|---|---|
| Complex multi-step agent workflows / 复杂的多步骤 Agent 工作流 | Simple sequential chains — use LangChain instead / 简单顺序链——用 LangChain |
| You need checkpointing & state management / 需要检查点和状态管理 | Quick prototypes — use CrewAI instead / 快速原型——用 CrewAI |
| Production apps requiring reliability / 生产应用需要高可靠性 | One-shot LLM calls — just use the API / 单次 LLM 调用——直接用 API |
| Human-in-the-loop approval steps / 需要人工审批环节 | Simple chatbots without tool use / 不需要工具的简单聊天机器人 |

---

## Core Concepts / 核心概念

### 1. StateGraph / 状态图

The **container** for your entire workflow. Like a **whiteboard** where you draw your flowchart.

整个工作流的**容器**，就像一块**白板**，你在上面画流程图。

```python
from langgraph.graph import StateGraph
graph = StateGraph(AgentState)  # Create the whiteboard / 创建白板
```

### 2. Node / 节点

A **single step** in your workflow. Each node is a Python function that does one thing.
Like a **box** in a flowchart.

工作流中的**单个步骤**。每个节点是一个执行单一任务的 Python 函数，
就像流程图中的一个**方框**。

```python
graph.add_node("think", thinking_function)    # Add a box / 添加方框
graph.add_node("act", action_function)
```

### 3. Edge / 边

A **connection** between two nodes. Like an **arrow** in a flowchart — it says "go here next".

两个节点之间的**连接**，就像流程图中的**箭头**——表示"接下来去这里"。

```python
graph.add_edge("think", "act")  # think → act / 思考 → 行动
```

### 4. Conditional Edge / 条件边

A **branching point** — like a **diamond** in a flowchart that asks "which way?"

一个**分支点**——就像流程图中的**菱形判断框**，问"走哪条路？"

```python
graph.add_conditional_edges(
    "agent",                    # From this node / 从此节点
    should_continue,            # Decision function / 判断函数
    {"continue": "tools", "end": END}  # Route map / 路由映射
)
```

### 5. State / 状态

A **shared notebook** that every node can read and write. It carries information through the
entire workflow.

一个**共享笔记本**，每个节点都可以读写。它在整个工作流中传递信息。

```python
class AgentState(TypedDict):
    messages: list[BaseMessage]   # Chat history / 聊天记录
    next_step: str                # What to do next / 下一步做什么
```

### 6. Checkpointer / 检查点

A **save button** for your workflow. If something crashes, you can resume from the last save.

工作流的**存档按钮**。如果出错了，可以从上次存档点恢复。

```python
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)
```

---

## Quick Start / 快速开始

```bash
# Install LangGraph / 安装 LangGraph
pip install langgraph langchain-core langchain-openai

# Set your API key / 设置 API 密钥
export OPENAI_API_KEY="your-key-here"

# Run the example / 运行示例
python react_agent.py
```

---

## How It Works / 工作原理

```
Define State        Add Nodes         Add Edges         Compile          Run
定义状态     →      添加节点     →    添加边       →    编译       →    运行

┌──────────┐    ┌──────────────┐   ┌─────────────┐   ┌─────────┐   ┌─────────┐
│ TypedDict│    │ graph.add_   │   │ graph.add_  │   │ graph.  │   │ app.    │
│ with     │ →  │ node("name", │ → │ edge(A, B)  │ → │ compile │ → │ invoke  │
│ fields   │    │ function)    │   │ + conditional│   │ ()      │   │ (input) │
└──────────┘    └──────────────┘   └─────────────┘   └─────────┘   └─────────┘
```

### The ReAct Loop / ReAct 循环

```
    ┌─────────────────────────────────────┐
    │                                     │
    v                                     │
┌────────┐     ┌────────┐     ┌────────┐  │
│ Think  │ ──> │  Act   │ ──> │Observe │──┘
│ 思考   │     │  行动  │     │  观察  │
└────────┘     └────────┘     └────────┘
    │
    │ (done / 完成)
    v
┌────────┐
│  END   │
│  结束  │
└────────┘
```

---

## LangGraph vs CrewAI / LangGraph 与 CrewAI 对比

| Feature / 特性 | LangGraph | CrewAI |
|---|---|---|
| Control level / 控制粒度 | Fine-grained (you draw every arrow) / 细粒度（每条边都自己画） | High-level (agents collaborate automatically) / 高层级（Agent 自动协作） |
| Learning curve / 学习曲线 | Steeper — more concepts to learn / 较陡——需要学习更多概念 | Gentler — feels like managing a team / 较平缓——像管理团队 |
| State management / 状态管理 | Built-in checkpointing / 内置检查点 | Basic shared memory / 基础共享内存 |
| Best for / 最适合 | Production reliability / 生产环境可靠性 | Quick multi-agent prototypes / 快速多 Agent 原型 |
| Customization / 定制化 | Maximum flexibility / 最大灵活性 | Convention over configuration / 约定优于配置 |
| Error handling / 错误处理 | Granular retry & fallback / 细粒度重试和回退 | Automatic delegation / 自动委托 |

**Rule of thumb / 经验法则:**
- Need full control? → **LangGraph** / 需要完全控制？→ **LangGraph**
- Need it working fast? → **CrewAI** / 需要快速上手？→ **CrewAI**

---

## Learn More / 了解更多

- [LangGraph Documentation / 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Tutorials / 教程](https://langchain-ai.github.io/langgraph/tutorials/)
- [LangChain Academy — LangGraph Course / LangChain 学院课程](https://academy.langchain.com/)
- [ReAct Paper / ReAct 论文](https://arxiv.org/abs/2210.03629)
