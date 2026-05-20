"""
LangGraph ReAct Agent Example / LangGraph ReAct 智能体示例
==========================================================

This example builds a ReAct (Reason + Act) agent using LangGraph.
The agent follows a loop: Think → Act → Observe → Repeat.

本示例使用 LangGraph 构建一个 ReAct（推理 + 行动）智能体。
该智能体遵循循环：思考 → 行动 → 观察 → 重复。

Pattern / 模式:
    agent_node → should_continue? → tool_node → agent_node (loop)
                                  → END (if done)
"""

import json
from typing import Annotated, TypedDict

# --- LangGraph imports / LangGraph 导入 ---
# StateGraph: the "whiteboard" where we draw our flowchart
# StateGraph: 我们画流程图的"白板"
# END: a special marker meaning "workflow is finished"
# END: 特殊标记，表示"工作流结束"
from langgraph.graph import StateGraph, END

# --- Message types / 消息类型 ---
# These represent different speakers in the conversation
# 这些代表对话中的不同角色
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,   # User's message / 用户消息
    AIMessage,       # AI's response / AI 回复
    ToolMessage,     # Tool's result / 工具执行结果
)


# ============================================================
# Step 1: Define the State / 第一步：定义状态
# ============================================================
# State is like a shared notebook — every node can read/write it.
# 状态就像一个共享笔记本——每个节点都可以读写它。

class AgentState(TypedDict):
    """The shared state passed between all nodes. / 在所有节点间传递的共享状态。"""
    messages: list[BaseMessage]  # Full conversation history / 完整对话历史


# ============================================================
# Step 2: Define Tools / 第二步：定义工具
# ============================================================
# Tools are functions the agent can call to interact with the world.
# 工具是智能体可以调用的函数，用于与外部世界交互。

def search(query: str) -> str:
    """Fake search tool — returns mock results. / 模拟搜索工具——返回模拟结果。"""
    # In production, this would call a real search API.
    # 在生产环境中，这里会调用真实的搜索 API。
    mock_results = {
        "langgraph": "LangGraph is a library by LangChain for building stateful agent workflows.",
        "weather":   "Today's weather: sunny, 25 degrees Celsius.",
    }
    for key, value in mock_results.items():
        if key in query.lower():
            return value
    return f"No results found for: {query} / 未找到关于 {query} 的结果"


def calculator(expression: str) -> str:
    """Fake calculator tool — evaluates simple math. / 模拟计算器工具——计算简单数学表达式。"""
    try:
        # WARNING: eval() is unsafe in production! Use a proper math parser.
        # 警告：eval() 在生产环境中不安全！请使用专业的数学解析器。
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Registry of available tools / 可用工具注册表
TOOLS = {"search": search, "calculator": calculator}


# ============================================================
# Step 3: Define Nodes / 第三步：定义节点
# ============================================================
# Each node is a function that takes state and returns updated state.
# 每个节点是一个接收状态并返回更新后状态的函数。

def agent_node(state: AgentState) -> AgentState:
    """
    The 'thinking' node — the agent decides what to do next.
    "思考"节点——智能体决定下一步做什么。

    In production, this would call an LLM (e.g., GPT-4, Claude).
    Here we simulate the decision for demonstration purposes.
    在生产环境中，这里会调用 LLM（如 GPT-4、Claude）。
    这里为了演示，我们模拟决策过程。
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Simulate AI decision: if the last message is from a human, use a tool.
    # If we already got a tool result, we're done.
    # 模拟 AI 决策：如果最后一条是用户消息，则调用工具；
    # 如果已经拿到工具结果，就结束。
    if isinstance(last_message, HumanMessage):
        # Agent decides to search / 智能体决定搜索
        ai_msg = AIMessage(
            content="Let me search for that. / 让我搜索一下。",
            additional_kwargs={
                "tool_calls": [{"name": "search", "args": last_message.content}]
            },
        )
        return {"messages": messages + [ai_msg]}
    elif isinstance(last_message, ToolMessage):
        # Agent has the tool result, formulate final answer
        # 智能体已获得工具结果，生成最终答案
        ai_msg = AIMessage(
            content=f"Based on my research: {last_message.content} "
                    f"/ 根据我的调查：{last_message.content}"
        )
        return {"messages": messages + [ai_msg]}
    else:
        # Nothing more to do / 没有更多要做的了
        return state


def tool_node(state: AgentState) -> AgentState:
    """
    The 'action' node — executes the tool the agent chose.
    "行动"节点——执行智能体选择的工具。
    """
    messages = state["messages"]
    last_ai_message = messages[-1]

    # Extract the tool call from the AI message / 从 AI 消息中提取工具调用
    tool_calls = last_ai_message.additional_kwargs.get("tool_calls", [])
    if not tool_calls:
        return state

    tool_call = tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    # Execute the tool / 执行工具
    if tool_name in TOOLS:
        result = TOOLS[tool_name](tool_args)
    else:
        result = f"Unknown tool: {tool_name} / 未知工具：{tool_name}"

    # Return the result as a ToolMessage / 将结果作为 ToolMessage 返回
    tool_msg = ToolMessage(content=result, tool_call_id=tool_name)
    return {"messages": messages + [tool_msg]}


# ============================================================
# Step 4: Define the Decision Function / 第四步：定义决策函数
# ============================================================

def should_continue(state: AgentState) -> str:
    """
    The 'diamond' in the flowchart — decides where to go next.
    流程图中的"菱形判断框"——决定下一步去哪里。

    Returns:
        "continue" → go to tool_node (agent wants to use a tool)
        "end"      → go to END (agent is done)
    返回值：
        "continue" → 去工具节点（智能体想使用工具）
        "end"      → 结束（智能体已完成）
    """
    messages = state["messages"]
    last_message = messages[-1]

    # If the AI message has tool calls, continue to tool_node
    # 如果 AI 消息包含工具调用，继续到工具节点
    if isinstance(last_message, AIMessage):
        tool_calls = last_message.additional_kwargs.get("tool_calls", [])
        if tool_calls:
            return "continue"

    return "end"


# ============================================================
# Step 5: Build the Graph / 第五步：构建图
# ============================================================

def build_react_agent() -> StateGraph:
    """
    Assemble the ReAct agent graph. / 组装 ReAct 智能体图。

    The graph looks like this / 图的结构如下：
        agent → should_continue? → tools → agent (loop)
                                 → END
    """
    # Create the graph with our state type / 用状态类型创建图
    graph = StateGraph(AgentState)

    # Add nodes (the "boxes" in our flowchart) / 添加节点（流程图中的"方框"）
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # Set the entry point — where the workflow starts / 设置入口点——工作流从这里开始
    graph.set_entry_point("agent")

    # Add a conditional edge (the "diamond") from agent
    # 从 agent 添加条件边（"菱形判断框"）
    graph.add_conditional_edges(
        "agent",                              # From node / 起始节点
        should_continue,                      # Decision function / 判断函数
        {"continue": "tools", "end": END},    # Route map / 路由映射
    )

    # After tools run, always go back to agent (the loop!)
    # 工具执行后，始终回到 agent（循环！）
    graph.add_edge("tools", "agent")

    return graph


# ============================================================
# Step 6: Run the Agent / 第六步：运行智能体
# ============================================================

if __name__ == "__main__":
    # Build and compile the graph / 构建并编译图
    graph = build_react_agent()
    app = graph.compile()

    print("=" * 60)
    print("LangGraph ReAct Agent / LangGraph ReAct 智能体")
    print("=" * 60)

    # Create the initial input / 创建初始输入
    initial_state = {
        "messages": [HumanMessage(content="langgraph")]
    }

    # Run the agent! / 运行智能体！
    # invoke() runs the graph from start to END
    # invoke() 从起点运行图到 END
    result = app.invoke(initial_state)

    # Print each message in the conversation / 打印对话中的每条消息
    print("\nConversation / 对话记录:")
    print("-" * 40)
    for msg in result["messages"]:
        role = type(msg).__name__
        print(f"  [{role}] {msg.content}")

    print("-" * 40)
    print("Done! The ReAct loop has completed. / 完成！ReAct 循环已结束。")
