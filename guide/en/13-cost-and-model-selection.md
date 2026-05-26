# Cost Optimization & Model Selection

> Spend wisely, build faster. Choose the right model for each task, understand token economics, and keep your AI-assisted development budget under control.

## Table of Contents

- [Model Comparison](#model-comparison)
- [Token Economics](#token-economics)
- [Cost Estimation](#cost-estimation)
- [Cost Saving Strategies](#cost-saving-strategies)
- [Billing and Limits](#billing-and-limits)
- [Decision Flowchart](#decision-flowchart)

---

## Model Comparison

### The Three Tiers

| Feature | Claude Opus 4 | Claude Sonnet 4 | Claude Haiku |
|---|---|---|---|
| **Quality** | Highest | High | Good |
| **Speed** | Slowest | Medium | Fastest |
| **Cost** | $$$ | $$ | $ |
| **Context** | 200K (1M extended) | 200K | 200K |
| **Best For** | Complex architecture | Daily coding | Simple edits |

### Pricing (per million tokens)

| Model | Input | Output | Cache Write | Cache Read |
|---|---|---|---|---|
| Claude Opus 4 | $15.00 | $75.00 | $18.75 | $1.50 |
| Claude Sonnet 4 | $3.00 | $15.00 | $3.75 | $0.30 |
| Claude Haiku 4.5 | $0.80 | $4.00 | $1.00 | $0.08 |

> Note: Prices may change at any time. Check [anthropic.com/pricing](https://www.anthropic.com/pricing) for current rates.

### When to Use Each Model

**Claude Opus 4** -- the architect:
```
Use when:
- Designing complex system architecture
- Debugging subtle race conditions or memory leaks
- Writing critical security-sensitive code
- Multi-file refactoring with deep dependency chains
- Understanding large unfamiliar codebases
- Tasks requiring extended thinking (1M context)

Skip when:
- Simple file edits
- Running linters or formatters
- Writing boilerplate code
```

**Claude Sonnet 4** -- the daily driver:
```
Use when:
- Feature implementation (most day-to-day coding)
- Code reviews and PR descriptions
- Writing tests
- Refactoring individual modules
- Documentation generation
- Bug fixes with clear error messages

This is your default. Start here.
```

**Claude Haiku** -- the sprinter:
```
Use when:
- Linting and formatting fixes
- Simple find-and-replace patterns
- Generating boilerplate (interfaces, types, schemas)
- Quick syntax questions
- Commit message generation
- Small one-file edits

Skip when:
- The task requires understanding multiple files
- Complex reasoning is needed
```

### Switching Models Mid-Session

```bash
# Check current model
/model

# Switch to a specific model
/model claude-sonnet-4-20250514
/model claude-opus-4-20250514

# Or set via environment variable before starting
export ANTHROPIC_MODEL=claude-sonnet-4-20250514
claude
```

---

## Token Economics

### What Counts as Tokens

Everything Claude reads and writes costs tokens. A token is roughly 3-4 characters of English text or 1-2 characters of code.

```
Approximate token counts:
- 1 line of code      ≈ 10-30 tokens
- 1 function (20 LOC) ≈ 200-600 tokens
- 1 file (200 LOC)    ≈ 2,000-6,000 tokens
- package.json         ≈ 500-2,000 tokens
- A typical CLAUDE.md  ≈ 500-3,000 tokens
```

### What Consumes Tokens Per Request

Every time you send a message, Claude processes:

```
┌─────────────────────────────────────────┐
│  System prompt (Claude Code internals)  │  ~2,000-5,000 tokens
│  CLAUDE.md content                      │  ~500-3,000 tokens
│  Conversation history                   │  Grows each turn
│  Tool results (file reads, commands)    │  Can be very large
│  Your message                           │  Usually small
├─────────────────────────────────────────┤
│  Claude's response                      │  Output tokens (5x cost)
└─────────────────────────────────────────┘
```

**Key insight**: Output tokens cost 5x more than input tokens. A long response from Claude is significantly more expensive than a long prompt from you.

### Conversation History Growth

```
Turn 1:  system + CLAUDE.md + your msg            = ~5K tokens
Turn 5:  system + CLAUDE.md + 5 turns of history   = ~20K tokens
Turn 20: system + CLAUDE.md + 20 turns of history  = ~80K tokens
Turn 50: system + CLAUDE.md + 50 turns of history  = ~200K+ tokens
```

This is why long sessions get expensive. Each message re-sends the entire conversation.

### The /compact Command

`/compact` summarizes your conversation history, drastically reducing token count:

```
Before /compact: 80,000 tokens of history
After /compact:  ~5,000 token summary

Savings: ~75,000 input tokens per subsequent message
```

**When to use /compact**:
- After completing a major task (before starting the next one)
- When you notice responses getting slower
- Every 15-20 turns in a long session
- Before switching to a different area of the codebase

```bash
# Basic compact
/compact

# Compact with focus instruction
/compact focus on the auth module changes we discussed
```

### Context Window Sizes

```
Claude Sonnet 4:  200K tokens (~150K pages of code)
Claude Haiku:     200K tokens
Claude Opus 4:    200K standard, up to 1M with extended thinking

1M tokens ≈ an entire medium-sized codebase
200K tokens ≈ enough for most single-feature work
```

---

## Cost Estimation

### Small Task (~5 minutes)

**Example**: "Fix the typo in the error message in auth.ts"

```
Input:  ~8,000 tokens  (system + CLAUDE.md + file read + your prompt)
Output: ~2,000 tokens  (response + file edit)

Cost with Sonnet 4:
  Input:  8K × $3.00/1M  = $0.024
  Output: 2K × $15.00/1M = $0.030
  Total: ~$0.05

Cost with Haiku:
  Input:  8K × $0.80/1M  = $0.006
  Output: 2K × $4.00/1M  = $0.008
  Total: ~$0.01
```

### Feature Implementation (~1 hour)

**Example**: "Add password reset flow with email verification"

```
Typical session: ~30 turns, multiple file reads/writes

Input:  ~500,000 tokens total (cumulative across all turns)
Output: ~100,000 tokens total

Cost with Sonnet 4:
  Input:  500K × $3.00/1M  = $1.50
  Output: 100K × $15.00/1M = $1.50
  Total: ~$3.00

Cost with Opus 4:
  Input:  500K × $15.00/1M  = $7.50
  Output: 100K × $75.00/1M  = $7.50
  Total: ~$15.00

With /compact at turn 15:
  ~30% savings → Sonnet: ~$2.10, Opus: ~$10.50
```

### Full Project Sprint (~1 week)

**Example**: "Build a REST API with auth, CRUD, and tests"

```
~20 sessions, ~40 turns each, heavy file operations

Input:  ~10,000,000 tokens total
Output: ~2,000,000 tokens total

Cost with Sonnet 4:
  Input:  10M × $3.00/1M  = $30.00
  Output: 2M × $15.00/1M  = $30.00
  Total: ~$60.00

With aggressive cost optimization:
  - /compact every 15 turns
  - Haiku for boilerplate
  - Prompt caching enabled
  Optimized total: ~$25-35
```

### Checking Your Usage

```bash
# Inside Claude Code, check session cost
/cost

# Example output:
# Session cost: $1.47
# ├─ Input tokens:  234,567 ($0.70)
# ├─ Output tokens:  51,234 ($0.77)
# └─ Cache read:    180,000 ($0.05)
```

---

## Cost Saving Strategies

### 1. Match Model to Task Complexity

```
Simple edit, formatting, linting     → Haiku      (cheapest)
Feature work, tests, refactoring     → Sonnet 4   (balanced)
Architecture, complex debugging      → Opus 4     (when it matters)
```

**Rule of thumb**: Start with Sonnet. Only upgrade to Opus if Sonnet gives unsatisfying results. Drop to Haiku for mechanical tasks.

### 2. Keep CLAUDE.md Concise

Every line in CLAUDE.md is sent with every single request. A bloated CLAUDE.md quietly drains your budget.

```markdown
# Bad: 200-line CLAUDE.md with verbose explanations
This project was started in January 2024 and uses a microservices
architecture because we found that our monolith was becoming difficult
to maintain. The team decided to migrate to...
(200 more lines of backstory)

# Good: 40-line CLAUDE.md with essential facts only
## Stack
- TypeScript, Node 20, Express, PostgreSQL, Redis
- Monorepo: apps/api, apps/web, packages/shared

## Conventions
- camelCase for files, PascalCase for components
- All API routes in apps/api/src/routes/
- Tests: *.test.ts co-located with source

## Commands
- npm run dev — start dev server
- npm test — run all tests
```

**Cost impact**:
```
200-line CLAUDE.md ≈ 3,000 tokens × every request
 40-line CLAUDE.md ≈   600 tokens × every request

Over a 30-turn session with Sonnet:
  Bloated: 3,000 × 30 × $3/1M = $0.27 wasted
  Concise: 600 × 30 × $3/1M   = $0.05
  Difference compounds over weeks of use.
```

### 3. Use /compact Aggressively

```bash
# After finishing a task
/compact

# With context preservation
/compact keep the database schema discussion, drop everything about CSS fixes

# Set up auto-compact (in settings)
# Claude Code will suggest compacting when context gets large
```

### 4. Sub-Agent Pattern for Fresh Context

The GSD/Superpowers pattern spawns fresh Claude instances per task:

```bash
# Each sub-agent starts with clean context
# No accumulated history from previous tasks
# Smaller context = cheaper per request

# Main agent orchestrates:
"Implement user registration" → sub-agent 1 (fresh context)
"Add email verification"     → sub-agent 2 (fresh context)
"Write integration tests"    → sub-agent 3 (fresh context)
```

**Why it saves money**: Instead of one session growing to 200K tokens of context, each sub-agent uses only 10-30K.

### 5. Prompt Caching

Prompt caching stores frequently-sent content (system prompt, CLAUDE.md) so you pay full price once, then 90% less for subsequent requests.

```
Without caching:
  Every request sends full CLAUDE.md: $3.00/1M each time

With caching:
  First request: $3.75/1M (cache write, 25% premium)
  Subsequent:    $0.30/1M (cache read, 90% discount)

Break-even: after just 2 requests, caching saves money
```

Claude Code enables prompt caching by default for API usage. For direct API calls:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Your long system prompt here...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Your question"}]
)
```

### 6. Batch API for Large-Scale Work

For non-interactive bulk generation (50% cheaper):

```python
# Create a batch of requests
batch = client.batches.create(
    requests=[
        {
            "custom_id": "task-1",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Generate tests for auth.ts"}]
            }
        },
        {
            "custom_id": "task-2",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Generate tests for user.ts"}]
            }
        }
    ]
)

# Results available within 24 hours
# 50% cheaper than real-time API calls
```

**Good for**: Generating tests for many files, bulk documentation, large refactoring plans.

### 7. Pipe Only Relevant Files

```bash
# Bad: sends entire directory (could be thousands of tokens)
cat src/**/*.ts | claude "review this code"

# Good: send only what's relevant
cat src/auth/login.ts src/auth/middleware.ts | claude "review the auth flow"

# Better: let Claude read files as needed
claude "review the auth flow in src/auth/"
# Claude will selectively read only the files it needs
```

### 8. Smart Prompting Reduces Rounds

Fewer back-and-forth messages = fewer tokens:

```bash
# Bad: vague prompt leads to 5 rounds of clarification
"make it better"
# "What do you mean by better?"
"the performance"
# "Which function?"
"the search function"
# ...

# Good: one clear prompt, one response
"Optimize the searchUsers() function in src/services/user.ts
 for performance. Current issue: it does N+1 queries.
 Use a single JOIN query instead."
```

---

## Billing and Limits

### API Pricing Tiers

```
Pay-as-you-go:
  No minimum commitment
  Billed monthly based on actual usage
  Standard rate limits

Scale tier (contact sales):
  Volume discounts
  Higher rate limits
  Priority access during high demand
```

### Rate Limits

```
Tier 1 (new accounts):
  Opus:   2K input tokens/min,   8K output tokens/min
  Sonnet: 8K input tokens/min,  32K output tokens/min
  Haiku: 16K input tokens/min,  64K output tokens/min

Tier 4 (established accounts):
  Significantly higher limits
  Check console.anthropic.com for your tier
```

**When you hit rate limits**:

```bash
# Claude Code handles rate limits automatically with retries
# If you see "rate limited" messages:

# 1. Switch to a cheaper model (higher limits)
/model claude-sonnet-4-20250514

# 2. Wait a moment and retry
# 3. Use /compact to reduce token usage per request
# 4. Contact Anthropic to increase your tier
```

### Setting Spending Limits

```bash
# Set monthly budget in Anthropic Console
# console.anthropic.com → Settings → Billing → Usage Limits

# Set per-session awareness
# Check cost periodically during long sessions
/cost
```

### Monitoring Usage

```bash
# Anthropic Console dashboard shows:
# - Daily/weekly/monthly spend
# - Token usage by model
# - Request counts
# - Cache hit rates

# In Claude Code:
/cost                    # Current session cost
```

---

## Decision Flowchart

```
                    What's the task?
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         Simple edit   Feature    Architecture
         / format      work       / Complex
              │          │          │
              ▼          ▼          ▼
           Haiku      Sonnet      Opus
           ~$0.01     ~$0.05     ~$0.50
           per task   per task   per task
              │          │          │
              ▼          ▼          ▼
         "Fix this    "Add user   "Design the
          typo"       registration database
                      with email   schema for
                      verify"      a multi-tenant
                                   SaaS platform"


Quick decision guide:
┌─────────────────────────────────────────────────────┐
│ Can a junior dev do this in < 5 min?  → Haiku       │
│ Standard feature work?                → Sonnet      │
│ Would you ask a senior/architect?     → Opus        │
│ Not sure?                             → Start Sonnet│
│   └─ If result is poor               → Upgrade Opus │
└─────────────────────────────────────────────────────┘
```

### Cost Optimization Checklist

```
Before starting a session:
  □ Choose the right model for the task
  □ Keep CLAUDE.md concise and relevant
  □ Have clear, specific prompts ready

During the session:
  □ Use /compact every 15-20 turns
  □ Check /cost periodically
  □ Switch models if task complexity changes
  □ Pipe specific files, not entire directories

After the session:
  □ Review /cost — was it reasonable?
  □ Could a cheaper model have worked?
  □ Any CLAUDE.md bloat to trim?
```

---

## Summary

```
Model selection:
  Haiku  = speed + cost    (simple tasks)
  Sonnet = balance         (daily driver, start here)
  Opus   = quality         (complex reasoning)

Biggest cost drivers:
  1. Output tokens (5x input cost)
  2. Conversation history growth
  3. Bloated CLAUDE.md
  4. Too many back-and-forth rounds

Biggest cost savers:
  1. /compact regularly
  2. Clear, specific prompts
  3. Right model for the task
  4. Prompt caching (automatic in Claude Code)
  5. Sub-agent pattern for multi-task work
```

> Next: [Debugging AI-Generated Code](14-debugging-ai-code.md) -- learn to catch and fix common AI coding mistakes.

---

## Organization-Level Token Budget Management

For individuals, `/cost` is enough. But when scaling AI across teams, you need systematic budget management.

### Budget Allocation Framework

| Dimension | Approach |
|-----------|----------|
| **By team** | Set monthly token budget caps per team, isolate via separate API keys |
| **By project** | High-priority projects get Opus, maintenance work uses Sonnet/Haiku |
| **By task type** | Code generation → Sonnet, review/testing → Haiku, architecture → Opus |
| **Buffer** | Reserve 15-20% for unexpected needs (production incidents, etc.) |

### Cost Forecasting

```
Monthly cost ≈ developers × avg daily tokens × work days × price

Example:
- 10-person team, 100K tokens/day avg (Sonnet)
- Monthly ≈ 10 × 100K × 22 × $3/M input + $15/M output
- Roughly $800-1500/month (depends on input/output ratio)
```

### Consumption Anomaly Alerts

- Set daily/weekly spend thresholds with automatic notifications
- Watch for sudden spikes — usually infinite loops, oversized file inputs, or agents stuck retrying
- Periodically review top consumers to find more economical usage patterns

---

## Model Migration Strategy

When a new model launches (e.g., Sonnet 4.6 → next gen), don't switch everyone at once.

### Four-Step Gradual Migration

1. **Evaluate**: Compare new vs old on representative tasks (code quality, speed, cost)
2. **Canary**: Switch 10-20% of developers first, collect feedback for 1-2 weeks
3. **Validate**: Compare CI pass rates, bug rates, developer satisfaction between groups
4. **Rollout**: After confirming no regression, switch everyone; keep old model API key as fallback

### Prompt Compatibility Check

Model upgrades may cause the same CLAUDE.md to produce different results:
- Export AI outputs from a set of "standard tasks" as a baseline before upgrading
- Run the same tasks after upgrading and compare output differences
- Key areas: code style changes, tool calling behavior, constraint adherence

---

[← Previous: CI/CD Integration](12-cicd-integration.md) | [Table of Contents](../../README.md) | [Next: Debugging AI Code →](14-debugging-ai-code.md)
