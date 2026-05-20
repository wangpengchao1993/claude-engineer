"""
Streaming Demo — Claude API Streaming Example
流式演示 - Claude API 流式传输示例

Demonstrates streaming responses for real-time output.
演示流式响应以实现实时输出。

Usage:
用法：
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python stream_demo.py
"""

import anthropic

# Initialize the Anthropic client
# 初始化 Anthropic 客户端
client = anthropic.Anthropic()


def basic_streaming():
    """Stream a simple text response.
    流式传输简单文本响应。"""
    print("=== Basic Streaming ===\n")

    # Open a streaming connection and iterate over text chunks
    # 打开流式连接并逐块迭代文本
    with client.messages.stream(
        model="claude-sonnet-4-6-20250514",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": "Write a haiku about programming, then explain it."
        }]
    ) as stream:
        for text in stream.text_stream:
            # Print each text chunk as it arrives
            # 每个文本块到达时立即打印
            print(text, end="", flush=True)

    print("\n")


def streaming_with_metadata():
    """Stream with event handling for metadata.
    带事件处理的流式传输，用于获取元数据。"""
    print("=== Streaming with Events ===\n")

    with client.messages.stream(
        model="claude-sonnet-4-6-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": "List 3 benefits of TypeScript in one sentence each."
        }]
    ) as stream:
        for event in stream:
            # Handle different event types
            # 处理不同的事件类型
            if event.type == "message_start":
                # Message started — print model info
                # 消息开始 - 打印模型信息
                print(f"[Model: {event.message.model}]")
            elif event.type == "content_block_delta" and hasattr(event.delta, "text"):
                # Content delta — print text as it streams
                # 内容增量 - 流式打印文本
                print(event.delta.text, end="", flush=True)
            elif event.type == "message_stop":
                # Message complete
                # 消息完成
                print("\n[Done]")

    # Access final message for usage stats
    # 获取最终消息以查看使用统计
    message = stream.get_final_message()
    print(f"[Tokens — Input: {message.usage.input_tokens}, Output: {message.usage.output_tokens}]")
    print()


def streaming_with_system_prompt():
    """Stream with a system prompt for controlled output.
    使用系统提示进行流式传输以控制输出。"""
    print("=== Streaming with System Prompt ===\n")

    # Stream with a system prompt to guide Claude's response style
    # 使用系统提示引导 Claude 的响应风格进行流式传输
    with client.messages.stream(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1024,
        system="You are a concise technical writer. Use bullet points and code examples.",
        messages=[{
            "role": "user",
            "content": "Explain Python's `asyncio.gather` with a code example."
        }]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


if __name__ == "__main__":
    # Run all three streaming demos in sequence
    # 按顺序运行三个流式传输演示
    basic_streaming()
    streaming_with_metadata()
    streaming_with_system_prompt()
