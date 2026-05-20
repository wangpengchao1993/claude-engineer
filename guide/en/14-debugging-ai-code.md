# Debugging AI-Generated Code

> AI writes code fast, but not always correctly. Learn to spot common AI mistakes, fix them efficiently, and build workflows that prevent them in the first place.

## Table of Contents

- [Common AI Error Types](#common-ai-error-types)
- [Detection Strategies](#detection-strategies)
- [Recovery Strategies](#recovery-strategies)
- [Prevention Patterns](#prevention-patterns)
- [When AI Gets Stuck](#when-ai-gets-stuck)
- [Real-World Debugging Session](#real-world-debugging-session)

---

## Common AI Error Types

### 1. Hallucinated APIs

AI confidently uses functions, modules, or methods that do not exist.

```typescript
// AI wrote this — looks reasonable, but crypto.timingSafeCompare doesn't exist
import crypto from 'crypto';

function verifyToken(provided: string, expected: string): boolean {
  return crypto.timingSafeCompare(provided, expected);  // ❌ Not a real function
}

// The actual function is crypto.timingSafeEqual, and it takes Buffers
import crypto from 'crypto';

function verifyToken(provided: string, expected: string): boolean {
  return crypto.timingSafeEqual(             // ✅ Correct function name
    Buffer.from(provided),                   // ✅ Needs Buffer conversion
    Buffer.from(expected)
  );
}
```

**Why it happens**: AI trained on many code examples blends similar APIs together.

**How to catch it**: TypeScript compiler, IDE hover, `tsc --noEmit`, test execution.

### 2. Outdated Syntax

AI uses deprecated or removed patterns from older versions.

```jsx
// AI wrote old-style React class component with deprecated lifecycle
class UserProfile extends React.Component {
  componentWillMount() {              // ❌ Deprecated since React 16.3
    this.fetchUser();
  }

  componentWillReceiveProps(next) {   // ❌ Deprecated since React 16.3
    if (next.userId !== this.props.userId) {
      this.fetchUser(next.userId);
    }
  }
}

// Modern equivalent
function UserProfile({ userId }: { userId: string }) {
  useEffect(() => {                   // ✅ Modern hook
    fetchUser(userId);
  }, [userId]);                       // ✅ Dependency array handles changes
}
```

**Why it happens**: Training data includes code from all eras. Older patterns appear more frequently.

**How to catch it**: Linting rules (react-hooks/exhaustive-deps), framework documentation, deprecation warnings.

### 3. Logic Errors

Code compiles and runs but produces wrong results.

```python
# AI wrote a pagination function
def get_page(items: list, page: int, per_page: int = 10) -> list:
    start = page * per_page         # ❌ Off-by-one: page 1 skips first items
    end = start + per_page
    return items[start:end]

# Page 1 returns items 10-19 instead of 0-9!

# Correct version
def get_page(items: list, page: int, per_page: int = 10) -> list:
    start = (page - 1) * per_page   # ✅ Page 1 starts at index 0
    end = start + per_page
    return items[start:end]
```

**Why it happens**: AI generates plausible-looking code without "running" it mentally. Off-by-one, wrong comparison operators, and inverted conditions are common.

**How to catch it**: Unit tests with boundary values, manual trace-through, test-driven development.

### 4. Missing Edge Cases

AI handles the happy path but forgets about nulls, empty inputs, errors, and boundaries.

```python
# AI wrote a user lookup
def get_user_display_name(user_id: str, db: Database) -> str:
    user = db.find_user(user_id)
    return f"{user.first_name} {user.last_name}"  # ❌ What if user is None?
                                                    # ❌ What if names are None?

# Robust version
def get_user_display_name(user_id: str, db: Database) -> str:
    user = db.find_user(user_id)
    if user is None:                               # ✅ Handle missing user
        return "Unknown User"
    first = user.first_name or ""                   # ✅ Handle None names
    last = user.last_name or ""
    name = f"{first} {last}".strip()
    return name if name else "Unnamed User"         # ✅ Handle both empty
```

**Common missed edge cases**:
```
- None/null/undefined values
- Empty strings, empty arrays, empty objects
- Zero, negative numbers
- Very large inputs (memory, timeout)
- Unicode characters (emoji in names, RTL text)
- Concurrent access (race conditions)
- Network failures (timeout, DNS, TLS errors)
- File system errors (permission, disk full, missing file)
```

### 5. Inconsistent Patterns

AI mixes different coding styles within the same file or project.

```typescript
// AI generated code with mixed patterns in one file
class UserService {
  // Pattern 1: callback style
  getUser(id: string, callback: (err: Error, user: User) => void) {
    db.find(id, callback);
  }

  // Pattern 2: promise style
  updateUser(id: string, data: Partial<User>): Promise<User> {
    return db.update(id, data);
  }

  // Pattern 3: async/await style
  async deleteUser(id: string): Promise<void> {
    await db.delete(id);
  }
}

// Consistent version — pick one pattern and stick with it
class UserService {
  async getUser(id: string): Promise<User> {
    return await db.find(id);
  }

  async updateUser(id: string, data: Partial<User>): Promise<User> {
    return await db.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await db.delete(id);
  }
}
```

**How to catch it**: Code review, ESLint consistency rules, project-level CLAUDE.md style guidelines.

### 6. Over-Engineering

AI adds unnecessary abstraction, patterns, or complexity.

```typescript
// AI was asked to "add a logger" and created an entire framework
interface LogStrategy { log(msg: string): void; }
class ConsoleLogStrategy implements LogStrategy { /* ... */ }
class FileLogStrategy implements LogStrategy { /* ... */ }
class LogStrategyFactory { /* ... */ }
class LoggerBuilder { /* ... */ }
class Logger {
  private strategy: LogStrategy;
  private static instance: Logger;
  // ... 200 more lines
}

// What was actually needed
import pino from 'pino';
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });
export default logger;
```

**Why it happens**: AI training data includes enterprise patterns, design pattern tutorials, and textbook examples. It defaults to "thorough" rather than "simple."

**How to prevent it**: Be explicit — "use a simple approach", "no more than 30 lines", "use an existing library."

### 7. Dependency Confusion

AI imports the wrong package, wrong version, or non-existent package.

```python
# AI wrote this import
from sklearn.ensemble import GradientBoostedClassifier  # ❌ Wrong class name

# Correct
from sklearn.ensemble import GradientBoostingClassifier  # ✅

# AI suggested a package that doesn't exist (or is malicious)
pip install python-jwt        # ❌ Not the popular one
pip install PyJWT             # ✅ The widely-used JWT library

# AI mixed up package versions
import { serve } from '@hono/node-server'    # Works in Hono v3+
import { Hono } from 'hono'                  # But AI wrote Hono v2 patterns
```

**How to catch it**: `pip install` / `npm install` errors, import errors at runtime, lock file review.

---

## Detection Strategies

### Type Checking

The fastest way to catch hallucinated APIs and wrong signatures.

```bash
# TypeScript
npx tsc --noEmit
# Catches: wrong method names, wrong argument types, missing properties

# Python
mypy src/ --strict
# or
pyright src/

# Go
go vet ./...
```

**Ask Claude to run type checks**:
```
"Run tsc --noEmit and fix any type errors in the files you just changed"
```

### Linting

Catches deprecated patterns, style violations, and potential bugs.

```bash
# JavaScript/TypeScript
npx eslint src/ --fix

# Python
ruff check src/ --fix
# or
flake8 src/

# Go
golangci-lint run
```

**Pro tip**: Add lint checks to your CLAUDE.md:
```markdown
## After Every Change
- Run `npm run lint` to check for issues
- Run `npm run typecheck` to verify types
```

### Test-Driven Development (TDD)

Write tests first, then ask AI to implement. Tests catch bugs immediately.

```bash
# Step 1: Write the test yourself (or have AI write it first)
"Write a test for a function that calculates shipping cost.
 Free shipping over $50, $5.99 flat rate under $50, no negative prices."

# Step 2: Ask AI to implement
"Now implement the calculateShipping function to pass these tests"

# Step 3: Run tests
npm test

# If tests fail, AI sees the failure and can fix it
"Tests are failing — fix the implementation"
```

### AI Self-Review

Ask Claude to review its own code with fresh eyes.

```bash
# After AI writes code
"Now review the code you just wrote. Look for:
 - Missing error handling
 - Edge cases not covered
 - Security issues
 - Performance problems
 List each issue with file:line and suggested fix."

# Or use a second Claude instance
cat src/auth/*.ts | claude "Review this auth code for security issues"
```

### Static Analysis

Specialized tools catch security and quality issues.

```bash
# Security scanning
semgrep --config auto src/          # Multi-language security patterns
bandit -r src/                       # Python security linter
npm audit                            # Node.js dependency vulnerabilities

# Code quality
sonarqube-scanner                    # Comprehensive quality analysis

# Complexity analysis
npx complexity-report src/           # Cyclomatic complexity
radon cc src/ -a                     # Python complexity
```

### Runtime Testing

Some bugs only appear at runtime.

```bash
# Integration tests
npm run test:integration

# Smoke tests (hit real endpoints)
curl -s http://localhost:3000/health | jq .

# Load tests (find performance issues)
k6 run load-test.js

# Manual testing in dev
npm run dev
# Then manually test the feature
```

---

## Recovery Strategies

### See What Changed

Before fixing anything, understand what the AI changed.

```bash
# See all changes (staged and unstaged)
git diff

# See changes in a specific file
git diff src/auth/login.ts

# See what files changed
git diff --name-only

# Compare with a specific commit
git diff HEAD~3
```

### Save Work Before Reverting

```bash
# Stash current changes (reversible)
git stash
# Later: git stash pop (to restore)

# Create a backup branch
git checkout -b backup/ai-changes
git add -A && git commit -m "backup: AI changes before debugging"
git checkout main
```

### Revert Specific Files

```bash
# Revert one file to last commit
git checkout HEAD -- src/auth/login.ts

# Revert multiple specific files
git checkout HEAD -- src/auth/login.ts src/auth/middleware.ts

# Keep some changes, revert others
git add src/auth/login.ts        # Stage the file you want to keep
git checkout HEAD -- .            # Revert everything else
```

### Claude Code's Built-in Undo

```bash
# Ask Claude to undo its last change
"undo the last change"

# Undo specific changes
"revert only the changes to the auth module"

# Undo with explanation
"undo the database migration change — the schema was correct before"
```

### Session Reset

When the conversation context is polluted with wrong assumptions:

```bash
# Clear conversation and start fresh
/clear

# Or compact with specific instructions
/compact forget the auth approach we tried, it was wrong. Keep the DB schema discussion.

# Start a completely new session
# Exit and restart claude
```

### Selective Rollback

```bash
# See commit history
git log --oneline -10

# Revert a specific commit (creates a new reverse commit)
git revert abc1234

# Cherry-pick only the good commits from a branch
git cherry-pick def5678 ghi9012

# Interactive: unstage specific hunks
git reset HEAD src/auth/login.ts    # Unstage file
git add -p src/auth/login.ts        # Stage only the hunks you want
```

---

## Prevention Patterns

### 1. Small Tasks (5-Minute Chunks)

The single most effective prevention strategy. Small changes are easy to verify.

```bash
# Bad: one massive prompt
"Build the entire authentication system with JWT, refresh tokens,
 password reset, email verification, OAuth2, and rate limiting"

# Good: sequential small tasks
"Create the User model with email, passwordHash, and createdAt fields"
# Verify → commit

"Add a POST /auth/register endpoint that creates a user with hashed password"
# Verify → commit

"Add a POST /auth/login endpoint that returns a JWT"
# Verify → commit

"Add JWT middleware that validates tokens on protected routes"
# Verify → commit
```

**Rule**: If you cannot verify the output in under 5 minutes, the task is too big.

### 2. Spec-First Development

Write the specification before the code. The Superpowers/Spec-Kit pattern:

```bash
# Step 1: Write a spec
"Write a technical spec for password reset flow. Include:
 - API endpoints
 - Database changes
 - Email templates
 - Security considerations
 - Edge cases
 Save to specs/password-reset.md"

# Step 2: Review the spec yourself

# Step 3: Implement from spec
"Implement the password reset flow according to specs/password-reset.md.
 Start with the database migration."
```

### 3. TDD (Red-Green-Refactor)

```bash
# Red: write a failing test
"Write tests for a PasswordResetService. Test:
 - Generating a reset token (should be URL-safe, expire in 1 hour)
 - Using a valid token (should return success, invalidate token)
 - Using an expired token (should return error)
 - Using a token twice (should return error on second use)
 Do NOT write the implementation yet."

# Green: implement to pass tests
"Now implement PasswordResetService to pass all tests"

# Refactor: clean up
"Refactor PasswordResetService — simplify without breaking tests"
```

### 4. Incremental Commits

Commit after each verified task. This creates safe rollback points.

```bash
# After each small task:
git add src/models/user.ts
git commit -m "add User model with email and password fields"

# If the next AI change breaks something:
git diff                                # See what changed
git checkout HEAD -- src/models/user.ts # Revert just that file
```

**Commit strategy**:
```
Task 1: Add model         → verify → commit
Task 2: Add route         → verify → commit
Task 3: Add middleware     → verify → commit
Task 4: Add tests         → verify → commit

If Task 3 breaks things, you can revert to after Task 2.
```

### 5. Review at Each Step

Do not wait until the end to review all AI output.

```bash
# After each AI change:
# 1. Read the diff
git diff

# 2. Ask yourself:
#    - Does this make sense?
#    - Are there obvious edge cases?
#    - Does it follow our patterns?

# 3. Ask AI to self-review
"Review the changes you just made. Any issues?"

# 4. Run tests
npm test

# Only then: move to the next task
```

---

## When AI Gets Stuck

### Provide More Context

When AI gives wrong answers, it usually lacks context.

```bash
# Bad: no context
"Fix the auth bug"

# Good: full context
"The /api/login endpoint returns 500 when users with special characters
 in their password try to log in. Here's the error:

 TypeError: Cannot read property 'hash' of undefined
   at AuthService.login (src/services/auth.ts:45)

 The bcrypt.hash call on line 45 receives undefined because
 the password field is being URL-decoded before it reaches the service.

 The relevant files are:
 - src/routes/auth.ts (the route handler)
 - src/services/auth.ts (the login service)
 - src/middleware/parser.ts (body parsing middleware)"
```

### Switch Models

Complex problems sometimes need a more capable model.

```bash
# If Sonnet can't figure it out
/model claude-opus-4-20250514

# Then provide the full context again
"I'm debugging a race condition in the WebSocket connection manager.
 When two clients connect simultaneously with the same user ID..."
```

### Break the Problem Down

```bash
# Instead of:
"Fix the authentication system"

# Break it down:
"First, just explain what the current auth flow does.
 Read src/auth/ and describe the flow step by step."

# Then:
"The bug is in step 3. The token refresh happens before
 the old token is invalidated. Fix only the token invalidation
 timing in src/auth/refresh.ts."
```

### Show Examples

```bash
# Instead of describing what you want:
"Format the API responses consistently"

# Show an example:
"Format all API responses like this example:

 Success: { status: 'ok', data: { ... }, meta: { timestamp: '...' } }
 Error:   { status: 'error', error: { code: 'NOT_FOUND', message: '...' } }

 Apply this to all route handlers in src/routes/"
```

### Reset Context

```bash
# When the conversation is going in circles
/compact

# Or start completely fresh
/clear

# Then re-state the problem cleanly
"Fresh start. I need to fix a bug in src/auth/refresh.ts.
 The issue: refresh tokens are accepted after logout.
 Expected: after POST /auth/logout, the refresh token should be rejected."
```

---

## Real-World Debugging Session

### Scenario: AI Generated Broken Auth Code

You asked Claude to "add JWT authentication to the Express API." The code compiles but login always returns 401.

#### Step 1: Reproduce the Bug

```bash
# Start the dev server
npm run dev

# Try to log in
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Response: { "error": "Invalid credentials" }
# But you know this user exists in the database!
```

#### Step 2: Read the AI-Generated Code

```bash
# Ask Claude to explain what it wrote
"Read src/auth/login.ts and explain the login flow step by step"
```

Claude explains the flow. You notice:

```typescript
// src/auth/login.ts — AI-generated code
async function login(email: string, password: string) {
  const user = await db.users.findOne({ email });
  if (!user) return null;

  // AI used bcrypt.compare but passed arguments in wrong order
  const valid = await bcrypt.compare(user.passwordHash, password);
  //                                 ^^^^^^^^^^^^^^^^   ^^^^^^^^
  //                                 Should be: (password, user.passwordHash)
  return valid ? generateToken(user) : null;
}
```

#### Step 3: Identify the Bug

```bash
"The bcrypt.compare call on line 8 of src/auth/login.ts has the arguments
 in the wrong order. The first argument should be the plaintext password,
 the second should be the hash. Fix this."
```

#### Step 4: Verify the Fix

```bash
# Claude fixes the code. Verify:
git diff src/auth/login.ts

# You see:
# -  const valid = await bcrypt.compare(user.passwordHash, password);
# +  const valid = await bcrypt.compare(password, user.passwordHash);

# Test again
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Response: { "token": "eyJhbG..." }  ✅ It works!
```

#### Step 5: Check for Similar Issues

```bash
"Search the entire auth module for other bcrypt calls.
 Make sure all of them have the correct argument order."
```

#### Step 6: Add Tests to Prevent Regression

```bash
"Write tests for the login function that cover:
 - Valid credentials return a token
 - Wrong password returns null
 - Non-existent user returns null
 - SQL injection in email field is handled safely"
```

#### Step 7: Commit the Fix

```bash
git add src/auth/login.ts src/auth/__tests__/login.test.ts
git commit -m "fix: correct bcrypt.compare argument order in login"
```

#### Step 8: Retrospective

What went wrong and how to prevent it next time:

```
Root cause: AI swapped bcrypt.compare arguments
Detection:  Manual testing (could have been caught earlier)

Prevention for next time:
1. Write login tests BEFORE implementation (TDD)
2. Ask AI to self-review security-critical code
3. Add to CLAUDE.md:
   "bcrypt.compare takes (plaintext, hash) — not the reverse"
4. Small tasks: separate "add user model" from "add login" from "add JWT"
```

---

## Quick Reference

### AI Bug Detection Checklist

```
After every AI code generation:
  □ Does it compile? (tsc --noEmit, mypy, go vet)
  □ Does it pass lint? (eslint, ruff, golangci-lint)
  □ Do existing tests still pass? (npm test)
  □ Does the new code have tests?
  □ Did you read the diff? (git diff)
  □ Are edge cases handled? (null, empty, error, boundaries)
  □ Are the right packages/versions imported?
  □ Is the coding style consistent with the project?
```

### Common AI Mistakes by Language

```
TypeScript:
  - any types where specific types are needed
  - Missing null checks (strictNullChecks)
  - Wrong module system (import vs require)
  - Forgetting to await async functions

Python:
  - Wrong indentation (mixing tabs and spaces)
  - Mutable default arguments (def foo(items=[]))
  - Not handling exceptions (bare except:)
  - Wrong string formatting (% vs .format vs f-string)

Go:
  - Ignoring error returns (_, _ = someFunc())
  - Goroutine leaks (no context cancellation)
  - Race conditions (missing mutex)
  - Incorrect nil checks on interfaces

React:
  - Missing dependency arrays in useEffect
  - Stale closures
  - Not memoizing expensive calculations
  - Direct state mutation
```

### Recovery Commands Cheat Sheet

```bash
# See what changed
git diff                          # All changes
git diff --name-only              # Changed files only
git log --oneline -5              # Recent commits

# Save current state
git stash                         # Stash changes
git stash pop                     # Restore stashed changes

# Revert changes
git checkout HEAD -- <file>       # Revert one file
git checkout HEAD -- .            # Revert all files
git revert <commit>               # Reverse a commit (safe)

# Claude Code
"undo the last change"            # Undo AI's last edit
"revert changes to auth module"   # Selective undo
/clear                            # Reset conversation
/compact                          # Compress context
```

---

## Summary

```
Most common AI bugs:
  1. Hallucinated APIs (wrong function names)
  2. Outdated syntax (deprecated patterns)
  3. Logic errors (off-by-one, wrong comparisons)
  4. Missing edge cases (null, empty, error)

Best detection tools:
  1. Type checker (tsc, mypy) — catches hallucinated APIs
  2. Tests (especially TDD) — catches logic errors
  3. Code review (read the diff!) — catches everything else

Best prevention:
  1. Small tasks (5 min chunks, verify each one)
  2. TDD (write tests first)
  3. Incremental commits (safe rollback points)
  4. Clear prompts (specific context, not vague requests)

When stuck:
  1. More context (error messages, file paths)
  2. Stronger model (upgrade to Opus)
  3. Smaller pieces (break the problem down)
  4. Fresh start (/clear, /compact)
```

> Previous: [Cost Optimization & Model Selection](13-cost-and-model-selection.md)
