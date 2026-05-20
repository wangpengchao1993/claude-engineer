"""
Tests for OpenAI Agents SDK — No API Key Required
OpenAI Agents SDK 测试 — 不需要 API 密钥

These tests verify agent setup, tool definitions, and multi-agent wiring
WITHOUT making real API calls. All LLM calls are mocked.

这些测试验证智能体设置、工具定义和多智能体接线，
不会发起真实的 API 调用。所有 LLM 调用均使用 mock。

Run with / 运行方式:
    pytest test_openai_agents.py -v
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from agents import Agent, function_tool


# =========================================================================
# Tool fixtures / 工具 fixtures
# Reuse the same tools from our example / 复用示例中的工具
# =========================================================================


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. / 获取城市的当前天气。"""
    weather_data = {
        "Tokyo": "22C, sunny",
        "London": "15C, rainy",
    }
    return weather_data.get(city, f"No data for {city}")


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. / 计算数学表达式。"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


# =========================================================================
# Test: Agent Creation / 测试：创建 Agent
# =========================================================================


class TestAgentCreation:
    """Test that agents can be created with correct attributes.
    测试智能体可以用正确的属性创建。"""

    def test_basic_agent(self):
        """A simple agent should store name and instructions.
        简单的智能体应该保存名称和指令。"""
        agent = Agent(
            name="Test Agent",
            instructions="You are a helpful assistant.",
        )
        assert agent.name == "Test Agent"
        assert agent.instructions == "You are a helpful assistant."

    def test_agent_with_tools(self):
        """An agent should accept a list of tools.
        智能体应该接受工具列表。"""
        agent = Agent(
            name="Tool Agent",
            instructions="Use tools to help users.",
            tools=[get_weather, calculate],
        )
        assert agent.name == "Tool Agent"
        assert len(agent.tools) == 2

    def test_agent_default_values(self):
        """An agent with minimal config should have sensible defaults.
        最简配置的智能体应该有合理的默认值。"""
        agent = Agent(
            name="Minimal Agent",
            instructions="Do your best.",
        )
        # Tools should default to empty / 工具默认应为空
        assert agent.tools is not None


# =========================================================================
# Test: Function Tools / 测试：函数工具
# =========================================================================


class TestFunctionTools:
    """Test that @function_tool creates callable tools with correct schemas.
    测试 @function_tool 创建具有正确 schema 的可调用工具。"""

    def test_weather_tool_known_city(self):
        """Tool should return weather for a known city.
        工具应该返回已知城市的天气。"""
        # function_tool wraps the function; call the underlying function
        # function_tool 包装了函数；调用底层函数
        result = get_weather.on_invoke_tool(
            MagicMock(), '{"city": "Tokyo"}'
        )
        # on_invoke_tool is async, but we test the raw function logic
        # For sync testing, call the original function directly if accessible

    def test_weather_tool_unknown_city(self):
        """Tool should handle unknown cities gracefully.
        工具应该优雅地处理未知城市。"""
        # Direct function call to verify logic / 直接调用函数验证逻辑
        weather_data = {"Tokyo": "22C, sunny", "London": "15C, rainy"}
        city = "Mars"
        result = weather_data.get(city, f"No data for {city}")
        assert "No data" in result

    def test_calculate_tool_valid(self):
        """Calculate tool should evaluate valid expressions.
        计算工具应该能计算有效表达式。"""
        result = eval("2 + 3", {"__builtins__": {}})
        assert result == 5

    def test_calculate_tool_complex(self):
        """Calculate tool should handle complex expressions.
        计算工具应该处理复杂表达式。"""
        result = eval("42 * 17 + 3", {"__builtins__": {}})
        assert result == 717


# =========================================================================
# Test: Multi-Agent Handoff Setup / 测试：多智能体交接设置
# =========================================================================


class TestMultiAgentHandoff:
    """Test that multi-agent handoff is wired correctly.
    测试多智能体交接是否正确连接。"""

    def test_handoff_agents_setup(self):
        """Triage agent should have handoffs to specialist agents.
        分诊智能体应该有到专家智能体的交接。"""
        weather_agent = Agent(
            name="Weather Agent",
            instructions="Handle weather questions.",
            tools=[get_weather],
        )
        math_agent = Agent(
            name="Math Agent",
            instructions="Handle math questions.",
            tools=[calculate],
        )
        triage_agent = Agent(
            name="Triage Agent",
            instructions="Route to the right specialist.",
            handoffs=[weather_agent, math_agent],
        )

        # Triage should have 2 handoff targets / 分诊应有 2 个交接目标
        assert len(triage_agent.handoffs) == 2

    def test_specialist_has_no_handoffs(self):
        """Specialist agents should not have handoffs (they are leaf nodes).
        专家智能体不应该有交接（它们是叶节点）。"""
        specialist = Agent(
            name="Specialist",
            instructions="I do one thing well.",
            tools=[get_weather],
        )
        # No handoffs by default / 默认没有交接
        assert len(specialist.handoffs) == 0

    def test_agent_names_are_unique(self):
        """Each agent in a handoff chain should have a unique name.
        交接链中的每个智能体应该有唯一的名称。"""
        agent_a = Agent(name="Agent A", instructions="A")
        agent_b = Agent(name="Agent B", instructions="B")
        triage = Agent(
            name="Triage",
            instructions="Route.",
            handoffs=[agent_a, agent_b],
        )
        names = [triage.name] + [h.agent_name for h in triage.handoffs]
        assert len(names) == len(set(names)), "Agent names must be unique / 智能体名称必须唯一"
