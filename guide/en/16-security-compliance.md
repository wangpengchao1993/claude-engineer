# Security & Compliance for AI-Generated Code

> Understanding the security model, protecting secrets, preventing common vulnerabilities in AI-generated code, managing dependency security, and meeting compliance requirements.

## Table of Contents

- [The Security Model](#the-security-model)
- [Secrets Management](#secrets-management)
- [OWASP Top 10 for AI Code](#owasp-top-10-for-ai-code)
- [Dependency Security](#dependency-security)
- [Compliance Workflows](#compliance-workflows)
- [Security Hooks Configuration](#security-hooks-configuration)

---

## The Security Model

### What Data Goes to the Anthropic API?

When you use Claude Code, code context is sent to the Anthropic API for processing.

```
What IS sent:
- File contents that Claude reads (only files you ask it to read or it needs)
- Your prompts and instructions
- Terminal output from commands Claude runs
- Content of CLAUDE.md files

What is NOT sent:
- Files Claude doesn't access during the session
- Your entire filesystem
- Environment variables (unless you paste them into the prompt)
- Git credentials or SSH keys
```

### API Data Retention

```
Anthropic API data handling:
- API inputs/outputs are NOT used to train models
- Data retention depends on your plan:
  - Standard API: 30-day retention for trust & safety
  - Enterprise: zero-retention option available
- See https://anthropic.com/policies for current policy
```

### Enterprise Security Options

```bash
# For enterprise deployments, configure zero-retention
# This is set at the API key / organization level

# Verify your API key's organization settings
claude "/config" # Check current configuration

# Enterprise teams should:
# 1. Use organization-managed API keys
# 2. Enable zero-retention at the org level
# 3. Use SSO for team member authentication
# 4. Set up audit logging for API usage
```

### Local-Only Operations

Some operations never leave your machine:

```
Always local:
- File reading and writing (Claude reads locally, sends context to API)
- Git operations
- Shell command execution
- Hook execution
- CLAUDE.md parsing

The flow:
1. Claude reads files locally
2. Sends relevant context to API
3. Receives response from API
4. Executes actions locally (file writes, commands)
```

---

## Secrets Management

### Rule: NEVER Put Secrets in Prompts or CLAUDE.md

```markdown
# BAD - CLAUDE.md with secrets
## Database
Connection string: postgres://admin:s3cret_p4ss@db.example.com:5432/prod

## API Keys
Stripe: sk_live_abc123...
SendGrid: SG.xyz789...
```

```markdown
# GOOD - CLAUDE.md with references
## Database
Connection string is in DATABASE_URL env var. See .env.example for format.

## API Keys
All API keys are in .env (gitignored). See .env.example for required variables.
```

### Environment Variable Strategy

```bash
# .env.example (committed - shows required vars without values)
DATABASE_URL=postgres://user:password@localhost:5432/dbname
STRIPE_SECRET_KEY=sk_test_...
REDIS_URL=redis://localhost:6379
JWT_SECRET=generate-a-random-string-here

# .env (gitignored - actual values)
DATABASE_URL=postgres://admin:real_password@localhost:5432/myapp
STRIPE_SECRET_KEY=sk_test_actual_key_here
REDIS_URL=redis://localhost:6379
JWT_SECRET=a8f2e1b5c3d4...
```

```bash
# .gitignore must include:
.env
.env.local
.env.production
*.pem
*.key
credentials.json
service-account.json
```

### Vault Solutions for Production

```typescript
// src/config/secrets.ts - Load secrets from vault in production
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

interface AppSecrets {
  databaseUrl: string;
  stripeKey: string;
  jwtSecret: string;
}

async function loadSecrets(): Promise<AppSecrets> {
  if (process.env.NODE_ENV === 'development') {
    // In development, use .env file
    return {
      databaseUrl: process.env.DATABASE_URL!,
      stripeKey: process.env.STRIPE_SECRET_KEY!,
      jwtSecret: process.env.JWT_SECRET!,
    };
  }

  // In production, use AWS Secrets Manager
  const client = new SecretsManager({ region: 'us-east-1' });
  const response = await client.getSecretValue({
    SecretId: 'myapp/production',
  });

  return JSON.parse(response.SecretString!);
}

export const secrets = await loadSecrets();
```

### Pre-Commit Hook to Block Secrets

```bash
#!/bin/bash
# .git/hooks/pre-commit or via .claude/settings.json hooks

# Patterns that indicate secrets
PATTERNS=(
  'AKIA[0-9A-Z]{16}'                    # AWS Access Key ID
  'sk_live_[a-zA-Z0-9]+'                # Stripe live key
  'sk-[a-zA-Z0-9]{48}'                  # OpenAI API key
  'ghp_[a-zA-Z0-9]{36}'                 # GitHub personal access token
  'xoxb-[0-9]+-[a-zA-Z0-9]+'           # Slack bot token
  'password\s*=\s*["\x27][^"\x27]+'     # Hardcoded passwords
  'secret\s*=\s*["\x27][^"\x27]+'       # Hardcoded secrets
  'jdbc:.*password=[^&\s]+'             # JDBC connection strings with password
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR)

for file in $STAGED_FILES; do
  for pattern in "${PATTERNS[@]}"; do
    if git show ":$file" 2>/dev/null | grep -qE "$pattern"; then
      echo "ERROR: Potential secret detected in $file"
      echo "Pattern matched: $pattern"
      echo "Please remove the secret and use environment variables instead."
      exit 1
    fi
  done
done

exit 0
```

Configure this as a Claude Code hook:

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreCommit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/check-secrets.sh"
          }
        ]
      }
    ]
  }
}
```

---

## OWASP Top 10 for AI Code

AI-generated code frequently introduces specific vulnerability patterns. Here are the most common ones and how to prevent them.

### 1. SQL Injection

```typescript
// BAD: AI often generates string concatenation for queries
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const result = await db.query(`SELECT * FROM users WHERE name = '${name}'`);
  res.json(result.rows);
});

// GOOD: Parameterized queries
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const result = await db.query('SELECT * FROM users WHERE name = $1', [name]);
  res.json(result.rows);
});

// BEST: Use an ORM that handles parameterization
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const users = await db.select().from(usersTable).where(eq(usersTable.name, name));
  res.json(users);
});
```

### 2. Cross-Site Scripting (XSS)

```typescript
// BAD: AI may use dangerouslySetInnerHTML or skip sanitization
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// GOOD: Use text content (React auto-escapes)
function Comment({ text }: { text: string }) {
  return <div>{text}</div>;
}

// When HTML is necessary, sanitize explicitly
import DOMPurify from 'dompurify';

function RichComment({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

### 3. Insecure Authentication

```typescript
// BAD: AI sometimes generates weak auth patterns
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await db.findUser(username);
  if (user.password === password) {  // Plain text comparison!
    const token = jwt.sign({ id: user.id }, 'hardcoded-secret');  // Hardcoded!
    res.json({ token });
  }
});

// GOOD: Proper auth implementation
import bcrypt from 'bcrypt';

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await db.findUser(username);

  if (!user) {
    // Same response for missing user and wrong password (prevent enumeration)
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '1h', algorithm: 'HS256' }
  );

  res.json({ token });
});
```

### 4. Path Traversal

```typescript
// BAD: AI may not validate file paths
app.get('/files/:name', (req, res) => {
  const filePath = path.join('/uploads', req.params.name);
  res.sendFile(filePath);  // ../../../etc/passwd works!
});

// GOOD: Validate the resolved path stays within the allowed directory
app.get('/files/:name', (req, res) => {
  const uploadsDir = path.resolve('/uploads');
  const filePath = path.resolve(uploadsDir, req.params.name);

  if (!filePath.startsWith(uploadsDir)) {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.sendFile(filePath);
});
```

### Security Review Prompt for CLAUDE.md

Add this to your CLAUDE.md to make Claude Code security-aware:

```markdown
## Security Requirements

When generating code, always:
- Use parameterized queries for ALL database operations
- Sanitize user input before rendering in HTML
- Use bcrypt or argon2 for password hashing (never MD5/SHA for passwords)
- Load secrets from environment variables, never hardcode them
- Validate file paths to prevent path traversal
- Set appropriate CORS headers (not wildcard in production)
- Use HTTPS-only cookies with SameSite attribute
- Implement rate limiting on authentication endpoints
- Validate and sanitize all user input at API boundaries
- Use Content-Security-Policy headers
```

---

## Dependency Security

### AI May Suggest Vulnerable Packages

```bash
# After AI installs or suggests dependencies, always audit

# Node.js
npm audit
npm audit fix

# Python
pip-audit
pip-audit --fix

# Rust
cargo audit

# Go
govulncheck ./...
```

### Automated Audit After Dependency Changes

```jsonc
// .claude/settings.json - Run audit after any dependency change
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash(npm install*)",
        "hooks": [
          {
            "type": "command",
            "command": "npm audit --audit-level=high"
          }
        ]
      },
      {
        "matcher": "Bash(pip install*)",
        "hooks": [
          {
            "type": "command",
            "command": "pip-audit 2>/dev/null || echo 'pip-audit not installed, run: pip install pip-audit'"
          }
        ]
      }
    ]
  }
}
```

### Lockfile Verification

```bash
# Ensure lockfiles are committed and consistent
# Add to CI pipeline

# Node.js - verify lockfile integrity
npm ci  # Fails if lockfile is out of sync with package.json

# Python - verify pinned versions
pip install --require-hashes -r requirements.txt

# Always review dependency changes in AI-generated PRs
git diff package-lock.json | head -50  # Check what changed
```

### CLAUDE.md Dependency Policy

```markdown
## Dependencies

- Do NOT add new dependencies without discussing first
- Prefer well-maintained packages (>1000 GitHub stars, recent commits)
- No packages with known critical vulnerabilities
- Always run `npm audit` after adding dependencies
- Pin exact versions in package.json (no ^ or ~ prefixes)
- Review transitive dependencies for known issues
```

---

## Compliance Workflows

### Audit Logging

Track AI-assisted development for compliance:

```typescript
// scripts/log-ai-session.ts
import { appendFileSync } from 'fs';

interface AIAuditEntry {
  timestamp: string;
  developer: string;
  sessionId: string;
  action: 'prompt' | 'code_generated' | 'code_committed';
  summary: string;
  filesModified: string[];
}

function logAIActivity(entry: AIAuditEntry): void {
  const logPath = process.env.AI_AUDIT_LOG || './logs/ai-audit.jsonl';
  appendFileSync(logPath, JSON.stringify(entry) + '\n');
}

// Example usage in a git hook
// After each AI-assisted commit, log what was done
logAIActivity({
  timestamp: new Date().toISOString(),
  developer: process.env.USER || 'unknown',
  sessionId: process.env.CLAUDE_SESSION_ID || 'unknown',
  action: 'code_committed',
  summary: 'AI-assisted implementation of rate limiting middleware',
  filesModified: ['src/middleware/rate-limiter.ts', 'tests/rate-limiter.test.ts'],
});
```

### SOC 2 Considerations

```markdown
## SOC 2 Checklist for AI in Development

### Access Control
- [ ] API keys are managed through organization, not individual accounts
- [ ] API key rotation schedule is in place (every 90 days)
- [ ] Developer access to AI tools is logged
- [ ] AI tool access is revoked on offboarding

### Change Management
- [ ] AI-generated code goes through the same review process as human code
- [ ] AI-assisted changes are tagged in commit messages
- [ ] Audit trail exists for what AI was asked to do
- [ ] No AI-generated code bypasses code review

### Data Protection
- [ ] Production data is never used in AI prompts
- [ ] Customer PII is never included in code context
- [ ] Zero-retention API option is enabled for sensitive projects
- [ ] Data flow diagram includes AI API interactions

### Monitoring
- [ ] API usage is monitored for anomalies
- [ ] AI-generated code is included in security scanning
- [ ] Dependency audits cover AI-suggested packages
```

### GDPR: Personal Data in AI Context

```bash
# NEVER include personal data in prompts

# BAD
claude "Fix the bug with user john.doe@example.com whose order #12345
  for $499.99 shipped to 123 Main St isn't showing in the dashboard"

# GOOD
claude "Fix the bug where a user's order isn't showing in the dashboard.
  The order has status 'shipped' but the dashboard query filters it out.
  Reproduce with: npm run seed && npm test -- --grep 'order display'"
```

```markdown
# Add to CLAUDE.md for GDPR-regulated projects

## Data Privacy Rules
- NEVER include real customer data in prompts or code comments
- Use synthetic data for all examples and tests
- Seed scripts must generate fake data (use @faker-js/faker)
- Log files must be excluded from AI context (.claude/settings.json)
- Database dumps are NEVER loaded into AI sessions
```

### Tagging AI-Assisted Commits

```bash
# Convention: tag commits that had AI assistance
git commit -m "feat(auth): add OAuth2 PKCE flow

Implemented OAuth2 PKCE flow for public clients.

AI-assisted: yes
AI-tool: claude-code
AI-scope: implementation and tests"
```

```bash
# Git hook to prompt for AI-assistance tag
# .git/hooks/prepare-commit-msg

#!/bin/bash
COMMIT_MSG_FILE=$1

# Check if AI-assisted tag already present
if ! grep -q "AI-assisted:" "$COMMIT_MSG_FILE"; then
  echo "" >> "$COMMIT_MSG_FILE"
  echo "AI-assisted: yes/no" >> "$COMMIT_MSG_FILE"
  echo "AI-tool: claude-code" >> "$COMMIT_MSG_FILE"
fi
```

---

## Security Hooks Configuration

### Comprehensive Security Hook Setup

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$CLAUDE_TOOL_INPUT\" | python3 scripts/validate-command.py'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$CLAUDE_FILE_PATH\" | xargs -I{} grep -lE \"(password|secret|key)\\s*=\\s*[\\x27\\\"][^\\x27\\\"]+\" {} && echo \"WARNING: Possible hardcoded secret in {}\" || true'"
          }
        ]
      }
    ],
    "PreCommit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/check-secrets.sh && npm audit --audit-level=high"
          }
        ]
      }
    ]
  }
}
```

### Command Validation Script

```python
#!/usr/bin/env python3
# scripts/validate-command.py
"""Validate commands before Claude Code executes them."""

import json
import sys

BLOCKED_PATTERNS = [
    'curl.*|.*sh',          # Piping remote scripts to shell
    'wget.*|.*sh',          # Same for wget
    'eval ',                # Arbitrary code execution
    'rm -rf /',             # Destructive commands
    'chmod 777',            # Overly permissive permissions
    '> /etc/',              # Writing to system files
    'nc -l',               # Network listeners
    'ssh-keygen',          # Key generation should be manual
]

def validate_command(tool_input: str) -> bool:
    import re
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, tool_input):
            print(f"BLOCKED: Command matches dangerous pattern: {pattern}")
            return False
    return True

if __name__ == '__main__':
    input_data = sys.stdin.read().strip()
    try:
        data = json.loads(input_data)
        command = data.get('command', '')
    except json.JSONDecodeError:
        command = input_data

    if not validate_command(command):
        sys.exit(1)
```

### Security Scanning Integration

```bash
#!/bin/bash
# scripts/security-scan.sh
# Run after AI generates code, before committing

set -e

echo "=== Running Security Scan ==="

# Static analysis for security issues
if command -v semgrep &> /dev/null; then
  echo "Running Semgrep..."
  semgrep --config auto --error --quiet .
fi

# Dependency audit
if [ -f "package-lock.json" ]; then
  echo "Running npm audit..."
  npm audit --audit-level=high
fi

if [ -f "requirements.txt" ]; then
  echo "Running pip-audit..."
  pip-audit -r requirements.txt 2>/dev/null || echo "pip-audit not available"
fi

# Check for secrets in staged files
echo "Checking for secrets..."
if command -v gitleaks &> /dev/null; then
  gitleaks detect --staged --no-banner
else
  # Fallback: basic pattern matching
  git diff --cached --name-only | xargs grep -lE \
    'AKIA|sk_live|ghp_|xoxb-|password\s*=' 2>/dev/null && {
    echo "ERROR: Potential secrets found in staged files"
    exit 1
  } || true
fi

echo "=== Security Scan Passed ==="
```

---

## Summary

Security with AI-generated code requires defense in depth:

1. **Understand the data flow**: Know what goes to the API and what stays local
2. **Never expose secrets**: Use env vars, vaults, and pre-commit hooks
3. **Watch for OWASP patterns**: AI frequently generates injection, XSS, and weak auth
4. **Audit dependencies**: AI may suggest outdated or vulnerable packages
5. **Maintain compliance**: Log AI usage, tag commits, protect personal data
6. **Automate security checks**: Hooks catch issues before they reach production

---

[← Previous: Team Workflows](15-team-workflows.md) | [Table of Contents](../../README.md) | [Next: Large Codebase Management →](17-large-codebase.md)
