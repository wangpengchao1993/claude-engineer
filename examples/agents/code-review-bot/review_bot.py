"""
Code Review Bot — Automated PR reviewer powered by Claude.
代码审查机器人 - 由 Claude 驱动的自动化 PR 审查工具。

Reviews pull request diffs for:
审查拉取请求的 diff，检查以下内容：
- Security vulnerabilities
  安全漏洞
- Logic errors and bugs
  逻辑错误和缺陷
- Performance issues
  性能问题
- Missing error handling
  缺失的错误处理

Usage:
用法：
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic

    # Review staged changes
    # 审查暂存的更改
    python review_bot.py

    # Review a specific diff
    # 审查特定的 diff
    git diff main...feature | python review_bot.py --stdin

    # Review a file
    # 审查文件
    python review_bot.py --file src/api/auth.ts
"""

import argparse
import subprocess
import sys
import anthropic

# Initialize the Anthropic client
# 初始化 Anthropic 客户端
client = anthropic.Anthropic()

REVIEW_PROMPT = """You are a senior software engineer performing a thorough code review.

## Review Checklist
1. **Security** — Injection, auth bypass, data exposure, SSRF, path traversal
2. **Bugs** — Logic errors, off-by-one, null/undefined handling, race conditions
3. **Performance** — N+1 queries, unnecessary allocations, O(n²) when O(n) is possible
4. **Error Handling** — Uncaught exceptions, missing error cases, silent failures
5. **Edge Cases** — Empty inputs, large inputs, concurrent access, unicode

## Output Format
For each finding, use this format:

### [SEVERITY] Title
**File:** `path/to/file` (line X)
**Issue:** Description of the problem
**Fix:**
```
suggested code fix
```

Severity levels:
- 🔴 **CRITICAL** — Must fix before merge (security, data loss, crash)
- 🟡 **WARNING** — Should fix (bugs, performance, error handling)
- 🔵 **SUGGESTION** — Nice to have (readability, best practices)

## Rules
- Be specific — cite exact lines and show fixes
- Skip style/formatting comments
- If the code looks good, say so briefly
- End with a summary: total findings, overall assessment, merge recommendation
"""
# REVIEW_PROMPT 审查提示说明：
# 审查清单包含五大类：
# 1. 安全性 — 注入攻击、认证绕过、数据泄露、SSRF、路径遍历
# 2. 缺陷 — 逻辑错误、偏移一位错误、空值处理、竞态条件
# 3. 性能 — N+1 查询、不必要的内存分配、可用 O(n) 时却用了 O(n²)
# 4. 错误处理 — 未捕获的异常、遗漏的错误场景、静默失败
# 5. 边界情况 — 空输入、大输入、并发访问、Unicode
# 严重级别分为：严重（必须修复）、警告（应当修复）、建议（锦上添花）


def get_diff() -> str:
    """Get the git diff of staged changes.
    获取已暂存更改的 git diff。"""
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    diff = result.stdout

    if not diff:
        # Fall back to unstaged changes
        # 回退到未暂存的更改
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True, text=True
        )
        diff = result.stdout

    if not diff:
        # Fall back to last commit
        # 回退到上一次提交
        result = subprocess.run(
            ["git", "diff", "HEAD~1"],
            capture_output=True, text=True
        )
        diff = result.stdout

    return diff


def review_code(code: str, source: str = "diff") -> str:
    """Send code to Claude for review.
    将代码发送给 Claude 进行审查。"""
    print(f"Reviewing {source}...\n")

    # Use streaming to display review results in real time
    # 使用流式传输实时显示审查结果
    with client.messages.stream(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system=REVIEW_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Review this {source}:\n\n```\n{code}\n```"
        }]
    ) as stream:
        full_response = []
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response.append(text)

    print("\n")
    return "".join(full_response)


def main():
    """Main entry point: parse arguments and run review.
    主入口：解析参数并执行审查。"""
    parser = argparse.ArgumentParser(description="AI-powered code review bot")
    parser.add_argument("--stdin", action="store_true", help="Read diff from stdin")
    parser.add_argument("--file", type=str, help="Review a specific file")
    args = parser.parse_args()

    if args.stdin:
        # Read diff from standard input
        # 从标准输入读取 diff
        code = sys.stdin.read()
        if not code.strip():
            print("No input received on stdin.")
            sys.exit(1)
        review_code(code, "diff")

    elif args.file:
        # Read and review a specific file
        # 读取并审查指定文件
        with open(args.file, "r") as f:
            code = f.read()
        review_code(code, f"file: {args.file}")

    else:
        # Default: review git diff
        # 默认：审查 git diff
        diff = get_diff()
        if not diff.strip():
            print("No changes to review. Stage some changes or use --file.")
            sys.exit(1)
        review_code(diff, "git diff")


if __name__ == "__main__":
    main()
