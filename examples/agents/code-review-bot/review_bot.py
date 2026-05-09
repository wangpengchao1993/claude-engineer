"""
Code Review Bot — Automated PR reviewer powered by Claude.

Reviews pull request diffs for:
- Security vulnerabilities
- Logic errors and bugs
- Performance issues
- Missing error handling

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic

    # Review staged changes
    python review_bot.py

    # Review a specific diff
    git diff main...feature | python review_bot.py --stdin

    # Review a file
    python review_bot.py --file src/api/auth.ts
"""

import argparse
import subprocess
import sys
import anthropic

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


def get_diff() -> str:
    """Get the git diff of staged changes."""
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    diff = result.stdout

    if not diff:
        # Fall back to unstaged changes
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True, text=True
        )
        diff = result.stdout

    if not diff:
        # Fall back to last commit
        result = subprocess.run(
            ["git", "diff", "HEAD~1"],
            capture_output=True, text=True
        )
        diff = result.stdout

    return diff


def review_code(code: str, source: str = "diff") -> str:
    """Send code to Claude for review."""
    print(f"Reviewing {source}...\n")

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
    parser = argparse.ArgumentParser(description="AI-powered code review bot")
    parser.add_argument("--stdin", action="store_true", help="Read diff from stdin")
    parser.add_argument("--file", type=str, help="Review a specific file")
    args = parser.parse_args()

    if args.stdin:
        code = sys.stdin.read()
        if not code.strip():
            print("No input received on stdin.")
            sys.exit(1)
        review_code(code, "diff")

    elif args.file:
        with open(args.file, "r") as f:
            code = f.read()
        review_code(code, f"file: {args.file}")

    else:
        diff = get_diff()
        if not diff.strip():
            print("No changes to review. Stage some changes or use --file.")
            sys.exit(1)
        review_code(diff, "git diff")


if __name__ == "__main__":
    main()
