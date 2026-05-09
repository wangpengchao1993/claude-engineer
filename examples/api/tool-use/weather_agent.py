"""
Weather Agent — Claude API Tool Use Example

Demonstrates the complete tool-use loop:
1. Define tools with JSON schemas
2. Send a message with tools available
3. Handle tool calls from Claude
4. Return results and get final response

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python weather_agent.py
"""

import json
import anthropic

client = anthropic.Anthropic()

# --- Tool Definitions ---

tools = [
    {
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
# In a real app, these would call actual weather APIs

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulate getting current weather."""
    # Replace with real API call (e.g., OpenWeatherMap)
    weather_data = {
        "Tokyo, Japan": {"temp_c": 22, "condition": "Partly cloudy", "humidity": 65},
        "London, UK": {"temp_c": 14, "condition": "Rainy", "humidity": 80},
        "New York, US": {"temp_c": 18, "condition": "Sunny", "humidity": 55},
    }

    data = weather_data.get(location, {"temp_c": 20, "condition": "Clear", "humidity": 50})

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
    """Simulate getting weather forecast."""
    import random
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly cloudy", "Clear"]
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

def execute_tool(name: str, input_data: dict) -> str:
    """Route tool calls to implementations."""
    tool_map = {
        "get_weather": get_weather,
        "get_forecast": get_forecast,
    }

    if name not in tool_map:
        return json.dumps({"error": f"Unknown tool: {name}"})

    result = tool_map[name](**input_data)
    return json.dumps(result)


# --- Agent Loop ---

def run_agent(user_message: str, max_iterations: int = 5) -> str:
    """Run the agent loop: send message → handle tool calls → repeat until done."""

    print(f"\n{'='*60}")
    print(f"User: {user_message}")
    print(f"{'='*60}\n")

    messages = [{"role": "user", "content": user_message}]

    for i in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        print(f"--- Iteration {i + 1} | Stop reason: {response.stop_reason} ---")

        # If Claude is done (no tool calls), extract and return text
        if response.stop_reason == "end_turn":
            text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No response text."
            )
            print(f"\nClaude: {text}\n")
            return text

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"  Tool call: {block.name}({json.dumps(block.input)})")
                result = execute_tool(block.name, block.input)
                print(f"  Result: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached."


# --- Main ---

if __name__ == "__main__":
    # Example 1: Simple weather query
    run_agent("What's the weather like in Tokyo right now?")

    # Example 2: Multi-tool query
    run_agent("Compare the weather in London and New York, and give me the 3-day forecast for the warmer city.")
