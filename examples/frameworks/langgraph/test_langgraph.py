"""
LangGraph Tests (No API Keys Required) / LangGraph 测试（无需 API 密钥）
========================================================================

These tests verify LangGraph graph construction and configuration
without making any real LLM calls.

这些测试验证 LangGraph 图的构建和配置，不会进行任何真实的 LLM 调用。

Run with / 运行方式: pytest test_langgraph.py -v
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage


# Import our agent code / 导入我们的智能体代码
from react_agent import (
    AgentState,
    agent_node,
    tool_node,
    should_continue,
    build_react_agent,
    search,
    calculator,
)


# ============================================================
# Test 1: State Schema / 测试 1：状态结构定义
# ============================================================

class TestStateSchema:
    """Test that the state schema is correctly defined. / 测试状态结构是否正确定义。"""

    def test_agent_state_has_messages_field(self):
        """AgentState should have a 'messages' field. / AgentState 应包含 'messages' 字段。"""
        assert "messages" in AgentState.__annotations__

    def test_state_can_hold_messages(self):
        """State should accept a list of messages. / 状态应能存放消息列表。"""
        state: AgentState = {"messages": [HumanMessage(content="hello")]}
        assert len(state["messages"]) == 1
        assert state["messages"][0].content == "hello"


# ============================================================
# Test 2: Graph Construction / 测试 2：图的构建
# ============================================================

class TestGraphConstruction:
    """Test that the graph is built correctly. / 测试图是否正确构建。"""

    def test_build_react_agent_returns_graph(self):
        """build_react_agent() should return a StateGraph. / 应返回 StateGraph 对象。"""
        graph = build_react_agent()
        assert isinstance(graph, StateGraph)

    def test_graph_compiles_successfully(self):
        """The graph should compile without errors. / 图应能无错编译。"""
        graph = build_react_agent()
        app = graph.compile()
        # A compiled graph (CompiledGraph) should be callable
        # 编译后的图（CompiledGraph）应该是可调用的
        assert app is not None


# ============================================================
# Test 3: Node Behavior / 测试 3：节点行为
# ============================================================

class TestNodes:
    """Test individual node functions. / 测试各个节点函数。"""

    def test_agent_node_responds_to_human_message(self):
        """Agent should produce a tool call when given a human message.
        当收到用户消息时，智能体应产生工具调用。"""
        state = {"messages": [HumanMessage(content="langgraph")]}
        result = agent_node(state)
        last_msg = result["messages"][-1]
        assert isinstance(last_msg, AIMessage)
        assert "tool_calls" in last_msg.additional_kwargs

    def test_agent_node_finishes_after_tool_result(self):
        """Agent should produce a final answer after receiving tool results.
        收到工具结果后，智能体应生成最终答案。"""
        state = {
            "messages": [
                HumanMessage(content="test"),
                AIMessage(content="searching..."),
                ToolMessage(content="some result", tool_call_id="search"),
            ]
        }
        result = agent_node(state)
        last_msg = result["messages"][-1]
        assert isinstance(last_msg, AIMessage)
        assert "some result" in last_msg.content

    def test_tool_node_executes_search(self):
        """Tool node should execute the search tool. / 工具节点应执行搜索工具。"""
        state = {
            "messages": [
                AIMessage(
                    content="searching",
                    additional_kwargs={
                        "tool_calls": [{"name": "search", "args": "langgraph"}]
                    },
                )
            ]
        }
        result = tool_node(state)
        last_msg = result["messages"][-1]
        assert isinstance(last_msg, ToolMessage)
        assert "LangGraph" in last_msg.content


# ============================================================
# Test 4: Edge Configuration / 测试 4：边的配置
# ============================================================

class TestEdges:
    """Test the conditional edge logic. / 测试条件边逻辑。"""

    def test_should_continue_when_tool_calls_present(self):
        """Should return 'continue' when AI wants to use a tool.
        当 AI 想使用工具时，应返回 'continue'。"""
        state = {
            "messages": [
                AIMessage(
                    content="let me check",
                    additional_kwargs={
                        "tool_calls": [{"name": "search", "args": "test"}]
                    },
                )
            ]
        }
        assert should_continue(state) == "continue"

    def test_should_end_when_no_tool_calls(self):
        """Should return 'end' when AI has no more tool calls.
        当 AI 没有更多工具调用时，应返回 'end'。"""
        state = {"messages": [AIMessage(content="Here is your answer.")]}
        assert should_continue(state) == "end"

    def test_should_end_for_non_ai_message(self):
        """Should return 'end' for non-AI messages. / 对于非 AI 消息应返回 'end'。"""
        state = {"messages": [HumanMessage(content="hello")]}
        assert should_continue(state) == "end"


# ============================================================
# Test 5: Tools / 测试 5：工具
# ============================================================

class TestTools:
    """Test tool functions independently. / 独立测试工具函数。"""

    def test_search_finds_known_topic(self):
        """Search should return results for known topics. / 搜索已知话题应返回结果。"""
        result = search("Tell me about langgraph")
        assert "LangGraph" in result

    def test_search_returns_not_found_for_unknown(self):
        """Search should indicate when nothing is found. / 未找到时应有提示。"""
        result = search("xyzzy_unknown_topic")
        assert "No results" in result

    def test_calculator_basic_math(self):
        """Calculator should handle basic arithmetic. / 计算器应处理基本运算。"""
        assert calculator("2 + 3") == "5"
        assert calculator("10 * 5") == "50"

    def test_calculator_handles_errors(self):
        """Calculator should handle invalid expressions. / 计算器应处理无效表达式。"""
        result = calculator("invalid_expression")
        assert "Error" in result
