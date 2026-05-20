"""
Local Chat with Ollama / 使用 Ollama 本地对话

This script shows how to chat with a local LLM using the `ollama` Python package.
No API keys needed — the model runs entirely on your machine!

本脚本演示如何使用 `ollama` Python 包与本地大模型对话。
无需 API 密钥——模型完全在你的电脑上运行！

Prerequisites / 前提条件:
    1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh
       安装 Ollama
    2. Pull a model: ollama pull llama3.2
       下载模型
    3. Install Python package: pip install ollama
       安装 Python 包

Usage / 用法:
    python local_chat.py
"""

import ollama


# === 1. Basic Chat / 基础对话 ===
def basic_chat():
    """Send a single message and get a response / 发送一条消息并获取回复"""
    print("=== Basic Chat / 基础对话 ===\n")

    # ollama.chat() sends messages to the local model / 向本地模型发送消息
    # It works just like the OpenAI API format / 格式与 OpenAI API 类似
    response = ollama.chat(
        model="llama3.2",               # Which model to use / 使用哪个模型
        messages=[
            {"role": "user", "content": "What is Python in one sentence?"}
        ],
    )

    # The response contains the model's reply / 返回值包含模型的回复
    print(response["message"]["content"])
    print()


# === 2. Streaming Response / 流式响应 ===
def streaming_chat():
    """Stream the response token by token / 逐词流式输出回复"""
    print("=== Streaming Chat / 流式对话 ===\n")

    # stream=True returns tokens one at a time (like ChatGPT's typing effect)
    # stream=True 逐词返回（像 ChatGPT 的打字效果）
    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": "Count from 1 to 5 with fun facts."}
        ],
        stream=True,                     # Enable streaming / 启用流式输出
    )

    # Print each chunk as it arrives / 逐块打印
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print("\n")


# === 3. Multi-turn Conversation / 多轮对话 ===
def multi_turn_chat():
    """Have a back-and-forth conversation with history / 带历史记录的多轮对话"""
    print("=== Multi-turn Chat / 多轮对话 ===\n")

    # Keep a list of messages — this IS the conversation history
    # 维护一个消息列表——这就是对话历史
    history = [
        # System prompt sets the model's personality / system 提示词设定模型角色
        {"role": "system", "content": "You are a helpful cooking assistant. Answer briefly."},
        {"role": "user", "content": "What's an easy pasta recipe?"},
    ]

    # First turn / 第一轮
    response = ollama.chat(model="llama3.2", messages=history)
    assistant_msg = response["message"]["content"]
    print(f"User: What's an easy pasta recipe?")
    print(f"AI: {assistant_msg}\n")

    # Add the assistant's reply to history / 将助手的回复加入历史
    history.append({"role": "assistant", "content": assistant_msg})

    # Second turn — the model remembers the previous exchange
    # 第二轮——模型记住了之前的对话
    history.append({"role": "user", "content": "How do I make it spicy?"})
    response = ollama.chat(model="llama3.2", messages=history)
    print(f"User: How do I make it spicy?")
    print(f"AI: {response['message']['content']}\n")


# === 4. List Local Models / 列出本地模型 ===
def list_models():
    """Show all models downloaded on this machine / 显示本机已下载的所有模型"""
    print("=== Local Models / 本地模型 ===\n")

    models = ollama.list()
    for model in models.get("models", []):
        name = model.get("name", "unknown")
        size_gb = model.get("size", 0) / (1024 ** 3)  # bytes → GB
        print(f"  - {name} ({size_gb:.1f} GB)")
    print()


# === Run all examples / 运行所有示例 ===
if __name__ == "__main__":
    print("Make sure Ollama is running: ollama serve")
    print("确保 Ollama 正在运行: ollama serve\n")

    basic_chat()
    streaming_chat()
    multi_turn_chat()
    list_models()
