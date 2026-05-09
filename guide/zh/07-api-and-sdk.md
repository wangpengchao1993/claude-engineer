# Claude API 与 SDK

> 用 Claude 构建应用 — 从简单聊天到带工具的 Agent，再到流式响应。

## 目录

- [快速开始](#快速开始)
- [Messages API](#messages-api)
- [Tool Use（函数调用）](#tool-use函数调用)
- [流式响应](#流式响应)
- [多模态（视觉）](#多模态视觉)
- [扩展思考](#扩展思考)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

---

## 快速开始

### 安装

```bash
# Python
pip install anthropic

# TypeScript / Node.js
npm install @anthropic-ai/sdk
```

### 认证

```python
import anthropic

# 方式 1：环境变量（推荐）
# export ANTHROPIC_API_KEY=sk-ant-api03-...
client = anthropic.Anthropic()

# 方式 2：显式传入
client = anthropic.Anthropic(api_key="sk-ant-api03-...")
```

### 第一次 API 调用

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "法国的首都是什么？"}
    ]
)
print(response.content[0].text)
```

---

## Messages API

### 多轮对话

```python
messages = [
    {"role": "user", "content": "什么是斐波那契数列？"},
    {"role": "assistant", "content": "斐波那契数列是一个数列，每个数是前两个数的和：0, 1, 1, 2, 3, 5, 8, 13, 21, ..."},
    {"role": "user", "content": "写一个 Python 函数高效计算第 n 个斐波那契数"},
]

response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=messages
)
```

### 关键参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model` | string | 必填 | 模型 ID |
| `max_tokens` | int | 必填 | 最大输出 Token 数 |
| `messages` | array | 必填 | 对话消息 |
| `system` | string | 可选 | 系统提示 |
| `temperature` | float | 1.0 | 随机性（0.0=确定性，1.0=创造性） |
| `tools` | array | 可选 | 可用工具 |
| `stream` | bool | false | 启用流式输出 |

### 可用模型

| 模型 | ID | 上下文 | 强项 |
|------|------|--------|------|
| Opus 4.6 | `claude-opus-4-6` | 1M tokens | 最强能力，复杂推理 |
| Sonnet 4.6 | `claude-sonnet-4-6-20250514` | 200K tokens | 速度/质量平衡 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K tokens | 最快，轻量任务 |

---

## Tool Use（函数调用）

Tool Use 让 Claude 调用你定义的函数，从而与数据库、API 和外部系统交互。

### 定义工具

```python
tools = [
    {
        "name": "get_weather",
        "description": "获取指定位置的当前天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市和国家，如 '东京, 日本'"
                }
            },
            "required": ["location"]
        }
    }
]
```

### 处理工具调用

```python
import json

# 步骤 1：发送带工具的消息
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "东京天气怎么样？"}]
)

# 步骤 2：检查是否需要调用工具
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = get_weather(**tool_use.input)  # 执行工具

    # 步骤 3：把结果返回给 Claude
    follow_up = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "东京天气怎么样？"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(result)
            }]}
        ]
    )
```

### Agent 循环（多次工具调用）

```python
def run_agent(user_message: str, tools: list, max_iterations: int = 10) -> str:
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096, tools=tools, messages=messages
        )

        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "")

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

    return "达到最大迭代次数"
```

---

## 流式响应

逐 Token 获取响应，适合实时 UI：

```python
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一个关于编程的故事"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### TypeScript 流式

```typescript
const stream = await client.messages.stream({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "写一个故事" }],
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

---

## 多模态（视觉）

Claude 可以分析图片和 PDF：

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {
                "type": "base64", "media_type": "image/png", "data": image_data
            }},
            {"type": "text", "text": "描述你在这张图片中看到了什么。"}
        ]
    }]
)
```

支持格式：JPEG、PNG、GIF、WebP、PDF

---

## 扩展思考

让 Claude 在回答前深入推理 — 适合复杂问题：

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "设计一个分布式限流器"}]
)

for block in response.content:
    if block.type == "thinking":
        print("思考过程:", block.thinking)
    elif block.type == "text":
        print("回答:", block.text)
```

---

## 错误处理

```python
from anthropic import RateLimitError, APIConnectionError, AuthenticationError
import time

def call_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-6-20250514",
                max_tokens=1024, messages=messages
            )
        except RateLimitError:
            time.sleep(2 ** attempt)  # 指数退避
        except APIConnectionError:
            time.sleep(1)
        except AuthenticationError:
            raise  # API 密钥无效，不重试
    raise RuntimeError("超过最大重试次数")
```

---

## 最佳实践

1. **选对模型** — Opus 做复杂任务，Sonnet 做日常开发，Haiku 做批量简单任务
2. **写好工具描述** — 描述清楚工具做什么、什么时候用、什么时候不用
3. **优化 Token** — 不要 `max_tokens=100000` 当你只期望 100 token 的回答
4. **结构化输出** — 引导 Claude 返回 JSON 等结构化数据
5. **重试策略** — 用指数退避处理限流

---

<p align="center">
  <strong>下一篇：</strong> <a href="08-agent-sdk.md">Agent SDK</a> — 构建自定义 Agent
</p>
