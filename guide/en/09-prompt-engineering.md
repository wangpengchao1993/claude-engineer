# Prompt Engineering for Claude

> Get dramatically better results from Claude by structuring your prompts effectively. From basic techniques to advanced patterns.

## Table of Contents

- [Core Principles](#core-principles)
- [Prompt Structure](#prompt-structure)
- [Claude-Specific Techniques](#claude-specific-techniques)
- [Prompting for Code](#prompting-for-code)
- [System Prompts](#system-prompts)
- [Advanced Patterns](#advanced-patterns)
- [Common Mistakes](#common-mistakes)
- [Templates](#templates)

---

## Core Principles

### 1. Be Specific

The #1 rule. Vague prompts get vague results.

```
# Bad
"improve this code"

# Good
"refactor the UserService.createUser() method to:
 1. validate email format before database insert
 2. hash the password using bcrypt with 12 rounds
 3. return a UserDTO instead of the raw database model"
```

### 2. Provide Context

Claude doesn't know what you know. Share relevant background:

```
# Bad
"fix the auth bug"

# Good
"Users are getting 401 errors after their JWT expires even though the
refresh token is still valid. The auth middleware is in src/middleware/auth.ts
and the token refresh logic is in src/services/auth.ts. The refresh endpoint
works fine when tested directly — the issue seems to be in how the middleware
handles expired access tokens."
```

### 3. Show, Don't Just Tell

Examples are worth more than descriptions:

```
# Bad
"format the output nicely"

# Good
"Format each entry like this:

[2024-01-15] ERROR  auth/login — Invalid credentials for user@example.com
[2024-01-15] WARN   api/rate  — Rate limit approaching for IP 192.168.1.1

Left-align the date, fixed-width the level (5 chars), and right-pad the source."
```

### 4. Constrain the Output

Tell Claude what you want AND what you don't want:

```
"Generate a Python function that parses CSV files.

Requirements:
- Use the csv module from stdlib only
- Handle UTF-8 BOM
- Return list of dicts with column headers as keys
- Raise ValueError for malformed rows

Constraints:
- No pandas or external dependencies
- No type: ignore comments
- Under 30 lines
- Include docstring"
```

---

## Prompt Structure

### The Effective Prompt Template

```
[Role — who should Claude be?]
[Context — what's the background?]
[Task — what specifically to do?]
[Format — how should the output look?]
[Constraints — what to avoid?]
[Examples — show the expected result]
```

Not every prompt needs all sections. Use what's relevant.

### Simple Task

```
Add a rate limiter to the /api/login endpoint.
Use express-rate-limit, max 5 attempts per IP per 15 minutes.
Return 429 with message "Too many login attempts, try again later."
```

### Complex Task

```
You are a senior backend engineer reviewing code for production readiness.

Context: We're launching a payment processing service next week. The code
handles credit card charges via Stripe and must be PCI-compliant.

Task: Review src/payments/charge.ts and identify:
1. Security vulnerabilities
2. Error handling gaps
3. Edge cases that could cause incorrect charges
4. Missing logging for audit trails

Format: List each finding as:
- [SEVERITY: HIGH/MEDIUM/LOW] File:Line — Description
- Suggested fix (code snippet)

Focus only on correctness and security. Don't comment on style or naming.
```

---

## Claude-Specific Techniques

### 1. XML Tags for Structure

Claude is trained to understand XML tags exceptionally well. Use them to separate sections:

```
<context>
This is a React 18 application using TypeScript and Zustand for state management.
The component tree follows atomic design principles.
</context>

<current_code>
// paste the current implementation here
</current_code>

<task>
Refactor the ShoppingCart component to:
1. Split into smaller sub-components (CartItem, CartSummary, CartActions)
2. Move business logic to a custom hook (useCart)
3. Add proper TypeScript types for all props
</task>

<constraints>
- Keep all components in the same file for now
- Don't change the Zustand store interface
- Maintain the same visual appearance
</constraints>
```

### 2. Chain of Thought

For complex reasoning, explicitly ask Claude to think through the problem:

```
"Think step by step about how the request flows through our middleware stack:

1. What happens when a request hits the nginx proxy?
2. How does it reach our Express app?
3. What middleware runs in what order?
4. Where could the timeout be occurring?

Then suggest the most likely cause and fix."
```

### 3. Prefilling the Response

Guide Claude's output format by starting its response (API only):

```python
messages = [
    {"role": "user", "content": "List the top 5 security issues in this code"},
    {"role": "assistant", "content": "## Security Audit Results\n\n### Finding 1:"}
]
```

### 4. Extended Thinking

For truly complex problems, enable extended thinking to let Claude reason internally before responding:

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=8000,
    thinking={
        "type": "enabled",
        "budget_tokens": 5000  # tokens for internal reasoning
    },
    messages=[{"role": "user", "content": "Design the database schema for..."}]
)
```

### 5. Multi-Turn Refinement

Don't try to get everything in one prompt. Iterate:

```
Turn 1: "Implement a basic WebSocket server for real-time chat"
Turn 2: "Add authentication — users must send a JWT on connection"
Turn 3: "Add rooms — users can join/leave rooms, messages go to room members only"
Turn 4: "Add typing indicators and read receipts"
```

Each turn builds on the previous, with Claude maintaining full context.

---

## Prompting for Code

### Code Generation

```
"Write a Python function `parse_duration(s: str) -> int` that converts
human-readable duration strings to seconds.

Examples:
- '5m' → 300
- '2h30m' → 9000
- '1d12h' → 129600
- '500ms' → 0 (round down sub-second)

Handle: d, h, m, s, ms units. Raise ValueError for invalid input.
Include type hints and a docstring."
```

### Code Review

```
"Review this pull request diff for:
1. Bugs — logic errors, off-by-one, null handling
2. Security — injection, auth bypass, data exposure
3. Performance — N+1 queries, unnecessary allocations
4. Maintainability — unclear names, missing error messages

For each finding, explain the issue and show the fix.
Skip style/formatting comments."
```

### Debugging

```
"This code throws 'TypeError: Cannot read property 'id' of undefined'
at line 42 of src/api/orders.ts.

The input data looks like:
{
  "items": [{"productId": "abc", "qty": 2}],
  "customer": null  // <-- this is sometimes null for guest checkouts
}

Find the bug and fix it. Handle the null customer case gracefully."
```

### Refactoring

```
"Refactor this 200-line function into smaller, testable functions.

Rules:
- Each extracted function should do one thing
- Preserve the existing behavior exactly
- Keep functions in the same file
- Add type annotations to extracted functions
- Name functions descriptively (no 'helper1', 'processData', etc.)"
```

---

## System Prompts

System prompts set persistent behavior. Use them in the API or `CLAUDE.md`:

### Code Reviewer

```
You are a senior engineer performing code review. Focus on:
- Correctness and edge cases
- Security vulnerabilities
- Performance bottlenecks
- Clear, maintainable code

Be direct and specific. For every issue, show the fix.
Don't comment on style unless it impacts readability.
Praise good patterns when you see them.
```

### Technical Writer

```
You are a technical documentation writer. Your output should be:
- Clear and concise — no filler words
- Structured with headers and bullet points
- Includes code examples for every concept
- Appropriate for intermediate developers

Use active voice. Start instructions with verbs.
"Configure the database" not "The database can be configured by".
```

### Data Analyst

```
You are a data analyst working with SQL and Python.
When analyzing data:
- Start with understanding the schema
- Write queries that are readable and well-commented
- Explain your reasoning before showing results
- Visualize with matplotlib/seaborn when appropriate
- Always check for null values and edge cases in data
```

---

## Advanced Patterns

### Few-Shot Prompting

Provide input-output examples to establish patterns:

```
"Convert these API error messages to user-friendly messages.

Examples:
Input: "UNIQUE_VIOLATION: duplicate key value violates unique constraint"
Output: "An account with this email already exists. Try logging in instead."

Input: "FOREIGN_KEY_VIOLATION: insert or update on table violates foreign key"
Output: "The item you referenced no longer exists. Please refresh and try again."

Now convert:
Input: "CHECK_VIOLATION: new row violates check constraint on column 'age'"
```

### Persona + Constraints

```
"You are a Rust expert helping a developer migrate from Python.

When I show you Python code, provide the Rust equivalent with:
- Explanations of ownership/borrowing concepts when relevant
- Comparison to the Python version so I understand the differences
- Error handling with Result<T, E> instead of exceptions
- idiomatic Rust patterns, not direct translations

Keep explanations brief — I understand programming, just not Rust-specific concepts."
```

### Adversarial Prompting for Testing

```
"Act as a malicious user trying to break this input validation.
For each field in the form (email, name, age, bio):
1. List 5 edge case inputs that might bypass validation
2. Explain what could go wrong if they succeed
3. Suggest the fix

Be creative — think SQL injection, XSS, buffer overflow,
unicode tricks, and format string attacks."
```

### Meta-Prompting

Ask Claude to write prompts:

```
"I need to use Claude's API to automatically generate changelog entries
from git commit messages. Write me an optimized system prompt and
user prompt template that will produce clean, user-facing changelogs
grouped by category (Features, Fixes, Breaking Changes)."
```

---

## Common Mistakes

### 1. Over-Prompting

```
# Bad — too many instructions make Claude confused
"Write a function. Make sure it's clean. Use good names. Add comments.
Handle errors. Make it fast. Write tests. Use TypeScript. Follow SOLID.
Add logging. Make it extensible. Document the API. Consider edge cases.
Think about backwards compatibility..."

# Good — focused and clear
"Write a TypeScript function that validates email addresses.
Use a regex that handles common formats (user+tag@domain.co.uk).
Return { valid: boolean, reason?: string }."
```

### 2. Being Too Abstract

```
# Bad
"implement best practices for the codebase"

# Good
"add input validation to all API endpoints in src/api/ using Zod schemas"
```

### 3. Not Providing Examples

For any output format that matters, show an example. Don't assume Claude will match your mental model.

### 4. Ignoring Context Window

Don't paste 10,000 lines of code and ask "what's wrong?" Instead:
- Narrow down the relevant section
- Describe the symptoms
- Point to specific files/functions

---

## Templates

Ready-to-use prompt templates for common tasks:

- [Code Review Prompt](../../templates/system-prompts/code-reviewer.md)
- [Technical Writer Prompt](../../templates/system-prompts/technical-writer.md)
- [Data Analyst Prompt](../../templates/system-prompts/data-analyst.md)

---

<p align="center">
  <strong>Next:</strong> <a href="10-advanced-workflows.md">Advanced Workflows</a> — Complex real-world automation
</p>

---

## Prompt Version Management

When AI is deeply integrated into your workflow, prompts are code — they need version control just like code.

### CLAUDE.md Is Naturally Versioned

CLAUDE.md lives in git, giving it full version history for free:

```bash
# View CLAUDE.md change history
git log --oneline CLAUDE.md

# Compare two versions
git diff abc123..def456 CLAUDE.md

# Rollback to a previous version
git checkout abc123 -- CLAUDE.md
```

### System Prompt Change Tracking

For system prompts used in API calls:
- Store system prompts as separate files (e.g., `prompts/review.md`) in git
- Document why each change was made: "Added security review constraint because AI missed SQL injection 3 times"
- Before major changes, A/B compare old vs new prompt output quality

### Team Prompt Conventions

```markdown
# prompts/CHANGELOG.md

## 2025-05-20
- review.md: Added "must check error handling" constraint (missed 3 times)
- CLAUDE.md: Removed outdated API path descriptions

## 2025-05-10
- CLAUDE.md: Added database migration constraint (src/legacy/ is off-limits)
```

---

[← Previous: Agent SDK](08-agent-sdk.md) | [Table of Contents](../../README.md) | [Next: Advanced Workflows →](10-advanced-workflows.md)
