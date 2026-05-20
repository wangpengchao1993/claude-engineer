# LiteLLM — One API for 100+ LLM Providers / 一套接口调用 100+ 大模型

| Property | Value |
|----------|-------|
| **Language** | Python |
| **License** | MIT |
| **GitHub** | [BerriAI/litellm](https://github.com/BerriAI/litellm) |
| **Docs** | [docs.litellm.ai](https://docs.litellm.ai/) |

---

## What is LiteLLM? / 什么是 LiteLLM？

LiteLLM is a **unified Python interface** that lets you call any LLM — OpenAI,
Anthropic, Google Gemini, local Ollama models, and 100+ more — with the **same
code**. Think of it as a **universal remote control for AI models**: one API,
any model.

LiteLLM 是一个**统一的 Python 接口**，让你用**同一套代码**调用任何大语言模型——
OpenAI、Anthropic、Google Gemini、本地 Ollama 模型以及 100 多个其他提供商。
可以把它想象成**AI 模型的万能遥控器**：一个接口，任意模型。

```python
# Same function, different models — 同一个函数，不同的模型
import litellm

# OpenAI
litellm.completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hi"}])

# Anthropic
litellm.completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hi"}])

# Google Gemini
litellm.completion(model="gemini/gemini-2.0-flash", messages=[{"role": "user", "content": "Hi"}])
```

---

## When to Use LiteLLM / 什么时候用 LiteLLM

**Good fit / 适合使用：**

- **Comparing models** — test the same prompt across providers to find the best
  fit. 对比模型——用同一个提示词测试不同提供商，找到最合适的模型。
- **Switching providers** — swap models without rewriting code.
  切换提供商——换模型不用改代码。
- **Cost optimization** — route requests to cheaper models when quality allows.
  成本优化——在质量允许时将请求路由到更便宜的模型。
- **Building model-agnostic apps** — let users choose their own provider.
  构建模型无关的应用——让用户自己选择提供商。

**Not ideal / 不太适合：**

- **Single-provider apps** — if you only ever use one provider, the direct SDK
  is simpler. 只用一个提供商的应用——直接用官方 SDK 更简单。
- **Provider-specific features** — some advanced features (like Anthropic's
  computer use) need the native SDK.
  需要提供商专属功能——某些高级功能（如 Anthropic 的计算机使用）需要原生 SDK。
- **Low-level optimization** — if you need fine-grained control over HTTP
  connections or custom retry logic.
  底层优化——如果需要精细控制 HTTP 连接或自定义重试逻辑。

---

## Core Concepts / 核心概念

### 1. `completion()` — The Unified Call / 统一调用

Every model is called through **one function**: `litellm.completion()`. It
accepts the OpenAI chat-completion format and translates it for each provider.

所有模型都通过**一个函数**调用：`litellm.completion()`。它接受 OpenAI 聊天补全格式，
并为每个提供商进行转换。

### 2. Model Naming Convention / 模型命名规则

Models follow the `provider/model-name` pattern:

模型遵循 `提供商/模型名` 的格式：

```
openai/gpt-4o
anthropic/claude-sonnet-4-20250514
gemini/gemini-2.0-flash
ollama/llama3
```

### 3. Fallbacks / 回退机制

If one model fails, LiteLLM can automatically try another:

如果一个模型失败，LiteLLM 可以自动尝试另一个：

```python
response = litellm.completion(
    model="openai/gpt-4o",
    messages=messages,
    fallbacks=["anthropic/claude-sonnet-4-20250514", "gemini/gemini-2.0-flash"],
)
```

### 4. Router / 路由器

For production use, the `Router` distributes requests across multiple models
with load balancing, rate-limit handling, and retries.

在生产环境中，`Router` 可以将请求分发到多个模型，支持负载均衡、速率限制处理和重试。

---

## Supported Providers / 支持的提供商

| Prefix 前缀 | Provider 提供商 | Example Model 示例模型 |
|---|---|---|
| `openai/` | OpenAI | `openai/gpt-4o` |
| `anthropic/` | Anthropic | `anthropic/claude-sonnet-4-20250514` |
| `gemini/` | Google Gemini | `gemini/gemini-2.0-flash` |
| `ollama/` | Ollama (local) | `ollama/llama3` |
| `azure/` | Azure OpenAI | `azure/gpt-4o` |
| `bedrock/` | AWS Bedrock | `bedrock/anthropic.claude-3-sonnet` |
| `vertex_ai/` | Google Vertex AI | `vertex_ai/gemini-pro` |
| `huggingface/` | Hugging Face | `huggingface/meta-llama/Llama-3` |
| `cohere/` | Cohere | `cohere/command-r-plus` |
| `mistral/` | Mistral AI | `mistral/mistral-large-latest` |

Full list: [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)

完整列表见上方链接。

---

## Quick Start / 快速开始

```bash
# Install / 安装
pip install litellm

# Set API keys (use the providers you need) / 设置 API 密钥（按需设置）
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Run the example / 运行示例
python multi_provider.py
```

---

## How It Works / 工作原理

```
Your Code             LiteLLM                   Provider API
你的代码               LiteLLM                   提供商 API
─────────────────────────────────────────────────────────────
                      ┌─────────────────────┐
litellm.completion()  │ 1. Parse model name  │
  model="anthropic/   │    解析模型名称        │
   claude-sonnet-4-20250514"   │ 2. Translate params  │──► Anthropic API
  messages=[...]      │    转换参数格式        │
                      │ 3. Return OpenAI     │◄── Provider response
                      │    format response   │    提供商响应
                      │    返回 OpenAI 格式   │
                      └─────────────────────┘
```

**Key insight / 关键点:** No matter which provider you call, the response
always comes back in the **same OpenAI-compatible format**. This means your
downstream code never needs to change.

无论调用哪个提供商，响应始终以**相同的 OpenAI 兼容格式**返回。这意味着你的下游代码
永远不需要改变。

---

## Comparison with Direct API Calls / 与直接 API 调用的对比

| | Direct SDK 直接 SDK | LiteLLM |
|---|---|---|
| **Code per provider** 每个提供商的代码 | Different SDK + format 不同的 SDK 和格式 | Same `completion()` call 同一个调用 |
| **Switching models** 切换模型 | Rewrite code 重写代码 | Change one string 改一个字符串 |
| **Fallbacks** 回退 | Build yourself 自己实现 | Built-in 内置 |
| **Cost tracking** 成本追踪 | Manual 手动 | `completion_cost()` |
| **Streaming** 流式输出 | Different per provider 每个提供商不同 | Same interface 统一接口 |
| **Overhead** 额外开销 | None 无 | Minimal (~ms) 极小 |

---

## Learn More / 了解更多

- [Official Docs / 官方文档](https://docs.litellm.ai/)
- [GitHub Repository / GitHub 仓库](https://github.com/BerriAI/litellm)
- [Supported Models List / 支持的模型列表](https://docs.litellm.ai/docs/providers)
- [LiteLLM Proxy Server / 代理服务器](https://docs.litellm.ai/docs/simple_proxy)
- [Router Documentation / 路由器文档](https://docs.litellm.ai/docs/routing)

---

## Files in This Example / 本示例文件

| File 文件 | Description 说明 |
|---|---|
| `README.md` | This guide / 本指南 |
| `multi_provider.py` | Call multiple providers with one interface / 用同一接口调用多个提供商 |
| `test_litellm.py` | Tests (no API keys needed) / 测试（无需 API 密钥） |
