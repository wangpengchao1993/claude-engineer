# Multi-Agent Patterns

> Orchestrate multiple Claude agents for complex tasks — parallel execution, specialization, and workflow composition.

## Table of Contents

- [What Are Multi-Agent Patterns?](#what-are-multi-agent-patterns)
- [Claude Code Subagents](#claude-code-subagents)
- [Agent Patterns](#agent-patterns)
- [Real-World Examples](#real-world-examples)
- [Building Custom Multi-Agent Systems](#building-custom-multi-agent-systems)
- [Best Practices](#best-practices)

---

## What Are Multi-Agent Patterns?

Multi-agent patterns use multiple Claude instances working together, each with a specific role or focus area. This approach enables:

- **Parallelism** — Multiple agents working simultaneously
- **Specialization** — Each agent focuses on what it does best
- **Context isolation** — Each agent has its own context window
- **Scale** — Handle tasks too large for a single agent

---

## Claude Code Subagents

Claude Code has built-in multi-agent capabilities. When you give Claude a complex task, it can automatically launch **subagents**:

### Built-in Agent Types

| Type | Purpose | Example Use |
|------|---------|-------------|
| **Explore** | Fast codebase search and analysis | "Find all usages of deprecated API" |
| **Plan** | Design implementation strategies | "Plan the database migration" |
| **General** | Multi-step complex tasks | "Refactor auth across 20 files" |

### How It Works in Practice

```
You: "Search the entire codebase for SQL injection vulnerabilities
      and fix any you find"

Claude internally:
├── Agent 1 (Explore): Searches src/api/ for raw SQL usage
├── Agent 2 (Explore): Searches src/services/ for query building
├── Agent 3 (Explore): Searches src/repositories/ for ORM usage
│
└── Main: Collects findings, then fixes each vulnerability
```

### Encouraging Parallel Agents

Claude decides when to use subagents, but you can encourage it:

```
# This naturally triggers parallel agents
"Simultaneously check all three services (auth, payments, notifications)
 for proper error handling"

# This too
"Search for all files that import the old UserModel and list them,
 while also finding all references to the new UserEntity"
```

---

## Agent Patterns

### Pattern 1: Fan-Out / Fan-In

Multiple agents work in parallel, results are merged.

```
                    ┌── Agent: Review auth code ──────┐
                    │                                   │
Task ──► Splitter ──┼── Agent: Review API endpoints ──┼──► Merger ──► Result
                    │                                   │
                    └── Agent: Review data layer ──────┘
```

**Use case**: Code review across a large codebase, security audits, migration analysis.

### Pattern 2: Pipeline

Agents work sequentially, each building on the previous result.

```
Task ──► Agent 1: Analyze ──► Agent 2: Plan ──► Agent 3: Implement ──► Result
```

**Use case**: Complex feature implementation (analyze current code → design solution → implement).

### Pattern 3: Specialist Router

A router agent delegates to specialized agents based on the task.

```
                     ┌── Frontend Agent (React/CSS) ──────┐
                     │                                      │
Task ──► Router ─────┼── Backend Agent (API/DB) ──────────┼──► Result
                     │                                      │
                     └── DevOps Agent (CI/CD/Infra) ───────┘
```

**Use case**: Full-stack changes that span frontend, backend, and infrastructure.

### Pattern 4: Critic / Verifier

One agent does the work, another reviews it.

```
Task ──► Worker Agent ──► Reviewer Agent ──► Approved? ──► Result
              │                                  │
              └──────── Revise ◄─────────────────┘
```

**Use case**: Critical code changes, security-sensitive implementations.

### Pattern 5: Parallel Workers with Shared Context

Multiple agents work on independent subtasks with a shared understanding.

```
Context Setup ──┬── Agent 1: Implement feature A
                ├── Agent 2: Implement feature B
                ├── Agent 3: Write tests for A
                └── Agent 4: Write tests for B
                         │
                         ▼
                    Integration
```

**Use case**: Large feature with independent components.

---

## Real-World Examples

### Example 1: Full Codebase Audit

```
"Perform a security audit of the entire codebase. Check for:
1. SQL injection in all database queries
2. XSS vulnerabilities in all template rendering
3. Authentication bypass in middleware
4. Sensitive data exposure in API responses
5. Insecure dependencies in package.json

Organize findings by severity."
```

Claude may launch 3-5 agents to search different areas in parallel.

### Example 2: Large-Scale Refactoring

```
"We're migrating from Express to Fastify. The app has 40+ route files
in src/routes/. For each file:
1. Convert the Express router syntax to Fastify
2. Update middleware references
3. Convert req/res to Fastify request/reply
4. Update the route registration in src/app.ts

Start with a plan, then execute."
```

### Example 3: Cross-Service Analysis

```
"We have a bug where users see stale data after updating their profile.
The flow goes through:
- Frontend: src/components/Profile.tsx
- API Gateway: services/gateway/src/routes/profile.ts
- User Service: services/users/src/handlers/update.ts
- Cache Layer: services/cache/src/strategies/user.ts

Trace the data flow through all services and find where the
cache invalidation is missing."
```

---

## Building Custom Multi-Agent Systems

### Using Claude API for Multi-Agent

```python
import anthropic
import asyncio

client = anthropic.Anthropic()

async def run_agent(system_prompt: str, task: str) -> str:
    """Run a single specialized agent."""
    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

async def fan_out_review(code_files: dict[str, str]) -> dict:
    """Review multiple files in parallel with specialized agents."""

    security_prompt = "You are a security expert. Review for vulnerabilities only."
    perf_prompt = "You are a performance expert. Review for bottlenecks only."
    logic_prompt = "You are a senior dev. Review for logic errors and edge cases."

    tasks = []
    for name, code in code_files.items():
        tasks.append(run_agent(security_prompt, f"Review:\n```\n{code}\n```"))
        tasks.append(run_agent(perf_prompt, f"Review:\n```\n{code}\n```"))
        tasks.append(run_agent(logic_prompt, f"Review:\n```\n{code}\n```"))

    results = await asyncio.gather(*tasks)
    return {"reviews": results}
```

### Using Claude Code in Scripts

```bash
#!/bin/bash
# multi-agent-review.sh — Parallel code review with multiple Claude instances

FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(ts|py|rs)$')

for file in $FILES; do
    # Launch reviews in parallel (background processes)
    cat "$file" | claude -p "Security review this file" \
        --system-prompt "Focus only on security vulnerabilities." &

    cat "$file" | claude -p "Performance review this file" \
        --system-prompt "Focus only on performance issues." &
done

# Wait for all background reviews
wait
echo "All reviews complete."
```

---

## Best Practices

### 1. Keep Agent Roles Clear

Each agent should have a single, well-defined responsibility. Don't create "do everything" agents.

### 2. Minimize Inter-Agent Communication

Agents work best independently. If agents need to share a lot of state, consider using a single agent instead.

### 3. Use the Right Granularity

- **Too few agents**: Bottleneck on one context window
- **Too many agents**: Overhead of coordination outweighs benefits
- **Sweet spot**: 2-5 agents for most tasks

### 4. Handle Failures Gracefully

Individual agents can fail. Design your system to:
- Continue if one agent fails
- Retry failed agents
- Aggregate partial results

### 5. Match Agent Capabilities to Tasks

| Task Type | Agents Needed |
|-----------|---------------|
| Simple bug fix | 1 (no multi-agent needed) |
| Code review | 1-3 (by area or concern) |
| Large refactor | 2-5 (by module or file group) |
| Full audit | 3-5 (by vulnerability class) |

---

<p align="center">
  <strong>Next:</strong> <a href="07-api-and-sdk.md">API & SDK</a> — Build applications with Claude
</p>
