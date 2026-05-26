# Getting Started with Claude

> From zero to productive — install Claude Code, set up your environment, and complete your first real task.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Authentication](#authentication)
- [Your First Session](#your-first-session)
- [Understanding How Claude Code Works](#understanding-how-claude-code-works)
- [Your First Real Task](#your-first-real-task)
- [Essential Configuration](#essential-configuration)
- [What to Learn Next](#what-to-learn-next)

---

## Prerequisites

Before installing Claude Code, ensure you have:

- **Node.js 18+** — [Download](https://nodejs.org/)
- **An Anthropic API key** — [Get one here](https://console.anthropic.com/)
- **A terminal** — Any modern terminal (iTerm2, Windows Terminal, etc.)
- **Git** (recommended) — Claude Code works best in git repositories

### Platform Support

| Platform | Status |
|----------|--------|
| macOS | Fully supported (CLI + Desktop app) |
| Linux | Fully supported (CLI) |
| Windows | Supported via WSL2 (CLI) + Desktop app |

---

## Installation

### Option 1: npm (Recommended)

```bash
npm install -g @anthropic-ai/claude-code
```

### Option 2: Desktop App

Download from [claude.ai/code](https://claude.ai/code) for Mac or Windows.

### Option 3: IDE Extensions

- **VS Code**: Search "Claude Code" in the Extensions marketplace
- **JetBrains**: Search "Claude Code" in the Plugin marketplace

### Verify Installation

```bash
claude --version
```

---

## Authentication

### Using API Key

```bash
# Set your API key (add to your shell profile for persistence)
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Or let Claude Code prompt you on first run
claude
```

### Using AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
# Ensure AWS credentials are configured
```

### Using Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=1
# Ensure Google Cloud credentials are configured
```

---

## Your First Session

### Start Claude Code

```bash
# Navigate to a project directory
cd your-project

# Start Claude Code
claude
```

You'll see an interactive prompt where you can type messages to Claude.

### Try These Starter Commands

```
> what does this project do?

> explain the file structure

> what dependencies does this project use?

> find all TODO comments in the codebase
```

### Generate a CLAUDE.md

This is the **single most impactful thing** you can do to improve Claude's effectiveness:

```
> /init
```

Claude will analyze your project and generate a `CLAUDE.md` file with:
- Project overview
- Tech stack
- Common commands
- Code conventions

Review and edit the generated file — this becomes Claude's "memory" of your project.

---

## Understanding How Claude Code Works

### The Tool Loop

Claude Code doesn't just chat — it **acts**. Here's the cycle:

```
You: "add input validation to the signup form"
                    │
                    ▼
    ┌─────────────────────────────┐
    │  Claude analyzes the task    │
    │  and plans its approach      │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │  Reads relevant files        │◄──┐
    │  (Glob, Read, Grep)          │   │
    └──────────────┬──────────────┘   │
                   │                   │
                   ▼                   │
    ┌─────────────────────────────┐   │
    │  Makes changes               │   │ Iterates until
    │  (Edit, Write, Bash)         │   │ task is complete
    └──────────────┬──────────────┘   │
                   │                   │
                   ▼                   │
    ┌─────────────────────────────┐   │
    │  Verifies changes            │───┘
    │  (runs tests, checks output) │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │  Reports results to you      │
    └─────────────────────────────┘
```

### Permission Prompts

Claude will ask your permission before:
- **Writing or editing files** — Shows you the change first
- **Running shell commands** — Shows the command first

You can approve (`y`), deny (`n`), or always allow specific actions.

### Context Window

Claude has a large context window (up to 1M tokens), but it's not infinite. Tips:
- Use `/compact` when the conversation gets long
- Use `/clear` to start fresh
- Use `CLAUDE.md` for persistent context instead of repeating instructions

---

## Your First Real Task

Let's walk through a practical example. Try this in any project:

### Task: Add a Feature

```
> add a health check endpoint at GET /health that returns
  { "status": "ok", "timestamp": "<current ISO time>" }
```

Watch as Claude:
1. Searches for existing route patterns in your project
2. Creates the endpoint following your project's conventions
3. May add a test if your project has tests

### Task: Fix a Bug

```
> npm test

(paste the error output)

> fix this test failure
```

### Task: Understand Code

```
> explain how authentication works in this project — trace the
  flow from login request to JWT token issuance
```

### Task: Refactor

```
> refactor the UserService class to use dependency injection
  instead of direct database calls
```

---

## Essential Configuration

### Settings File Locations

| File | Scope |
|------|-------|
| `.claude/settings.json` | Project-level (commit to git) |
| `~/.claude/settings.json` | User-global |

### Recommended Starter Settings

Create `.claude/settings.json` in your project:

```jsonc
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      // Add your common commands:
      // "Bash(npm test)",
      // "Bash(npm run lint)"
    ]
  }
}
```

### Model Selection

```bash
# Use a specific model
claude --model claude-opus-4-6

# Or set a default
export ANTHROPIC_MODEL=claude-sonnet-4-6-20250514

# Switch model during a session
/model
```

| Model | Best For |
|-------|----------|
| Opus 4.6 | Complex tasks, large refactors, architecture |
| Sonnet 4.6 | Daily development, balanced speed/quality |
| Haiku 4.5 | Quick questions, simple edits |

---

## Common Patterns for Beginners

### 1. The Explore-Then-Act Pattern

```
> explain the current implementation of [feature]
(understand the code first)

> now add [new functionality] following the same patterns
(then make changes)
```

### 2. The Review-Fix Pattern

```
> review src/api/auth.ts for potential issues
(get Claude's analysis)

> fix the issues you found
(let Claude fix them)
```

### 3. The Test-Driven Pattern

```
> write a failing test for [feature]
(test first)

> now implement the feature to make the test pass
(then implement)
```

### 4. The Pipe-and-Ask Pattern

```bash
# Quick analysis without entering interactive mode
git diff | claude -p "any issues with these changes?"
cat error.log | claude -p "what caused this error?"
```

---

## Keyboard Reference

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line |
| `Shift+Tab` | Toggle Plan mode |
| `Esc` (1x) | Cancel input |
| `Esc` (2x) | Interrupt Claude |
| `Up Arrow` | Previous messages |
| `!command` | Run shell command |

---

## What to Learn Next

Now that you're up and running, explore these guides in order:

1. **[Claude Code Mastery](02-claude-code-mastery.md)** — Deep dive into all CLI features
2. **[CLAUDE.md Guide](03-claude-md-guide.md)** — Master project configuration
3. **[Hooks & Automation](04-hooks-and-automation.md)** — Automate your workflow
4. **[MCP Servers](05-mcp-servers.md)** — Extend Claude's capabilities

Or jump to the [Cheatsheet](../../cheatsheet.md) for a quick reference.

---

<p align="center">
  <strong>Next:</strong> <a href="02-claude-code-mastery.md">Claude Code Mastery</a> — Master every feature
</p>

---

[Table of Contents](../../README.md) | [Next: Claude Code Mastery →](02-claude-code-mastery.md)
