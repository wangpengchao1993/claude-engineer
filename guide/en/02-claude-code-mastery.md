# Claude Code Mastery

> Master every feature of Claude Code CLI — the most powerful way to use Claude for software engineering.

## Table of Contents

- [What is Claude Code?](#what-is-claude-code)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Interactive Mode](#interactive-mode)
- [Non-Interactive Mode](#non-interactive-mode)
- [Context Management](#context-management)
- [Permission System](#permission-system)
- [Plan Mode](#plan-mode)
- [Subagents](#subagents)
- [Working with Git](#working-with-git)
- [Working with Tests](#working-with-tests)
- [IDE Integration](#ide-integration)
- [Advanced Tips](#advanced-tips)

---

## What is Claude Code?

Claude Code is Anthropic's official CLI tool that turns Claude into an AI-powered software engineering assistant. It can:

- Read, write, and edit files in your project
- Run shell commands
- Search codebases
- Manage git operations
- Work with MCP servers for extended capabilities
- Launch parallel subagents for complex tasks

It's available as a CLI, desktop app (Mac/Windows), web app (claude.ai/code), and IDE extensions (VS Code, JetBrains).

---

## Installation

```bash
# Install via npm (recommended)
npm install -g @anthropic-ai/claude-code

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Verify installation
claude --version

# Start using Claude Code
claude
```

### First Run

On first launch, Claude Code will:
1. Detect your project structure
2. Read any existing `CLAUDE.md` files
3. Start an interactive session

**Pro tip**: Run `/init` immediately to generate a `CLAUDE.md` for your project. This dramatically improves Claude's understanding of your codebase.

---

## Core Concepts

### How Claude Code Thinks

Claude Code operates with a **tool-based architecture**:

1. You provide a prompt (task, question, or instruction)
2. Claude analyzes the task and decides which tools to use
3. It executes tools (read files, search, edit, run commands)
4. It iterates until the task is complete
5. It reports back with results

### Available Tools

Claude Code has access to these built-in tools:

| Tool | What It Does |
|------|-------------|
| **Read** | Read file contents |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Glob** | Find files by pattern |
| **Grep** | Search file contents |
| **Bash** | Execute shell commands |
| **Agent** | Launch subagents for parallel work |

Plus any tools provided by MCP servers you configure.

---

## Interactive Mode

The default mode — start a conversation with Claude:

```bash
claude
```

### Effective Prompting in Interactive Mode

**Be specific about what you want:**

```
Bad:  "fix the bug"
Good: "the login endpoint returns 500 when email contains '+' — fix the validation in src/auth/validator.ts"
```

**Provide context when needed:**

```
"I'm working on the user settings page. The React component is at
src/components/Settings.tsx and the API handler is at src/api/settings.ts.
Add a 'change password' feature with proper validation."
```

**Use incremental instructions:**

Rather than one massive prompt, break complex tasks into steps:
1. "First, read the current auth implementation and explain how it works"
2. "Now add OAuth2 support following the same patterns"
3. "Write tests for the new OAuth2 flow"

### Conversation Management

```bash
# Resume the last conversation
claude -c

# Your conversation history is preserved
# Use /compact when context gets large
/compact

# Clear and start fresh
/clear

# Check token usage
/cost
```

---

## Non-Interactive Mode

Perfect for scripts, CI/CD, and automation:

```bash
# Simple query with print mode
claude -p "what does this project do?"

# Pipe input for analysis
cat error.log | claude -p "summarize these errors"
git diff --staged | claude -p "review these changes"

# JSON output for programmatic use
claude -p "list all API endpoints" --output-format json

# Limit agent turns for predictable execution
claude -p "run the tests" --max-turns 5

# Chain commands
git diff HEAD~1 | claude -p "write a commit message" | git commit -F -
```

### Use Cases for Non-Interactive Mode

- **CI/CD**: Automated code review on PRs
- **Git hooks**: Pre-commit validation
- **Scripts**: Batch processing files
- **Pipelines**: Part of larger automation workflows

---

## Context Management

### How Context Works

Claude Code has a context window (up to 1M tokens with Opus 4.6). As your conversation grows, context fills up. Managing it well is key to effective usage.

### CLAUDE.md — Persistent Context

The most important context mechanism. Claude automatically reads:

1. `CLAUDE.md` at project root (shared with team via git)
2. `CLAUDE.md` in subdirectories (directory-specific context)
3. `~/.claude/CLAUDE.md` (your personal global config)

**What to put in CLAUDE.md:**
- Project overview and tech stack
- Common commands (build, test, lint)
- Code conventions and patterns
- Things to avoid
- Architecture overview

See [CLAUDE.md Guide](03-claude-md-guide.md) for detailed best practices.

### Context Compaction

When the context window fills up, use `/compact` to compress the conversation while preserving key information. Claude will:
1. Summarize the conversation so far
2. Keep important code snippets and decisions
3. Free up context for new work

**Pro tip**: Use `/compact` with a summary hint to preserve specific info:
```
/compact focus on the authentication changes we discussed
```

### Adding Extra Context

```bash
# Add another directory to context
claude --add-dir /path/to/related/project

# Pipe files directly
cat spec.md | claude "implement this specification"
```

---

## Permission System

Claude Code asks permission before potentially destructive actions. There are three permission modes:

| Mode | Behavior |
|------|----------|
| **Default** | Asks before writes and commands |
| **Plan** | Read-only until plan is approved |
| **Bypass** | No permission prompts (use with caution) |

### Configuring Permissions

In `.claude/settings.json`:

```jsonc
{
  "permissions": {
    "allow": [
      "Read",           // Always allow file reads
      "Glob",           // Always allow file search
      "Grep",           // Always allow content search
      "Bash(npm test)", // Allow specific commands
      "Bash(npm run lint)"
    ],
    "deny": [
      "Bash(rm -rf *)", // Never allow this
    ]
  }
}
```

**Best practice**: Start with default permissions. Add specific `allow` rules for commands you run frequently (like test and lint commands).

---

## Plan Mode

Plan mode makes Claude think before acting. Toggle with **Shift+Tab**.

### When to Use Plan Mode

- Complex refactoring across multiple files
- Architecture decisions
- Tasks where you want to review the approach first
- When you're not sure about the best solution

### How It Works

1. **Toggle on**: Press `Shift+Tab` (or start with plan mode)
2. **Claude plans**: Reads code, analyzes the task, proposes a plan
3. **You review**: Approve, modify, or redirect
4. **Toggle off**: Press `Shift+Tab` to let Claude execute
5. **Claude implements**: Follows the approved plan

### Pro Tips for Plan Mode

- Use it for the first iteration of complex tasks
- Ask Claude to consider alternatives: "propose 2-3 different approaches"
- Once the plan is good, exit plan mode and say "execute the plan"

---

## Subagents

Claude can launch parallel subagents for complex tasks. This is like having multiple Claude instances working simultaneously.

### How Subagents Work

When Claude encounters a task that benefits from parallelization, it uses the Agent tool to launch specialized subagents:

- **Explore agents**: Fast codebase exploration and search
- **Plan agents**: Design implementation approaches
- **General-purpose agents**: Handle complex multi-step subtasks

### When Claude Uses Subagents

- Searching multiple areas of the codebase simultaneously
- Running independent tasks in parallel
- Isolating large research tasks from the main context
- Working on files that need independent analysis

### You Don't Need to Do Anything Special

Claude automatically decides when to use subagents. But you can encourage it:

```
"Search for all usages of the deprecated UserService class across the
entire codebase and list the files that need updating"
```

Claude may launch multiple search agents to cover different areas in parallel.

---

## Working with Git

Claude Code is excellent at git operations:

```
# Common git workflows
"review the last 3 commits and summarize changes"
"write a commit message for the staged changes"
"create a PR with a summary of all changes on this branch"
"resolve the merge conflicts in src/api.ts"
"show me what changed in the authentication module this week"
```

### Commit Messages

Claude follows repository conventions. For best results, include a few example commits in your `CLAUDE.md`:

```markdown
## Git Conventions
- Use conventional commits: feat(scope): description
- Keep subject line under 72 characters
- Include body for non-trivial changes
```

### Pull Requests

```
"create a PR for this branch with a detailed description"
```

Claude will:
1. Analyze all commits on the branch
2. Generate a title and description
3. Create the PR using `gh` CLI

---

## Working with Tests

```
# Run and fix tests
"run the tests and fix any failures"

# Write tests for existing code
"write tests for the UserService class"

# Test-driven development
"write a failing test for [feature], then implement the feature"

# Coverage
"run tests with coverage and add tests for uncovered code in auth/"
```

**Pro tip**: Include your test commands in `CLAUDE.md` so Claude always runs them correctly:

```markdown
## Testing
- `npm test` — Run all tests
- `npm test -- --watch` — Watch mode
- `npm test -- path/to/file` — Run specific file
```

---

## IDE Integration

### VS Code

Install the Claude Code extension for VS Code:
- Inline chat with Claude
- Highlight code and ask questions
- Terminal integration

### JetBrains

Available for IntelliJ, PyCharm, WebStorm, and other JetBrains IDEs.

---

## Advanced Tips

### 1. Use the Right Level of Autonomy

- **Exploratory tasks**: Let Claude run freely
- **Critical changes**: Use Plan mode first
- **Production code**: Review every change

### 2. Give Claude Enough Context

Claude works best when it understands the full picture:
- Keep `CLAUDE.md` up to date
- Reference specific files in your prompts
- Explain the "why" behind your requests

### 3. Iterate, Don't Overspecify

Instead of writing a 500-word prompt, start simple and iterate:
1. "Add a caching layer to the API"
2. [Review Claude's approach]
3. "Use Redis instead of in-memory cache"
4. [Review and refine]

### 4. Let Claude Handle the Tedious Parts

Claude excels at:
- Boilerplate code generation
- Test writing
- Refactoring across many files
- Documentation
- Migration scripts
- Configuration files

### 5. Use Pipes for Quick Tasks

```bash
# Quick code review
git diff | claude -p "any issues with this?"

# Generate documentation
cat src/api.ts | claude -p "generate API docs in markdown"

# Convert formats
cat data.csv | claude -p "convert to JSON"

# Explain errors
npm test 2>&1 | claude -p "explain why these tests fail"
```

### 6. Multi-Session Workflows

For large projects, use multiple Claude sessions:
1. One session for the main feature work
2. Use `-c` to resume when you come back
3. Use `/compact` to keep context manageable

### 7. Custom System Prompts for Scripts

```bash
claude -p "review for security issues" \
  --system-prompt "You are a security auditor. Focus only on OWASP Top 10 vulnerabilities." \
  < src/auth.ts
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Context window full" | Use `/compact` to compress |
| Claude makes wrong assumptions | Improve your `CLAUDE.md` |
| Slow response | Try `/fast` mode or a smaller model |
| Permission denied | Check `.claude/settings.json` permissions |
| MCP server not connecting | Run `claude mcp list` to verify config |
| Claude edits wrong file | Be more specific in your prompt |

---

<p align="center">
  <strong>Next:</strong> <a href="03-claude-md-guide.md">CLAUDE.md Guide</a> — Master project-level configuration
</p>

---

[← Previous: Getting Started](01-getting-started.md) | [Table of Contents](../../README.md) | [Next: CLAUDE.md Guide →](03-claude-md-guide.md)
