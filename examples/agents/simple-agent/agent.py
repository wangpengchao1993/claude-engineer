"""
Simple Agent — A minimal Claude-powered agent with tools.
简单代理 - 一个使用 Claude 驱动的、带工具的最小化代理。

This agent can:
此代理可以：
- Read and write files
  读写文件
- Run shell commands
  运行 shell 命令
- Search the web (simulated)
  搜索网络（模拟）

Usage:
用法：
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python agent.py "your task here"
"""

import json
import os
import subprocess
import sys
import anthropic

# Initialize the Anthropic client
# 初始化 Anthropic 客户端
client = anthropic.Anthropic()

# --- Tools ---
# --- 工具定义 ---

tools = [
    {
        # read_file: Read the contents of a file
        # read_file：读取文件内容
        "name": "read_file",
        "description": "Read the contents of a file at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"]
        }
    },
    {
        # write_file: Write content to a file
        # write_file：将内容写入文件
        "name": "write_file",
        "description": "Write content to a file. Creates the file if it doesn't exist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to write"},
                "content": {"type": "string", "description": "Content to write"}
            },
            "required": ["path", "content"]
        }
    },
    {
        # run_command: Execute a shell command
        # run_command：执行 shell 命令
        "name": "run_command",
        "description": "Run a shell command and return its output. Use for listing files, running tests, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"}
            },
            "required": ["command"]
        }
    },
    {
        # list_directory: List files and directories
        # list_directory：列出文件和目录
        "name": "list_directory",
        "description": "List files and directories at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path (default: current directory)"}
            },
            "required": []
        }
    }
]


def execute_tool(name: str, input_data: dict) -> str:
    """Execute a tool and return the result as a string.
    执行工具并以字符串形式返回结果。"""
    try:
        if name == "read_file":
            # Read file contents
            # 读取文件内容
            with open(input_data["path"], "r") as f:
                return f.read()

        elif name == "write_file":
            # Create parent directories if needed, then write file
            # 如有需要先创建父目录，然后写入文件
            os.makedirs(os.path.dirname(input_data["path"]) or ".", exist_ok=True)
            with open(input_data["path"], "w") as f:
                f.write(input_data["content"])
            return f"File written: {input_data['path']}"

        elif name == "run_command":
            # Run shell command with a 30-second timeout
            # 运行 shell 命令，超时时间为 30 秒
            result = subprocess.run(
                input_data["command"],
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output or "(no output)"

        elif name == "list_directory":
            # List directory entries, sorted alphabetically
            # 列出目录条目，按字母排序
            path = input_data.get("path", ".")
            entries = os.listdir(path)
            return "\n".join(sorted(entries))

        else:
            return f"Error: Unknown tool '{name}'"

    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


# --- Agent Loop ---
# --- 代理循环 ---

SYSTEM_PROMPT = """You are a helpful coding assistant with access to the file system and shell.

When given a task:
1. Understand what's being asked
2. Explore the relevant files and structure
3. Make changes or provide information
4. Verify your changes work (run tests if applicable)

Be efficient — don't read files you don't need. Explain what you're doing briefly."""
# 系统提示说明：
# 你是一个有文件系统和 shell 访问权限的编程助手。
# 接到任务后：1. 理解需求 2. 探索相关文件 3. 进行修改或提供信息 4. 验证更改是否生效


def run_agent(task: str, max_turns: int = 20) -> str:
    """Run the agent on a task.
    在任务上运行代理。"""
    print(f"\nTask: {task}\n{'='*60}\n")

    messages = [{"role": "user", "content": task}]

    for turn in range(max_turns):
        # Send message to Claude with tools available
        # 将消息发送给 Claude，附带可用的工具
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Collect text output
        # 收集文本输出
        text_parts = []
        tool_calls = []

        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(block)

        # Print any text
        # 打印文本内容
        if text_parts:
            text = "\n".join(text_parts)
            print(f"Agent: {text}\n")

        # If done, return
        # 如果完成，返回结果
        if response.stop_reason == "end_turn":
            return "\n".join(text_parts)

        # Process tool calls
        # 处理工具调用
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for tool_call in tool_calls:
            print(f"  [{tool_call.name}] {json.dumps(tool_call.input)[:100]}")
            # Execute the tool and collect the result
            # 执行工具并收集结果
            result = execute_tool(tool_call.name, tool_call.input)
            print(f"  → {result[:200]}{'...' if len(result) > 200 else ''}\n")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result,
            })

        # Send tool results back to Claude as a user message
        # 将工具结果作为用户消息发送回 Claude
        messages.append({"role": "user", "content": tool_results})

    return "Agent reached maximum turns."


# --- Main ---
# --- 主程序 ---

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use command-line argument as the task
        # 使用命令行参数作为任务
        task = " ".join(sys.argv[1:])
    else:
        # Default task if no argument provided
        # 未提供参数时使用默认任务
        task = "List the files in the current directory and describe what this project does."

    run_agent(task)
