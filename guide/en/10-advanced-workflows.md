# Advanced Workflows

> Real-world automation patterns combining Claude Code, API, hooks, and multi-agent strategies for production use.

## Table of Contents

- [Automated Code Review Pipeline](#automated-code-review-pipeline)
- [Test-Driven Development Workflow](#test-driven-development-workflow)
- [Documentation Generation](#documentation-generation)
- [Migration Assistant](#migration-assistant)
- [Incident Response Agent](#incident-response-agent)
- [Continuous Code Quality](#continuous-code-quality)
- [Release Management](#release-management)

---

## Automated Code Review Pipeline

### Full CI/CD Review Bot

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Claude Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR for:
            1. Bugs and logic errors
            2. Security vulnerabilities
            3. Performance issues
            4. Missing tests for new functionality

            Changed files: ${{ steps.changed.outputs.files }}

            Be specific and actionable. For each issue, show the fix.
```

### Custom Review Script with Categories

```bash
#!/bin/bash
# scripts/review-pr.sh

set -e

BASE_BRANCH="${1:-main}"
DIFF=$(git diff "origin/$BASE_BRANCH...HEAD")

# Security review
echo "## Security Review"
echo "$DIFF" | claude -p \
  --system-prompt "You are a security auditor. Focus ONLY on security issues: injection, auth bypass, data exposure, SSRF, path traversal. Ignore code style." \
  "Review this diff for security vulnerabilities. Output findings as markdown."

echo ""

# Logic review
echo "## Logic Review"
echo "$DIFF" | claude -p \
  --system-prompt "You are a senior developer. Focus ONLY on bugs: logic errors, race conditions, null handling, edge cases. Ignore style and security." \
  "Review this diff for bugs and logic issues. Output findings as markdown."

echo ""

# Test coverage check
echo "## Test Coverage"
echo "$DIFF" | claude -p \
  --system-prompt "You are a QA engineer. Check if the changes have adequate test coverage." \
  "Are there sufficient tests for these changes? What's missing?"
```

---

## Test-Driven Development Workflow

### TDD with Claude Code

A structured workflow for test-driven development:

```
Step 1: "Write a failing test for [feature description]"
        Claude writes the test → test fails → confirms it tests the right thing

Step 2: "Now implement the minimum code to make the test pass"
        Claude implements → test passes

Step 3: "Refactor the implementation while keeping tests green"
        Claude refactors → runs tests → confirms they pass
```

### Automated TDD Script

```bash
#!/bin/bash
# scripts/tdd.sh — TDD workflow with Claude

FEATURE="$1"

if [ -z "$FEATURE" ]; then
    echo "Usage: ./scripts/tdd.sh 'feature description'"
    exit 1
fi

echo "=== TDD: $FEATURE ==="

# Step 1: Write failing test
echo "--- Writing test ---"
claude -p "Write a failing test for: $FEATURE. Only output the test code, no implementation." \
  --system-prompt "You are doing TDD. Write minimal, focused tests. Use the project's existing test patterns."

echo ""
echo "--- Running test (should fail) ---"
npm test 2>&1 | tail -10

# Step 2: Implement
echo ""
echo "--- Implementing ---"
claude -p "The test was written. Now implement the minimum code to make it pass." -c

echo ""
echo "--- Running test (should pass) ---"
npm test 2>&1 | tail -10

echo ""
echo "=== TDD cycle complete ==="
```

---

## Documentation Generation

### API Documentation from Code

```bash
#!/bin/bash
# Generate API documentation from source code

# Find all route files
ROUTES=$(find src/api -name "*.ts" -o -name "*.py" | sort)

echo "# API Documentation" > docs/api.md
echo "" >> docs/api.md
echo "Generated on $(date -I)" >> docs/api.md
echo "" >> docs/api.md

for route_file in $ROUTES; do
    echo "Documenting: $route_file"
    cat "$route_file" | claude -p \
      --system-prompt "Generate API documentation in markdown. For each endpoint include: method, path, description, request body (if any), response format, error codes. Use tables for parameters." \
      "Document all API endpoints in this file." >> docs/api.md
    echo "" >> docs/api.md
done
```

### Changelog Generation

```bash
#!/bin/bash
# Generate changelog from git commits since last tag

LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")
COMMITS=$(git log "$LAST_TAG"..HEAD --oneline)

echo "$COMMITS" | claude -p \
  --system-prompt "Generate a user-facing changelog in markdown. Group by: Features, Bug Fixes, Breaking Changes, Other. Use bullet points. Be concise — users don't need implementation details." \
  "Generate a changelog from these commits:"
```

---

## Migration Assistant

### Database Migration Workflow

```
"I need to migrate the users table:
1. Add column 'display_name' (varchar 255, nullable)
2. Populate it from 'first_name' + ' ' + 'last_name'
3. Make it non-nullable after population
4. Add an index on display_name

Generate the migration files for Alembic, including both upgrade and downgrade.
Also generate a data migration script that runs safely on a table with 10M+ rows
(batch processing, not one big UPDATE)."
```

### Framework Migration

```bash
#!/bin/bash
# Migrate Express routes to Fastify — one file at a time

find src/routes -name "*.ts" | while read file; do
    echo "Migrating: $file"

    claude -p "Convert this Express route file to Fastify.

Rules:
- Convert router.get/post/etc to fastify.get/post/etc
- Convert req.body to request.body (typed with schema)
- Convert res.json() to reply.send()
- Add JSON schema for request validation
- Keep the same business logic
- Add TypeScript types for request/reply

Output ONLY the converted file, no explanation." < "$file" > "${file}.new"

    # Review before replacing
    diff "$file" "${file}.new" | head -50
    echo ""
    echo "Replace $file? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        mv "${file}.new" "$file"
    else
        rm "${file}.new"
    fi
done
```

---

## Incident Response Agent

### On-Call Assistant

```python
from claude_agent_sdk import Agent, tool
import subprocess

@tool
def check_service_health(service: str) -> dict:
    """Check health endpoint of a service."""
    result = subprocess.run(
        ["curl", "-s", "-w", "%{http_code}", f"http://{service}/health"],
        capture_output=True, text=True, timeout=5
    )
    return {"status_code": result.stdout[-3:], "body": result.stdout[:-3]}

@tool
def get_recent_logs(service: str, lines: int = 100) -> str:
    """Get recent logs from a service."""
    result = subprocess.run(
        ["kubectl", "logs", f"deployment/{service}", "--tail", str(lines)],
        capture_output=True, text=True
    )
    return result.stdout

@tool
def get_metrics(service: str, metric: str, duration: str = "5m") -> dict:
    """Query Prometheus metrics for a service."""
    # Implementation with your metrics system
    ...

@tool
def restart_service(service: str) -> dict:
    """Restart a service deployment (requires confirmation)."""
    # Implementation with k8s rollout restart
    ...

incident_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_service_health, get_recent_logs, get_metrics, restart_service],
    system_prompt="""You are an on-call incident response assistant.

    When investigating an issue:
    1. Check service health first
    2. Look at recent logs for errors
    3. Check key metrics (error rate, latency, CPU, memory)
    4. Identify the root cause
    5. Suggest remediation steps

    Only restart services as a last resort after confirming with the user.
    Always explain your reasoning.
    """,
    max_turns=30,
)

# Usage during an incident
result = incident_agent.run(
    "The API is returning 503 errors. User reports started 10 minutes ago."
)
```

---

## Continuous Code Quality

### Pre-Commit Quality Gate

```bash
#!/bin/bash
# .git/hooks/pre-commit

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|py|rs)$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Quick quality check with Claude
DIFF=$(git diff --cached)
RESULT=$(echo "$DIFF" | claude -p \
  --max-turns 1 \
  --system-prompt "You are a quick code quality checker. Only flag CRITICAL issues: security vulnerabilities, obvious bugs, or data loss risks. Reply 'PASS' if no critical issues found. Otherwise list the critical issues briefly." \
  "Quick review:")

if [[ "$RESULT" == *"PASS"* ]]; then
    echo "Quality check: PASS"
    exit 0
else
    echo "Quality check found issues:"
    echo "$RESULT"
    echo ""
    echo "Commit anyway? (y/n)"
    exec < /dev/tty
    read -r answer
    if [ "$answer" != "y" ]; then
        exit 1
    fi
fi
```

### Periodic Codebase Health Check

```bash
#!/bin/bash
# scripts/health-check.sh — Run weekly via cron

REPORT_FILE="reports/health-$(date -I).md"

echo "# Codebase Health Report — $(date -I)" > "$REPORT_FILE"

# Check for TODOs and FIXMEs
echo "## Outstanding TODOs" >> "$REPORT_FILE"
grep -rn "TODO\|FIXME\|HACK\|XXX" src/ --include="*.ts" --include="*.py" 2>/dev/null | \
  claude -p "Categorize these TODOs by urgency (critical/medium/low) and summarize." >> "$REPORT_FILE"

# Check dependency freshness
echo "## Dependencies" >> "$REPORT_FILE"
if [ -f "package.json" ]; then
    npx npm-check-updates 2>/dev/null | \
      claude -p "Summarize which dependencies are outdated and which updates are breaking." >> "$REPORT_FILE"
fi

# Check test coverage
echo "## Test Coverage" >> "$REPORT_FILE"
npm test -- --coverage 2>&1 | \
  claude -p "Summarize the test coverage. Highlight files with <50% coverage." >> "$REPORT_FILE"

echo "Report saved to $REPORT_FILE"
```

---

## Release Management

### Automated Release Notes

```bash
#!/bin/bash
# scripts/release.sh

VERSION="$1"
if [ -z "$VERSION" ]; then
    echo "Usage: ./scripts/release.sh v1.2.3"
    exit 1
fi

LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
COMMITS=$(git log "${LAST_TAG}..HEAD" --oneline --no-merges)
DIFF_STAT=$(git diff "$LAST_TAG"..HEAD --stat)

NOTES=$(echo "Commits:
$COMMITS

Diff stats:
$DIFF_STAT" | claude -p \
  --system-prompt "Generate professional release notes. Sections: Highlights (1-2 sentences), What's New (features), Bug Fixes, Breaking Changes (if any). User-facing language, not developer jargon." \
  "Generate release notes for version $VERSION:")

echo "$NOTES"

echo ""
echo "Create release $VERSION with these notes? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    echo "$NOTES" | gh release create "$VERSION" --title "$VERSION" --notes-file -
    echo "Release $VERSION created!"
fi
```

### PR Description Generator

```bash
#!/bin/bash
# Generate a PR description from branch changes

BASE="${1:-main}"
BRANCH=$(git branch --show-current)
COMMITS=$(git log "origin/$BASE..$BRANCH" --oneline)
DIFF=$(git diff "origin/$BASE...$BRANCH" --stat)
FULL_DIFF=$(git diff "origin/$BASE...$BRANCH")

DESCRIPTION=$(echo "Branch: $BRANCH
Base: $BASE

Commits:
$COMMITS

Changed files:
$DIFF

Full diff:
$FULL_DIFF" | claude -p \
  --system-prompt "Generate a concise PR description with: Summary (2-3 bullet points), Changes (grouped by area), Test Plan (what to verify). Use markdown." \
  "Generate PR description:")

echo "$DESCRIPTION"
```

---

## Combining Patterns

The real power comes from combining these workflows:

```
1. Feature branch created
2. Developer works with Claude Code (interactive)
3. Pre-commit hook does quick quality check
4. PR created with auto-generated description
5. CI runs Claude review + tests
6. On merge, changelog auto-generated
7. On release, release notes auto-generated
```

Each step uses Claude in a different way — interactive, scripted, and CI-integrated — creating a seamless development experience.

---

<p align="center">
  <strong>Start from the beginning:</strong> <a href="01-getting-started.md">Getting Started</a>
</p>
