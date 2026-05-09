"""
Streaming Demo — Claude API Streaming Example

Demonstrates streaming responses for real-time output.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python stream_demo.py
"""

import anthropic

client = anthropic.Anthropic()


def basic_streaming():
    """Stream a simple text response."""
    print("=== Basic Streaming ===\n")

    with client.messages.stream(
        model="claude-sonnet-4-6-20250514",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": "Write a haiku about programming, then explain it."
        }]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


def streaming_with_metadata():
    """Stream with event handling for metadata."""
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
            if event.type == "message_start":
                print(f"[Model: {event.message.model}]")
            elif event.type == "content_block_delta" and hasattr(event.delta, "text"):
                print(event.delta.text, end="", flush=True)
            elif event.type == "message_stop":
                print("\n[Done]")

    # Access final message for usage stats
    message = stream.get_final_message()
    print(f"[Tokens — Input: {message.usage.input_tokens}, Output: {message.usage.output_tokens}]")
    print()


def streaming_with_system_prompt():
    """Stream with a system prompt for controlled output."""
    print("=== Streaming with System Prompt ===\n")

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
    basic_streaming()
    streaming_with_metadata()
    streaming_with_system_prompt()
