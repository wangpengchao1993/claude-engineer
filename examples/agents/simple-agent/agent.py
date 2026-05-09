"""
Simple Agent — A minimal Claude-powered agent with tools.

This agent can:
- Read and write files
- Run shell commands
- Search the web (simulated)

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python agent.py "your task here"
"""

import json
import os
import subprocess
import sys
import anthropic

client = anthropic.Anthropic()

# --- Tools ---

tools = [
    {
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
    """Execute a tool and return the result as a string."""
    try:
        if name == "read_file":
            with open(input_data["path"], "r") as f:
                return f.read()

        elif name == "write_file":
            os.makedirs(os.path.dirname(input_data["path"]) or ".", exist_ok=True)
            with open(input_data["path"], "w") as f:
                f.write(input_data["content"])
            return f"File written: {input_data['path']}"

        elif name == "run_command":
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
            path = input_data.get("path", ".")
            entries = os.listdir(path)
            return "\n".join(sorted(entries))

        else:
            return f"Error: Unknown tool '{name}'"

    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


# --- Agent Loop ---

SYSTEM_PROMPT = """You are a helpful coding assistant with access to the file system and shell.

When given a task:
1. Understand what's being asked
2. Explore the relevant files and structure
3. Make changes or provide information
4. Verify your changes work (run tests if applicable)

Be efficient — don't read files you don't need. Explain what you're doing briefly."""


def run_agent(task: str, max_turns: int = 20) -> str:
    """Run the agent on a task."""
    print(f"\nTask: {task}\n{'='*60}\n")

    messages = [{"role": "user", "content": task}]

    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Collect text output
        text_parts = []
        tool_calls = []

        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(block)

        # Print any text
        if text_parts:
            text = "\n".join(text_parts)
            print(f"Agent: {text}\n")

        # If done, return
        if response.stop_reason == "end_turn":
            return "\n".join(text_parts)

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for tool_call in tool_calls:
            print(f"  [{tool_call.name}] {json.dumps(tool_call.input)[:100]}")
            result = execute_tool(tool_call.name, tool_call.input)
            print(f"  → {result[:200]}{'...' if len(result) > 200 else ''}\n")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})

    return "Agent reached maximum turns."


# --- Main ---

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = "List the files in the current directory and describe what this project does."

    run_agent(task)
