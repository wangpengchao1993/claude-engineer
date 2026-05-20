"""
LiteLLM Multi-Provider Example / LiteLLM 多提供商示例

Call different LLM providers (OpenAI, Anthropic, Gemini) with the SAME code.
用同一套代码调用不同的大模型提供商（OpenAI、Anthropic、Gemini）。

Setup / 准备:
    pip install litellm
    export OPENAI_API_KEY="sk-..."
    export ANTHROPIC_API_KEY="sk-ant-..."
    export GEMINI_API_KEY="..."
"""

import litellm

# ---------------------------------------------------------------------------
# 1. Basic completion — same function, different models
#    基础调用——同一个函数，不同的模型
# ---------------------------------------------------------------------------

def ask_model(model: str, question: str) -> str:
    """Send a question to any model using the unified completion() call.
    使用统一的 completion() 调用向任意模型发送问题。"""
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=200,          # Limit response length / 限制回复长度
        temperature=0.7,         # Creativity level / 创造力级别
    )
    # Response is always in OpenAI format, regardless of provider
    # 不论提供商是谁，响应始终为 OpenAI 格式
    return response.choices[0].message.content


def compare_models():
    """Call multiple providers with identical code — the core value of LiteLLM.
    用完全相同的代码调用多个提供商——这就是 LiteLLM 的核心价值。"""
    question = "Explain what an API is in one sentence. / 用一句话解释什么是 API。"

    models = [
        "openai/gpt-4o",                    # OpenAI
        "anthropic/claude-sonnet-4-20250514",  # Anthropic
        "gemini/gemini-2.0-flash",           # Google Gemini
    ]

    print("=== Comparing Models / 对比模型 ===\n")
    for model in models:
        print(f"Model 模型: {model}")
        answer = ask_model(model, question)
        print(f"Answer 回答: {answer}\n")


# ---------------------------------------------------------------------------
# 2. Streaming — same interface for every provider
#    流式输出——每个提供商都用同一个接口
# ---------------------------------------------------------------------------

def stream_response(model: str, prompt: str):
    """Stream tokens from any provider using the same code.
    用同一套代码从任意提供商流式获取 token。"""
    print(f"Streaming from / 正在流式获取: {model}")

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,             # Enable streaming / 启用流式输出
        max_tokens=100,
    )

    # Iterate over chunks — works the same for all providers
    # 遍历数据块——所有提供商的用法完全相同
    for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            print(text, end="", flush=True)
    print("\n")


# ---------------------------------------------------------------------------
# 3. Fallbacks — if one model fails, try the next
#    回退机制——如果一个模型失败，自动尝试下一个
# ---------------------------------------------------------------------------

def call_with_fallback(prompt: str) -> str:
    """Use fallbacks so your app stays up even if a provider goes down.
    使用回退机制，即使某个提供商宕机，你的应用也能继续运行。"""
    response = litellm.completion(
        model="openai/gpt-4o",                  # Primary model / 主模型
        messages=[{"role": "user", "content": prompt}],
        fallbacks=[                              # Backup models / 备用模型
            "anthropic/claude-sonnet-4-20250514",
            "gemini/gemini-2.0-flash",
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 4. Cost tracking — know what each call costs
#    成本追踪——了解每次调用的花费
# ---------------------------------------------------------------------------

def track_cost(model: str, prompt: str):
    """LiteLLM can calculate the cost of each API call.
    LiteLLM 可以计算每次 API 调用的费用。"""
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )

    # Calculate cost from token usage / 根据 token 用量计算费用
    cost = litellm.completion_cost(completion_response=response)
    print(f"Model 模型: {model}")
    print(f"Cost 费用: ${cost:.6f}")
    print(f"Tokens used / 使用的 token: {response.usage.total_tokens}\n")


# ---------------------------------------------------------------------------
# Main — run all demos / 运行所有示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("LiteLLM Multi-Provider Demo / LiteLLM 多提供商演示")
    print("=" * 60, "\n")

    # 1. Compare models / 对比模型
    compare_models()

    # 2. Streaming / 流式输出
    stream_response("openai/gpt-4o", "Count from 1 to 5. / 从 1 数到 5。")

    # 3. Fallback / 回退
    print("=== Fallback Demo / 回退演示 ===")
    answer = call_with_fallback("What is Python? / 什么是 Python？")
    print(f"Answer 回答: {answer}\n")

    # 4. Cost tracking / 成本追踪
    print("=== Cost Tracking / 成本追踪 ===")
    track_cost("openai/gpt-4o", "Say hello. / 说你好。")
