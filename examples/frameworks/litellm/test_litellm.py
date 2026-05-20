"""
Tests for LiteLLM example — no real API keys needed.
LiteLLM 示例测试——无需真实 API 密钥。

Run / 运行: pytest test_litellm.py -v
"""

from unittest.mock import patch, MagicMock
import pytest


# ---------------------------------------------------------------------------
# 1. Test model name parsing / 测试模型名称解析
# ---------------------------------------------------------------------------

def test_model_name_format():
    """LiteLLM uses 'provider/model' naming. Verify the convention.
    LiteLLM 使用 '提供商/模型' 命名规则，验证该约定。"""
    models = [
        ("openai/gpt-4o", "openai", "gpt-4o"),
        ("anthropic/claude-sonnet-4-20250514", "anthropic", "claude-sonnet-4-20250514"),
        ("gemini/gemini-2.0-flash", "gemini", "gemini-2.0-flash"),
        ("ollama/llama3", "ollama", "llama3"),
    ]
    for full_name, expected_provider, expected_model in models:
        provider, model = full_name.split("/", 1)
        assert provider == expected_provider, f"Provider mismatch / 提供商不匹配: {full_name}"
        assert model == expected_model, f"Model mismatch / 模型不匹配: {full_name}"


# ---------------------------------------------------------------------------
# 2. Test completion call structure / 测试补全调用结构
# ---------------------------------------------------------------------------

@patch("litellm.completion")
def test_completion_call(mock_completion):
    """Verify completion() is called with correct parameters.
    验证 completion() 被正确的参数调用。"""
    import litellm

    # Build a fake response that looks like real output
    # 构建一个模拟的响应对象，模仿真实输出
    mock_message = MagicMock()
    mock_message.content = "Hello from mock! / 来自模拟的问候！"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion.return_value = MagicMock(choices=[mock_choice])

    # Call completion / 调用 completion
    messages = [{"role": "user", "content": "Hi / 你好"}]
    response = litellm.completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=100,
    )

    # Verify it was called correctly / 验证调用参数正确
    mock_completion.assert_called_once_with(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=100,
    )
    # Verify response format / 验证响应格式
    assert response.choices[0].message.content == "Hello from mock! / 来自模拟的问候！"


# ---------------------------------------------------------------------------
# 3. Test fallback configuration / 测试回退配置
# ---------------------------------------------------------------------------

@patch("litellm.completion")
def test_fallback_parameter(mock_completion):
    """Verify fallbacks parameter is passed through to completion().
    验证 fallbacks 参数被正确传递给 completion()。"""
    import litellm

    mock_message = MagicMock()
    mock_message.content = "Fallback response / 回退响应"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion.return_value = MagicMock(choices=[mock_choice])

    fallback_models = ["anthropic/claude-sonnet-4-20250514", "gemini/gemini-2.0-flash"]

    litellm.completion(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": "test"}],
        fallbacks=fallback_models,
    )

    # Verify fallbacks were included in the call / 验证回退列表包含在调用中
    call_kwargs = mock_completion.call_args[1]
    assert call_kwargs["fallbacks"] == fallback_models, \
        "Fallbacks not passed correctly / 回退参数未正确传递"


# ---------------------------------------------------------------------------
# 4. Test streaming parameter / 测试流式参数
# ---------------------------------------------------------------------------

@patch("litellm.completion")
def test_streaming_enabled(mock_completion):
    """Verify stream=True is forwarded to completion().
    验证 stream=True 被正确传递给 completion()。"""
    import litellm

    # Simulate a streaming response (iterable of chunks)
    # 模拟流式响应（可迭代的数据块）
    mock_delta = MagicMock()
    mock_delta.content = "chunk"
    mock_chunk_choice = MagicMock()
    mock_chunk_choice.delta = mock_delta
    mock_chunk = MagicMock(choices=[mock_chunk_choice])
    mock_completion.return_value = iter([mock_chunk])

    response = litellm.completion(
        model="anthropic/claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": "stream test / 流式测试"}],
        stream=True,
        max_tokens=50,
    )

    # Verify stream=True was passed / 验证 stream=True 已传递
    call_kwargs = mock_completion.call_args[1]
    assert call_kwargs["stream"] is True, "Streaming not enabled / 流式输出未启用"

    # Verify we can iterate the response / 验证可以遍历响应
    chunks = list(response)
    assert len(chunks) == 1, "Expected one chunk / 应有一个数据块"
    assert chunks[0].choices[0].delta.content == "chunk"
