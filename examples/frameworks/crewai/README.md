# CrewAI — The Easiest Multi-Agent Framework / 最简单的多智能体框架

> **GitHub Stars**: ~25k | **Language**: Python | **License**: MIT
>
> **GitHub Stars**: 约25k | **语言**: Python | **许可证**: MIT

---

## What is CrewAI? / 什么是 CrewAI？

CrewAI is a framework for creating **teams of AI agents** that work together.
Think of it as **hiring a team of AI employees** — each with their own role, goal, and skills.
You describe who they are and what they should do, and CrewAI coordinates the teamwork.

CrewAI 是一个用于创建**AI智能体团队**的框架。
你可以把它想象成**雇佣一组AI员工** — 每个员工都有自己的角色、目标和技能。
你只需描述他们是谁、该做什么，CrewAI 会自动协调团队合作。

```
You (the manager)  →  Define agents + tasks  →  CrewAI runs the team
你（经理）          →  定义智能体 + 任务       →  CrewAI 运行团队
```

---

## When to Use CrewAI / 什么时候用 CrewAI

**Good fit / 适合的场景:**

- Multi-step research tasks (e.g., research → summarize → report)
  多步骤研究任务（如：调研 → 总结 → 报告）
- Content creation pipelines (e.g., draft → review → publish)
  内容创作流水线（如：起草 → 审阅 → 发布）
- Complex analysis requiring different expertise (e.g., financial + legal review)
  需要不同专业知识的复杂分析（如：财务 + 法律审查）

**Not a good fit / 不适合的场景:**

- Simple single-step tasks — just call the LLM directly
  简单的单步骤任务 — 直接调用大模型即可
- Real-time applications — CrewAI adds coordination overhead
  实时应用 — CrewAI 会增加协调开销
- When you need fine-grained control over agent communication — use LangGraph instead
  当你需要精细控制智能体之间的通信时 — 请使用 LangGraph

---

## Core Concepts / 核心概念

| Concept / 概念 | Analogy / 类比 | Description / 描述 |
|---|---|---|
| **Agent** | Employee / 员工 | An AI with a specific role, goal, and backstory. 一个拥有特定角色、目标和背景的AI。 |
| **Task** | Assignment / 任务 | A specific piece of work assigned to an agent. 分配给智能体的具体工作。 |
| **Crew** | Team / 团队 | A group of agents working together. 一组协同工作的智能体。 |
| **Tool** | Skill / 技能 | A capability an agent can use (e.g., web search). 智能体可以使用的能力（如网络搜索）。 |
| **Process** | Workflow / 工作流 | How tasks are executed — sequential or hierarchical. 任务的执行方式 — 顺序或层级。 |

---

## Quick Start / 快速开始

```bash
# Install CrewAI / 安装 CrewAI
pip install crewai

# Or with extra tools / 或者安装额外工具
pip install crewai[tools]

# Run the example / 运行示例
python research_team.py
```

> **Note / 注意**: You need an OpenAI API key (or other LLM provider) set as an environment variable.
> 你需要设置 OpenAI API 密钥（或其他大模型提供商）作为环境变量。
>
> ```bash
> export OPENAI_API_KEY="your-key-here"
> ```

---

## How It Works / 工作原理

The workflow is simple — four steps:
工作流非常简单 — 四个步骤：

```
Step 1: Define Agents    →  Who is on the team?
步骤1：定义智能体         →  团队里有谁？

Step 2: Define Tasks      →  What does each person do?
步骤2：定义任务           →  每个人做什么？

Step 3: Create a Crew     →  Put the team together
步骤3：创建团队           →  把团队组建起来

Step 4: Kick off!         →  Let them work
步骤4：启动！             →  让他们开始工作
```

```python
from crewai import Agent, Task, Crew, Process

# Step 1: Create agents / 步骤1：创建智能体
researcher = Agent(role="Researcher", goal="Find accurate info", backstory="...")
writer = Agent(role="Writer", goal="Write clear articles", backstory="...")

# Step 2: Create tasks / 步骤2：创建任务
research_task = Task(description="Research AI trends", agent=researcher, expected_output="Report")
write_task = Task(description="Write an article", agent=writer, expected_output="Article")

# Step 3: Assemble the crew / 步骤3：组建团队
crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)

# Step 4: Start! / 步骤4：启动！
result = crew.kickoff()
```

---

## CrewAI vs LangGraph / CrewAI 与 LangGraph 对比

| | CrewAI | LangGraph |
|---|---|---|
| **Ease of use / 易用性** | Very easy — just define roles and tasks. 非常简单 — 只需定义角色和任务。 | Steeper learning curve. 学习曲线较陡。 |
| **Control / 控制力** | High-level, automatic coordination. 高层级，自动协调。 | Fine-grained, you control every step. 细粒度，你控制每一步。 |
| **Best for / 最适合** | Role-based teamwork. 基于角色的团队合作。 | Complex state machines and custom flows. 复杂状态机和自定义流程。 |
| **Mental model / 心智模型** | A team of employees. 一组员工。 | A flowchart / graph. 流程图 / 图。 |

**Rule of thumb / 经验法则:**
- Start with CrewAI if your problem maps naturally to "a team of specialists."
  如果你的问题可以自然地映射为"一组专家团队"，就用 CrewAI。
- Switch to LangGraph when you need precise control over agent communication and state.
  当你需要精确控制智能体通信和状态时，切换到 LangGraph。

---

## Learn More / 了解更多

- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI Examples](https://github.com/crewAIInc/crewAI-examples)
- [Getting Started Guide](https://docs.crewai.com/quickstart)

---

## Files in This Example / 本示例中的文件

| File / 文件 | Description / 描述 |
|---|---|
| `research_team.py` | A complete example: 3 agents collaborate to research, write, and edit an article. 完整示例：3个智能体协作完成调研、写作和编辑。 |
| `test_crewai.py` | Tests that verify agent/task/crew setup without needing API keys. 无需API密钥即可验证智能体/任务/团队设置的测试。 |
