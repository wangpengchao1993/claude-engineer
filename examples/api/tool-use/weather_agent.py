"""
Weather Agent — Claude API Tool Use Example
天气代理 - Claude API 工具使用示例

Demonstrates the complete tool-use loop:
演示完整的工具使用循环：
1. Define tools with JSON schemas
   使用 JSON 模式定义工具
2. Send a message with tools available
   发送消息并附带可用工具
3. Handle tool calls from Claude
   处理来自 Claude 的工具调用
4. Return results and get final response
   返回结果并获取最终响应

Usage:
用法：
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python weather_agent.py
"""

import json
import anthropic

# Initialize the Anthropic client
# 初始化 Anthropic 客户端
client = anthropic.Anthropic()

# --- Tool Definitions ---
# --- 工具定义 ---

tools = [
    {
        # get_weather: Get current weather for a location
        # get_weather：获取指定位置的当前天气
        "name": "get_weather",
        "description": "Get the current weather for a specific location. Returns temperature, conditions, and humidity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g. 'Tokyo, Japan' or 'London, UK'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit (default: celsius)"
                }
            },
            "required": ["location"]
        }
    },
    {
        # get_forecast: Get weather forecast for upcoming days
        # get_forecast：获取未来几天的天气预报
        "name": "get_forecast",
        "description": "Get the weather forecast for the next N days.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to forecast (1-7)",
                    "minimum": 1,
                    "maximum": 7
                }
            },
            "required": ["location", "days"]
        }
    }
]

# --- Tool Implementations ---
# --- 工具实现 ---
# In a real app, these would call actual weather APIs
# 在实际应用中，这些函数会调用真实的天气 API

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulate getting current weather.
    模拟获取当前天气。"""
    # Replace with real API call (e.g., OpenWeatherMap)
    # 替换为真实的 API 调用（例如 OpenWeatherMap）
    weather_data = {
        "Tokyo, Japan": {"temp_c": 22, "condition": "Partly cloudy", "humidity": 65},
        "London, UK": {"temp_c": 14, "condition": "Rainy", "humidity": 80},
        "New York, US": {"temp_c": 18, "condition": "Sunny", "humidity": 55},
    }

    # Look up location data, use defaults if not found
    # 查找位置数据，未找到则使用默认值
    data = weather_data.get(location, {"temp_c": 20, "condition": "Clear", "humidity": 50})

    # Convert to Fahrenheit if requested
    # 如果请求华氏温度则进行转换
    if unit == "fahrenheit":
        temp = data["temp_c"] * 9 / 5 + 32
        temp_str = f"{temp:.0f}°F"
    else:
        temp_str = f"{data['temp_c']}°C"

    return {
        "location": location,
        "temperature": temp_str,
        "condition": data["condition"],
        "humidity": f"{data['humidity']}%"
    }


def get_forecast(location: str, days: int) -> dict:
    """Simulate getting weather forecast.
    模拟获取天气预报。"""
    import random
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly cloudy", "Clear"]
    # Generate random forecast for each day
    # 为每一天生成随机预报
    forecast = []
    for i in range(days):
        forecast.append({
            "day": f"Day {i + 1}",
            "high": f"{random.randint(15, 30)}°C",
            "low": f"{random.randint(5, 15)}°C",
            "condition": random.choice(conditions)
        })
    return {"location": location, "forecast": forecast}


# --- Tool Dispatcher ---
# --- 工具分发器 ---

def execute_tool(name: str, input_data: dict) -> str:
    """Route tool calls to implementations.
    将工具调用路由到具体实现。"""
    tool_map = {
        "get_weather": get_weather,
        "get_forecast": get_forecast,
    }

    if name not in tool_map:
        return json.dumps({"error": f"Unknown tool: {name}"})

    # Call the matching tool function with input parameters
    # 使用输入参数调用匹配的工具函数
    result = tool_map[name](**input_data)
    return json.dumps(result)


# --- Agent Loop ---
# --- 代理循环 ---

def run_agent(user_message: str, max_iterations: int = 5) -> str:
    """Run the agent loop: send message → handle tool calls → repeat until done.
    运行代理循环：发送消息 → 处理工具调用 → 重复直到完成。"""

    print(f"\n{'='*60}")
    print(f"User: {user_message}")
    print(f"{'='*60}\n")

    messages = [{"role": "user", "content": user_message}]

    for i in range(max_iterations):
        # Send message to Claude with tools available
        # 将消息发送给 Claude，附带可用的工具
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        print(f"--- Iteration {i + 1} | Stop reason: {response.stop_reason} ---")

        # If Claude is done (no tool calls), extract and return text
        # 如果 Claude 完成（无工具调用），提取并返回文本
        if response.stop_reason == "end_turn":
            text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No response text."
            )
            print(f"\nClaude: {text}\n")
            return text

        # Process tool calls
        # 处理工具调用
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                # Execute each tool call and collect results
                # 执行每个工具调用并收集结果
                print(f"  Tool call: {block.name}({json.dumps(block.input)})")
                result = execute_tool(block.name, block.input)
                print(f"  Result: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Send tool results back to Claude as a user message
        # 将工具结果作为用户消息发送回 Claude
        messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached."


# --- Main ---
# --- 主程序 ---

if __name__ == "__main__":
    # Example 1: Simple weather query
    # 示例 1：简单天气查询
    run_agent("What's the weather like in Tokyo right now?")

    # Example 2: Multi-tool query
    # 示例 2：多工具查询
    run_agent("Compare the weather in London and New York, and give me the 3-day forecast for the warmer city.")
