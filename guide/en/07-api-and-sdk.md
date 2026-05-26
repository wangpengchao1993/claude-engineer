# Claude API & SDK

> Build applications powered by Claude — from simple chat to tool-using agents with streaming responses.

## Table of Contents

- [Getting Started](#getting-started)
- [Messages API](#messages-api)
- [Tool Use (Function Calling)](#tool-use-function-calling)
- [Streaming](#streaming)
- [Multimodal (Vision)](#multimodal-vision)
- [Extended Thinking](#extended-thinking)
- [System Prompts](#system-prompts)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Getting Started

### Installation

```bash
# Python
pip install anthropic

# TypeScript / Node.js
npm install @anthropic-ai/sdk
```

### Authentication

```python
import anthropic

# Option 1: Environment variable (recommended)
# export ANTHROPIC_API_KEY=sk-ant-api03-...
client = anthropic.Anthropic()

# Option 2: Explicit key
client = anthropic.Anthropic(api_key="sk-ant-api03-...")
```

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // Uses ANTHROPIC_API_KEY env var
```

### Your First API Call

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)
print(response.content[0].text)  # "The capital of France is Paris."
```

---

## Messages API

### Basic Conversation

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Write a Python function to check if a number is prime"},
    ]
)
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "user", "content": "What's the Fibonacci sequence?"},
    {"role": "assistant", "content": "The Fibonacci sequence is a series where each number is the sum of the two preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, 21, ..."},
    {"role": "user", "content": "Write a Python function to compute the nth Fibonacci number efficiently"},
]

response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=messages
)
```

### Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | required | Model ID to use |
| `max_tokens` | int | required | Maximum tokens in response |
| `messages` | array | required | Conversation messages |
| `system` | string | optional | System prompt |
| `temperature` | float | 1.0 | Randomness (0.0 = deterministic, 1.0 = creative) |
| `top_p` | float | — | Nucleus sampling threshold |
| `stop_sequences` | array | — | Stop generating at these strings |
| `stream` | bool | false | Enable streaming |

### Available Models

| Model | ID | Context | Strengths |
|-------|-------|---------|-----------|
| Opus 4.6 | `claude-opus-4-6` | 1M tokens | Most capable, complex reasoning |
| Sonnet 4.6 | `claude-sonnet-4-6-20250514` | 200K tokens | Balanced speed/quality |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K tokens | Fastest, lightweight tasks |

---

## Tool Use (Function Calling)

Tool use lets Claude call functions you define — enabling it to interact with databases, APIs, and external systems.

### Defining Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a given location. Use this when a user asks about weather conditions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state/country, e.g. 'San Francisco, CA'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]
```

### Handling Tool Calls

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your actual implementation
    return {"temperature": 22, "condition": "sunny", "location": location}

# Step 1: Send message with tools
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)

# Step 2: Check if Claude wants to use a tool
if response.stop_reason == "tool_use":
    # Find the tool use block
    tool_use = next(b for b in response.content if b.type == "tool_use")

    # Execute the tool
    result = get_weather(**tool_use.input)

    # Step 3: Send the result back to Claude
    follow_up = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Tokyo?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result)
                }]
            }
        ]
    )
    print(follow_up.content[0].text)
```

### Agentic Tool Use Loop

For agents that may need multiple tool calls:

```python
def run_agent(user_message: str, tools: list, max_iterations: int = 10) -> str:
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # If Claude is done (no more tool calls), return the text
        if response.stop_reason == "end_turn":
            return next(
                (b.text for b in response.content if hasattr(b, "text")),
                ""
            )

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

        messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached"
```

### Tool Choice

Control how Claude uses tools:

```python
# Let Claude decide (default)
tool_choice = {"type": "auto"}

# Force Claude to use a specific tool
tool_choice = {"type": "tool", "name": "get_weather"}

# Force Claude to use any tool (must use one)
tool_choice = {"type": "any"}
```

---

## Streaming

Get responses token-by-token for real-time UIs:

### Python Streaming

```python
# Simple streaming
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story about a robot"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### TypeScript Streaming

```typescript
const stream = await client.messages.stream({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a story about a robot" }],
});

for await (const event of stream) {
  if (
    event.type === "content_block_delta" &&
    event.delta.type === "text_delta"
  ) {
    process.stdout.write(event.delta.text);
  }
}
```

### Streaming with Tool Use

```python
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"Calling tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if hasattr(event.delta, "text"):
                print(event.delta.text, end="")
```

---

## Multimodal (Vision)

Claude can analyze images and PDFs:

### Image Analysis

```python
import base64

# From file
with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": "Describe what you see in this image."
            }
        ]
    }]
)
```

### Image from URL

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/image.png"
                }
            },
            {"type": "text", "text": "What's in this image?"}
        ]
    }]
)
```

### Supported Formats

| Format | MIME Type |
|--------|-----------|
| JPEG | `image/jpeg` |
| PNG | `image/png` |
| GIF | `image/gif` |
| WebP | `image/webp` |
| PDF | `application/pdf` |

---

## Extended Thinking

Let Claude reason deeply before responding — ideal for complex problems:

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Tokens allocated for internal reasoning
    },
    messages=[{
        "role": "user",
        "content": "Design a distributed rate limiter that works across multiple server instances."
    }]
)

# Access thinking and response separately
for block in response.content:
    if block.type == "thinking":
        print("Thinking:", block.thinking)
    elif block.type == "text":
        print("Response:", block.text)
```

### When to Use Extended Thinking

| Task | Extended Thinking? |
|------|-------------------|
| Simple Q&A | No |
| Code generation | Sometimes |
| Complex architecture design | Yes |
| Debugging tricky issues | Yes |
| Mathematical reasoning | Yes |
| Multi-step planning | Yes |

---

## System Prompts

Set persistent behavior across the conversation:

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="You are a senior Python developer. Write clean, type-annotated, well-tested code. Use Python 3.12+ features. Prefer functional patterns.",
    messages=[{"role": "user", "content": "Write a URL shortener service"}]
)
```

### Multi-Part System Prompt

```python
system = [
    {"type": "text", "text": "You are a helpful coding assistant."},
    {"type": "text", "text": "Always respond in the user's language."},
    {"type": "text", "text": "Format code with proper indentation."},
]
```

---

## Error Handling

```python
from anthropic import (
    APIError,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
)
import time

def call_claude_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-6-20250514",
                max_tokens=1024,
                messages=messages
            )
        except RateLimitError:
            wait = 2 ** attempt  # Exponential backoff
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
        except APIConnectionError:
            print("Connection error, retrying...")
            time.sleep(1)
        except AuthenticationError:
            print("Invalid API key!")
            raise
        except APIError as e:
            print(f"API error: {e.status_code} - {e.message}")
            raise
    raise RuntimeError("Max retries exceeded")
```

---

## Best Practices

### 1. Choose the Right Model

- **Opus 4.6**: Complex multi-step tasks, nuanced reasoning
- **Sonnet 4.6**: Best balance for most applications
- **Haiku 4.5**: High-volume, simple tasks (classification, extraction)

### 2. Optimize Token Usage

```python
# Be concise in system prompts
# Bad: 500-word system prompt for simple tasks
# Good: Focus on essentials

# Set appropriate max_tokens
# Don't set max_tokens=100000 when you expect a 100-token response
```

### 3. Write Good Tool Descriptions

```python
# Bad
{"name": "search", "description": "Search"}

# Good
{
    "name": "search_products",
    "description": "Search the product catalog by name, category, or price range. Returns up to 20 matching products sorted by relevance. Use this when the user wants to find or browse products."
}
```

### 4. Handle Context Windows

```python
# Count tokens before sending (approximate)
import tiktoken  # or use anthropic's token counter

# For long conversations, summarize older messages
# or implement a sliding window
```

### 5. Use Structured Output

Guide Claude to return structured data:

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="Always respond with valid JSON. No markdown, no explanation, just JSON.",
    messages=[{
        "role": "user",
        "content": "Extract name, email, and company from: 'Hi, I'm Alice at alice@acme.com, working at Acme Corp'"
    }]
)
# Parse: {"name": "Alice", "email": "alice@acme.com", "company": "Acme Corp"}
```

---

<p align="center">
  <strong>Next:</strong> <a href="08-agent-sdk.md">Agent SDK</a> — Build custom agents
</p>

---

[← Previous: Multi-Agent Patterns](06-multi-agent.md) | [Table of Contents](../../README.md) | [Next: Agent SDK →](08-agent-sdk.md)
