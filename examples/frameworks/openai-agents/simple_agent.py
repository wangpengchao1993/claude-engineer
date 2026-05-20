"""
OpenAI Agents SDK — Simple Agent Example
OpenAI Agents SDK — 简单智能体示例

This example shows how to:
本示例展示如何：
  1. Define function tools / 定义函数工具
  2. Create agents with instructions / 创建带指令的智能体
  3. Use Runner to execute / 使用 Runner 执行
  4. Set up multi-agent handoff / 设置多智能体交接

Install first / 先安装:
    pip install openai-agents
"""

from agents import Agent, Runner, function_tool

# =============================================================================
# Step 1: Define Tools / 第一步：定义工具
# Tools are just Python functions decorated with @function_tool
# 工具就是用 @function_tool 装饰的普通 Python 函数
# =============================================================================


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. / 获取城市的当前天气。"""
    # In a real app, you'd call a weather API here
    # 在真实应用中，你会在这里调用天气 API
    weather_data = {
        "Tokyo": "22C, sunny / 22度，晴天",
        "London": "15C, rainy / 15度，下雨",
        "New York": "28C, cloudy / 28度，多云",
    }
    return weather_data.get(city, f"No data for {city} / 没有 {city} 的数据")


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. / 计算数学表达式。"""
    try:
        # WARNING: eval() is unsafe in production! Use a proper math parser.
        # 警告：eval() 在生产环境中不安全！请使用专用的数学解析器。
        result = eval(expression, {"__builtins__": {}})
        return f"Result / 结果: {result}"
    except Exception as e:
        return f"Error / 错误: {e}"


# =============================================================================
# Step 2: Define Agents / 第二步：定义智能体
# An Agent has a name, instructions (system prompt), and tools
# Agent 有名称、指令（系统提示词）和工具
# =============================================================================

# Specialist agent: handles weather questions
# 专家智能体：处理天气问题
weather_agent = Agent(
    name="Weather Agent / 天气智能体",
    instructions=(
        "You are a weather assistant. Use the get_weather tool to answer "
        "weather questions. Be friendly and concise."
        # 你是一个天气助手。使用 get_weather 工具回答天气问题。友好简洁。
    ),
    tools=[get_weather],
)

# Specialist agent: handles math questions
# 专家智能体：处理数学问题
math_agent = Agent(
    name="Math Agent / 数学智能体",
    instructions=(
        "You are a math assistant. Use the calculate tool to solve math "
        "problems. Show your work step by step."
        # 你是一个数学助手。使用 calculate 工具解决数学问题。逐步展示过程。
    ),
    tools=[calculate],
)

# Triage agent: decides which specialist to hand off to
# 分诊智能体：决定交接给哪个专家
# This is the "router" — it doesn't do the work itself, it delegates.
# 这是"路由器" — 它自己不做工作，而是委托给别人。
triage_agent = Agent(
    name="Triage Agent / 分诊智能体",
    instructions=(
        "You are a helpful triage agent. "
        "If the user asks about weather, hand off to the Weather Agent. "
        "If the user asks about math, hand off to the Math Agent. "
        "For other questions, answer directly."
        # 你是一个分诊智能体。
        # 如果用户问天气，交接给天气智能体。
        # 如果用户问数学，交接给数学智能体。
        # 其他问题直接回答。
    ),
    handoffs=[weather_agent, math_agent],
)


# =============================================================================
# Step 3: Run the Agent / 第三步：运行智能体
# Runner.run_sync() is the simplest way to run an agent
# Runner.run_sync() 是运行智能体的最简单方式
# =============================================================================


def main():
    """Run the triage agent with a sample query. / 用示例问题运行分诊智能体。"""

    print("=" * 60)
    print("OpenAI Agents SDK — Multi-Agent Handoff Demo")
    print("OpenAI Agents SDK — 多智能体交接演示")
    print("=" * 60)

    # Example queries to try / 可以尝试的示例问题
    queries = [
        "What's the weather in Tokyo?",       # -> Weather Agent / 天气智能体
        "What is 42 * 17 + 3?",               # -> Math Agent / 数学智能体
        "Hello, who are you?",                 # -> Triage answers directly / 分诊直接回答
    ]

    for query in queries:
        print(f"\nUser / 用户: {query}")

        # Run the agent synchronously / 同步运行智能体
        # For async, use: result = await Runner.run(triage_agent, query)
        # 异步方式: result = await Runner.run(triage_agent, query)
        result = Runner.run_sync(triage_agent, query)

        print(f"Agent / 智能体: {result.final_output}")
        print("-" * 40)


if __name__ == "__main__":
    main()
