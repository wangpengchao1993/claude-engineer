# Team Collaboration with AI

> Practical workflows for integrating AI into team development processes: roles, PR lifecycles, shared configuration, onboarding, code ownership, and knowledge sharing.

## Table of Contents

- [AI Roles in a Team](#ai-roles-in-a-team)
- [PR Workflow with AI](#pr-workflow-with-ai)
- [Shared CLAUDE.md Management](#shared-claudemd-management)
- [Onboarding New Developers](#onboarding-new-developers)
- [Code Ownership and Review](#code-ownership-and-review)
- [Knowledge Sharing](#knowledge-sharing)
- [Anti-patterns to Avoid](#anti-patterns-to-avoid)

---

## AI Roles in a Team

AI fits into team workflows in three distinct roles. Choosing the right role for each situation is the key to effective collaboration.

### AI as Author

The developer describes the task; Claude Code writes the implementation.

```bash
# Developer provides intent, AI writes code
claude "Create a rate limiter middleware for Express that:
- Uses sliding window algorithm
- Stores state in Redis
- Returns 429 with Retry-After header
- Has per-route configuration"
```

Best for: boilerplate, well-specified features, CRUD operations, test generation.

### AI as Reviewer

The developer writes code; Claude Code reviews it before the PR.

```bash
# Review staged changes before committing
git diff --staged | claude "Review this diff for:
- Security issues
- Performance problems
- Missing edge cases
- Convention violations per our CLAUDE.md"
```

Best for: catching bugs, enforcing standards, security review, documentation gaps.

### AI as Pair Programmer

Developer and AI work interactively, alternating between human decisions and AI execution.

```bash
# Interactive session where developer guides direction
claude
> Let's refactor the payment module. First show me the current structure.
> OK, I want to extract the Stripe logic into a separate adapter. Start with the interface.
> Good. Now implement the adapter. Keep the error mapping from the old code.
> Add tests for the error cases we discussed.
```

Best for: complex refactoring, architectural decisions, exploratory work, learning new codebases.

### Role Selection Matrix

| Situation | AI Role | Human Role |
|-----------|---------|------------|
| New CRUD endpoint | Author | Review output |
| Security-sensitive code | Reviewer | Write code |
| Complex refactor | Pair Programmer | Guide decisions |
| Bug investigation | Pair Programmer | Confirm diagnosis |
| Writing tests | Author | Verify coverage |
| Performance optimization | Reviewer | Profile and implement |

---

## PR Workflow with AI

### Complete PR Lifecycle

The recommended flow integrates AI at multiple stages without removing human judgment.

```
Developer                 Claude Code              GitHub                  Team
    |                         |                       |                     |
    |--- describe task ------>|                       |                     |
    |<-- implement + tests ---|                       |                     |
    |--- review locally ----->|                       |                     |
    |<-- fix issues ----------|                       |                     |
    |                         |                       |                     |
    |--- git push ------------|---------------------> |                     |
    |                         |                       |--- CI runs -------->|
    |                         |<-- auto-review (GH Action) ---|            |
    |                         |--- posts comments --->|                     |
    |                         |                       |--- notify team ---->|
    |                         |                       |                     |
    |                         |                       |<-- human reviews ---|
    |                         |                       |    (reviews AI's    |
    |                         |                       |     review too)     |
    |                         |                       |                     |
    |<-- address feedback ----|                       |<-- approve/request--|
    |--- push fixes --------->|---------------------> |                     |
    |                         |                       |<-- merge ---------- |
```

### GitHub Action for AI Review

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > /tmp/pr-diff.txt

      - name: Run Claude Code review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cat /tmp/pr-diff.txt | claude -p \
            "Review this PR diff. Focus on:
             1. Bugs and logic errors
             2. Security vulnerabilities
             3. Performance issues
             4. Missing tests
             Format as GitHub PR review comments." \
            > /tmp/review.md

      - name: Post review comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('/tmp/review.md', 'utf8');
            await github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: review,
              event: 'COMMENT'
            });
```

### Human Review of AI Reviews

When reviewing an AI-generated review, check for:

```markdown
## AI Review Checklist (for human reviewers)

- [ ] Does the AI review identify real issues (not false positives)?
- [ ] Are the AI's suggestions actually better than the original?
- [ ] Did the AI miss anything obvious?
- [ ] Are the AI's comments actionable (not vague)?
- [ ] Does the AI understand the business context?
```

---

## Shared CLAUDE.md Management

### Three-Layer Configuration

A team needs shared conventions (committed) and personal preferences (gitignored). Use a layered approach.

```
project-root/
  CLAUDE.md                          # Team-wide (committed)
  packages/
    auth/
      CLAUDE.md                      # Module-specific (committed)
    api/
      CLAUDE.md                      # Module-specific (committed)
  .claude/
    settings.json                    # Shared tool permissions (committed)
    settings.local.json              # Personal preferences (gitignored)
```

### Root CLAUDE.md: Team Conventions

```markdown
# Project: Acme Platform

## Tech Stack
- TypeScript 5.x, Node.js 20 LTS
- React 18 with Next.js 14 (App Router)
- PostgreSQL 16 with Drizzle ORM
- Redis for caching and rate limiting

## Coding Conventions
- Use named exports, never default exports
- All functions must have JSDoc with @param and @returns
- Error handling: use Result<T, E> pattern, never throw in library code
- Database queries: always use parameterized queries via Drizzle
- API responses: always use the ApiResponse<T> wrapper from src/lib/api

## Testing
- Unit tests: Vitest, colocated as *.test.ts
- Integration tests: in __tests__/ directories
- Minimum 80% branch coverage for new code

## Git
- Conventional commits: feat|fix|chore|docs(scope): message
- PR title matches commit convention
- Squash merge to main
```

### Module-Level CLAUDE.md

```markdown
# packages/auth/CLAUDE.md

## Purpose
Authentication and authorization module. Handles JWT tokens,
session management, OAuth providers, and RBAC.

## Key Files
- src/jwt.ts: Token creation and verification
- src/providers/: OAuth provider adapters (Google, GitHub)
- src/rbac.ts: Role-based access control middleware
- src/session.ts: Session store (Redis-backed)

## Conventions Specific to This Module
- All token expiry values come from config, never hardcoded
- OAuth secrets are loaded from environment variables only
- RBAC permissions are defined in src/permissions.ts, nowhere else
- Always use the AuthError class for auth-related errors
```

### Personal Settings (gitignored)

```jsonc
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(docker compose *)"
    ]
  }
}
```

### Keeping Configurations in Sync

```bash
# Add to your CI pipeline: validate CLAUDE.md consistency
# scripts/validate-claude-md.sh

#!/bin/bash
set -e

# Check root CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
  echo "ERROR: Root CLAUDE.md is missing"
  exit 1
fi

# Check all packages have a CLAUDE.md
for pkg in packages/*/; do
  if [ ! -f "${pkg}CLAUDE.md" ]; then
    echo "WARNING: ${pkg} is missing a CLAUDE.md"
  fi
done

# Check for common issues
if grep -r "API_KEY\|SECRET\|PASSWORD" CLAUDE.md packages/*/CLAUDE.md 2>/dev/null; then
  echo "ERROR: Potential secret found in CLAUDE.md files"
  exit 1
fi

echo "CLAUDE.md validation passed"
```

---

## Onboarding New Developers

### Day 1: Understand the Codebase

```bash
# First thing a new developer does
claude "Explain this codebase to me. Cover:
1. What does this project do?
2. How is it structured?
3. What are the main entry points?
4. How do I run it locally?
5. Where are the tests?"
```

### Day 1: Understand the Conventions

```bash
# Point them to CLAUDE.md
claude "Read the CLAUDE.md files in this repo and summarize:
1. What coding conventions does this team follow?
2. What testing patterns are expected?
3. What are the common pitfalls mentioned?"
```

### First Week: Guided Tasks

```bash
# Small bug fix with AI guidance
claude "I'm new to this codebase. Help me fix issue #234.
Walk me through:
1. Where the bug likely lives
2. How to reproduce it
3. The fix
4. What tests to add"
```

```bash
# First feature with AI pair programming
claude "I need to add a /health endpoint to the API.
Show me similar endpoints in this codebase first,
then help me follow the same pattern."
```

### Onboarding Checklist Template

```markdown
## New Developer Onboarding with Claude Code

### Setup (Day 1)
- [ ] Clone repo and install dependencies
- [ ] Run `claude "explain this codebase"` for overview
- [ ] Read root CLAUDE.md for team conventions
- [ ] Set up personal .claude/settings.local.json
- [ ] Run the test suite with `claude "run all tests and explain any failures"`

### First Tasks (Week 1)
- [ ] Fix a small bug using Claude Code as pair programmer
- [ ] Add tests to an under-tested module
- [ ] Create a small feature following existing patterns

### Integration (Week 2)
- [ ] Review an AI-generated PR using the team checklist
- [ ] Create your first PR with Claude Code assistance
- [ ] Add a module-level CLAUDE.md for code you now own
```

---

## Code Ownership and Review

### Who Is Responsible for AI-Authored Code?

The developer who prompted the AI is responsible. Always.

```
Rule: If you prompted it, you own it.

- You review it before committing
- You ensure it passes tests
- You maintain it going forward
- You answer questions about it in code review
```

### Review Checklist for AI-Generated PRs

AI-generated code has different failure modes than human code. Use this checklist.

```markdown
## AI-Generated PR Review Checklist

### Correctness
- [ ] Does it actually solve the stated problem?
- [ ] Are edge cases handled (null, empty, boundary values)?
- [ ] Does it integrate correctly with existing code?
- [ ] Are error messages helpful (not generic)?

### Patterns
- [ ] Does it follow the project's established patterns?
- [ ] Are there unnecessary abstractions (AI loves over-engineering)?
- [ ] Is it using the project's existing utilities (not reimplementing)?
- [ ] Are imports from the correct internal packages?

### Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation is present
- [ ] SQL queries are parameterized
- [ ] Auth checks are in place

### Testing
- [ ] Tests cover the actual behavior (not just happy path)
- [ ] Test assertions are meaningful (not just "it doesn't throw")
- [ ] Mocks are realistic (not overly simplified)
- [ ] Edge case tests exist

### AI-Specific Issues
- [ ] No hallucinated APIs or methods that don't exist
- [ ] No outdated patterns from training data
- [ ] No unnecessary comments explaining obvious code
- [ ] No placeholder "TODO" items that should be implemented
```

### When to Reject AI Code

Reject and rewrite when:

```
1. The AI invented APIs that don't exist in your dependencies
2. The approach is fundamentally wrong (right code, wrong solution)
3. It reimplements something your codebase already has
4. Security-critical code that needs line-by-line human authorship
5. The code is correct but unmaintainable (too clever)
6. Test mocks don't reflect real behavior
```

---

## Knowledge Sharing

### Using Sessions as Documentation

```bash
# After a complex debugging session, capture the findings
claude "Summarize what we just did in this session:
- What was the bug?
- What was the root cause?
- What was the fix?
- What should we watch for in the future?
Write this as a post-mortem doc."
```

### Recording Architectural Decisions

```bash
# Use Claude Code to create ADRs (Architecture Decision Records)
claude "We just decided to switch from REST to GraphQL for the
internal API. Create an ADR document that captures:
- Context: why we considered this
- Decision: what we chose
- Consequences: what changes
- Migration plan: how we get there
Follow the ADR template in docs/adr/"
```

### Team Retrospectives on AI Effectiveness

Track these metrics monthly:

```markdown
## AI Effectiveness Retrospective Template

### Metrics
- PRs created with AI assistance: ___
- PRs that needed significant human rework: ___
- Average review cycles for AI PRs vs human PRs: ___
- Time saved estimate (hours/week/developer): ___

### What Worked
- Tasks where AI saved the most time
- Prompts or workflows worth sharing

### What Didn't Work
- Tasks where AI was counterproductive
- Common failure modes this month

### Action Items
- Update CLAUDE.md with new conventions
- Share effective prompts in team wiki
- Adjust AI role selection for specific task types
```

---

## Anti-patterns to Avoid

### 1. Blindly Trusting AI Output

```bash
# BAD: Accept everything without review
claude "implement the payment flow" && git add -A && git commit -m "feat: payments"

# GOOD: Review before committing
claude "implement the payment flow"
# Developer reads every line of generated code
# Developer runs tests manually
# Developer commits only after understanding the code
git add -A && git commit -m "feat: add payment flow with Stripe integration"
```

### 2. AI as a Crutch

```
Signs your team is over-relying on AI:
- Developers can't explain code they committed
- Nobody reads the AI output before merging
- "Claude wrote it" is an accepted answer in code review
- Test coverage is high but tests don't catch real bugs
- New developers skip learning the codebase ("just ask Claude")
```

### 3. Not Reviewing AI Output

```bash
# The "vibe coding" trap - shipping without understanding
# This leads to:
# - Security vulnerabilities in production
# - Subtle bugs that tests don't catch
# - Technical debt that nobody understands
# - Incidents where nobody can debug the code

# Fix: establish a team rule
# "If you can't explain every line to a reviewer, you can't merge it."
```

### 4. Inconsistent AI Usage Across the Team

```
Problem: Each developer uses AI differently, leading to inconsistent code.

Fix: Standardize through CLAUDE.md
- Same conventions for everyone
- Same review checklist
- Same prompt patterns for common tasks
- Regular team syncs on AI workflow improvements
```

### 5. Skipping Tests Because "AI Generated Them"

```bash
# BAD: Trust AI tests without verifying
claude "add tests for the user service"
# Merge without checking if tests actually test anything

# GOOD: Verify test quality
claude "add tests for the user service"
# Manually review: Do assertions check real behavior?
# Mutation testing: Do tests fail when code is broken?
# Coverage: Are edge cases actually covered?
```

### 6. Using AI for Everything

```
Not every task benefits from AI. Know when to type it yourself:

- One-line fixes: faster to type than to describe
- Naming: humans are better at domain-specific naming
- UX decisions: AI doesn't understand your users
- Architecture: AI can propose, but humans must decide
- Code review culture: AI supplements but doesn't replace human review
```

---

## Summary

Effective team AI collaboration requires:

1. **Clear roles**: Know when AI should author, review, or pair program
2. **Structured PR workflow**: AI assists at multiple stages, humans always decide
3. **Shared configuration**: Layered CLAUDE.md keeps everyone aligned
4. **Thoughtful onboarding**: AI accelerates learning but doesn't replace it
5. **Ownership culture**: The prompter owns the code
6. **Continuous improvement**: Track and retrospect on AI effectiveness
7. **Healthy skepticism**: Review everything, trust nothing blindly

---

## Measuring AI Effectiveness

After adopting AI, teams need data to answer: "Is AI actually making us faster/better?"

### Core Metrics

| Metric | How to Measure | Healthy Range |
|--------|---------------|---------------|
| **Delivery speed change** | Compare PR merge cycle before/after AI adoption | 20-40% reduction |
| **First-pass CI rate** | % of AI-generated code passing CI on first push | > 70% |
| **Review rework rate** | % of AI code modified during review | < 30% |
| **Post-deploy bug rate** | Bugs within 7 days for AI code vs human code | Should be equal or lower |
| **Developer satisfaction** | Monthly anonymous survey (1-5 scale) | > 3.5 |

### Avoid Vanity Metrics

Don't just track "how many lines of code AI generated" — lines of code ≠ value. Focus on quality and delivery efficiency, not output volume.

## Scaling AI Across Teams

Going from 1 person using AI to 100 people isn't just copy-paste.

### Phased Rollout

| Phase | Size | Focus |
|-------|------|-------|
| Pilot | 1-3 people | Validate tools, find pitfalls, write CLAUDE.md |
| Expand | 5-15 people | Standardize config (CLAUDE.md + Hooks + permissions), establish review norms |
| Full team | Everyone | Training, measurement, continuous optimization |

### Preventing "AI Zombie Code"

The biggest risk isn't AI writing bugs — it's the team accepting AI code that nobody understands.

Prevention:
- **Review means understand**: Hold AI code to the same review standard as human code
- **Comment key decisions**: If AI used an unusual approach, require developers to add comments explaining why
- **Knowledge sharing**: Regularly share "interesting AI solutions" or "AI pitfalls" as team learning moments

---

[← Previous: Debugging AI Code](14-debugging-ai-code.md) | [Table of Contents](../../README.md) | [Next: Security & Compliance →](16-security-compliance.md)
