"""
Tests for Ollama Examples / Ollama 示例测试

All tests run WITHOUT a real Ollama server — we mock the ollama client.
所有测试无需真实 Ollama 服务器运行——我们使用 mock 模拟 ollama 客户端。

Usage / 用法:
    pip install pytest ollama
    pytest test_ollama.py -v
"""

from unittest.mock import patch, MagicMock


# --- Test 1: Chat message formatting / 测试聊天消息格式 ---
def test_chat_message_format():
    """Verify messages follow the role/content format / 验证消息遵循 role/content 格式"""
    messages = [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello"},
    ]
    # Every message must have 'role' and 'content' keys / 每条消息必须有 role 和 content
    for msg in messages:
        assert "role" in msg, "Message must have 'role' / 消息必须包含 'role'"
        assert "content" in msg, "Message must have 'content' / 消息必须包含 'content'"
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


# --- Test 2: Streaming configuration / 测试流式配置 ---
@patch("ollama.chat")
def test_streaming_passes_flag(mock_chat):
    """Verify stream=True is passed to ollama.chat / 验证 stream=True 传递给 ollama.chat"""
    import ollama

    # Configure mock to return an iterable / 配置 mock 返回可迭代对象
    mock_chat.return_value = iter([
        {"message": {"content": "Hello"}},
    ])

    result = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "Hi"}],
        stream=True,
    )

    # Verify chat was called with stream=True / 验证调用时带了 stream=True
    mock_chat.assert_called_once_with(
        model="llama3.2",
        messages=[{"role": "user", "content": "Hi"}],
        stream=True,
    )


# --- Test 3: Conversation history building / 测试对话历史构建 ---
def test_conversation_history_building():
    """Verify multi-turn history accumulates correctly / 验证多轮对话历史正确累积"""
    history = [
        {"role": "system", "content": "You are a chef."},
        {"role": "user", "content": "What is sushi?"},
    ]

    # Simulate assistant reply / 模拟助手回复
    assistant_reply = "Sushi is a Japanese dish with vinegared rice."
    history.append({"role": "assistant", "content": assistant_reply})

    # Add follow-up question / 添加追问
    history.append({"role": "user", "content": "How do I make it?"})

    assert len(history) == 4, "Should have 4 messages / 应该有 4 条消息"
    assert history[0]["role"] == "system"
    assert history[2]["role"] == "assistant"
    assert history[3]["role"] == "user"


# --- Test 4: Mock ollama.chat response / 测试模拟 ollama.chat 响应 ---
@patch("ollama.chat")
def test_basic_chat_response(mock_chat):
    """Mock a full chat round-trip / 模拟一次完整的对话往返"""
    import ollama

    # Set up mock return value (same shape as real response)
    # 设置 mock 返回值（与真实响应结构相同）
    mock_chat.return_value = {
        "message": {"role": "assistant", "content": "Python is a programming language."},
        "model": "llama3.2",
    }

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "What is Python?"}],
    )

    assert response["message"]["role"] == "assistant"
    assert "Python" in response["message"]["content"]
    assert response["model"] == "llama3.2"
