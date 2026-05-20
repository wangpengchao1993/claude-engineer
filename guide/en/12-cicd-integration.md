# CI/CD Integration: AI in Your Pipeline

> Move AI beyond local development into your build, test, and deploy pipeline. Automate reviews, testing, and release notes.
> CI/CD 集成：AI 进入你的流水线 — 自动化审查、测试和发布说明。

## Table of Contents

- [Why AI in CI/CD](#why-ai-in-cicd)
- [GitHub Actions with Claude Code Action](#github-actions-with-claude-code-action)
- [GitLab CI Integration](#gitlab-ci-integration)
- [Pre-commit Hooks with AI](#pre-commit-hooks-with-ai)
- [Automated Testing Pipeline](#automated-testing-pipeline)
- [Security Scanning in CI](#security-scanning-in-ci)
- [Cost Control in CI](#cost-control-in-ci)
- [Complete Workflow Files](#complete-workflow-files)
- [Troubleshooting](#troubleshooting)

---

## Why AI in CI/CD

Most teams use Claude Code only during development. That wastes its potential. AI in CI/CD gives you:

> 大多数团队只在开发阶段使用 Claude Code，这浪费了它的潜力。AI 进入 CI/CD 可以带来：

| Benefit | Example |
|---------|---------|
| **Automated PR review** | Every PR gets reviewed before human eyes see it / 每个 PR 在人工审查前先由 AI 审查 |
| **Test gap detection** | AI identifies untested code paths on every push / AI 在每次推送时识别未测试的代码路径 |
| **Release notes** | Auto-generated from commit history / 从提交历史自动生成 |
| **Security scanning** | AI checks for OWASP vulnerabilities in changed code / AI 检查变更代码中的 OWASP 漏洞 |
| **Documentation updates** | Auto-detect when docs are stale / 自动检测文档是否过时 |

**The principle:** Humans review what matters. AI handles the rest.

> 原则：人类审查重要的事情，AI 处理其余的。

---

## GitHub Actions with Claude Code Action

### What `anthropics/claude-code-action` Does

The official GitHub Action runs Claude Code in your CI pipeline. It can:

- Read your repository files
- Analyze diffs and pull requests
- Post review comments directly on PRs
- Execute commands in the CI environment
- Generate reports and summaries

> `anthropics/claude-code-action` 是官方 GitHub Action，可以在 CI 流水线中运行 Claude Code。

### Setup: API Key in Secrets

**Step 1:** Add your Anthropic API key to repository secrets.

```
GitHub repo → Settings → Secrets and variables → Actions → New repository secret
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-...
```

**Step 2:** (Optional) Add a model preference:

```
Name: CLAUDE_MODEL
Value: claude-sonnet-4-20250514
```

> 第一步：将 API 密钥添加到仓库的 Secrets 中。

### Example 1: AI-Powered PR Review

This workflow runs on every pull request, reviews the changes, and posts comments.

```yaml
# .github/workflows/ai-review.yml
name: AI PR Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

# Required permissions for posting comments / 发布评论所需的权限
permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest
    # Skip drafts and bot PRs / 跳过草稿和机器人 PR
    if: github.event.pull_request.draft == false && github.actor != 'dependabot[bot]'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT
          echo "count=$(echo $FILES | wc -w)" >> $GITHUB_OUTPUT

      - name: AI Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: ${{ vars.CLAUDE_MODEL || 'claude-sonnet-4-20250514' }}
          prompt: |
            You are a senior code reviewer. Review this pull request.

            PR Title: ${{ github.event.pull_request.title }}
            PR Description: ${{ github.event.pull_request.body }}
            Changed files (${{ steps.changed.outputs.count }}): ${{ steps.changed.outputs.files }}

            Review for:
            1. **Bugs**: Logic errors, null handling, race conditions, edge cases
            2. **Security**: Injection, auth issues, data exposure, SSRF
            3. **Performance**: N+1 queries, missing indexes, unnecessary computation
            4. **Testing**: Are new code paths tested? Missing edge case tests?
            5. **Code quality**: DRY violations, unclear naming, missing docs

            For each issue found:
            - State the severity (Critical / Warning / Suggestion)
            - Quote the specific code
            - Explain why it's a problem
            - Show the fix

            If the code looks good, say so briefly. Don't invent issues.
```

### Example 2: AI-Generated Test Suggestions

Run on push to detect untested code and suggest tests.

```yaml
# .github/workflows/ai-test-suggestions.yml
name: AI Test Suggestions
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - '!src/**/*.test.*'
      - '!src/**/*.spec.*'

permissions:
  contents: read
  issues: write

jobs:
  suggest-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Get changed source files
        id: changed
        run: |
          # Only source files, not tests / 只获取源文件，不含测试
          FILES=$(git diff --name-only HEAD~1 HEAD -- 'src/' | grep -v '\.test\.' | grep -v '\.spec\.' | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: Check for corresponding tests
        id: coverage
        run: |
          MISSING=""
          for file in ${{ steps.changed.outputs.files }}; do
            # Check if test file exists / 检查对应的测试文件是否存在
            test_file=$(echo "$file" | sed 's/\.js/.test.js/' | sed 's/\.ts/.test.ts/')
            if [ ! -f "$test_file" ]; then
              MISSING="$MISSING $file"
            fi
          done
          echo "missing=$MISSING" >> $GITHUB_OUTPUT

      - name: AI Test Suggestions
        if: steps.coverage.outputs.missing != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            These source files were changed but have no corresponding test files:
            ${{ steps.coverage.outputs.missing }}

            For each file:
            1. Read the source code
            2. Identify the key functions/methods
            3. Write a complete test file using the project's test framework
            4. Cover: happy path, error cases, edge cases

            Output each test file with its path and full content.
```

### Example 3: AI-Assisted Release Notes

Generate release notes from commits when a release is created.

```yaml
# .github/workflows/ai-release-notes.yml
name: AI Release Notes
on:
  release:
    types: [created]

permissions:
  contents: write

jobs:
  release-notes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get commits since last release
        id: commits
        run: |
          # Find the previous tag / 找到上一个标签
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREV_TAG" ]; then
            COMMITS=$(git log --oneline)
          else
            COMMITS=$(git log --oneline "$PREV_TAG"..HEAD)
          fi
          # Write to file to handle multiline / 写入文件处理多行
          echo "$COMMITS" > /tmp/commits.txt
          echo "count=$(echo "$COMMITS" | wc -l)" >> $GITHUB_OUTPUT

      - name: Generate release notes
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            Generate release notes for version ${{ github.event.release.tag_name }}.

            Commits since last release:
            $(cat /tmp/commits.txt)

            Format the release notes as:
            ## What's New
            - Feature descriptions (from feat: commits)

            ## Bug Fixes
            - Fix descriptions (from fix: commits)

            ## Improvements
            - Other changes (refactor, perf, etc.)

            ## Breaking Changes
            - Any breaking changes (from commits with BREAKING CHANGE)

            Write for end users, not developers. Be concise.

      - name: Update release body
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release edit ${{ github.event.release.tag_name }} \
            --notes-file /tmp/release-notes.md
```

---

## GitLab CI Integration

### Equivalent `.gitlab-ci.yml` Examples

GitLab CI does not have a pre-built Claude Code action, so we use the CLI directly.

> GitLab CI 没有预构建的 Claude Code action，所以我们直接使用 CLI。

### AI PR Review for GitLab

```yaml
# .gitlab-ci.yml
stages:
  - review
  - test
  - deploy

ai-review:
  stage: review
  image: node:18-alpine
  only:
    - merge_requests
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      # Get the diff / 获取差异
      DIFF=$(git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD)

      # Run Claude review / 运行 Claude 审查
      REVIEW=$(echo "$DIFF" | claude -p \
        --model claude-sonnet-4-20250514 \
        "Review this merge request diff. Focus on bugs, security, and performance.
         MR Title: $CI_MERGE_REQUEST_TITLE
         Output as markdown.")

      # Post comment to MR / 发布评论到 MR
      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --header "Content-Type: application/json" \
        --data "{\"body\": $(echo "$REVIEW" | jq -Rs .)}" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
```

### AI Test Generation for GitLab

```yaml
ai-test-suggestions:
  stage: review
  image: node:18-alpine
  only:
    - merge_requests
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      # Find changed source files without tests / 找到没有测试的变更文件
      CHANGED=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD \
        | grep -E '\.(js|ts|py)$' \
        | grep -v '\.test\.' \
        | grep -v '\.spec\.' \
        | grep -v '__tests__')

      if [ -z "$CHANGED" ]; then
        echo "No source files changed, skipping."
        exit 0
      fi

      echo "Changed files without tests: $CHANGED"

      # Generate test suggestions / 生成测试建议
      claude -p \
        --model claude-sonnet-4-20250514 \
        "These files were changed but may lack tests: $CHANGED
         Read each file and suggest test cases. Output as markdown."
```

---

## Pre-commit Hooks with AI

### Why Pre-commit Hooks?

Pre-commit hooks catch issues *before* they enter your repository. Adding AI here means:

- Security issues caught before commit, not in CI (saves time and money)
- Code quality feedback is instant
- Developers learn from AI suggestions immediately

> 预提交钩子在代码进入仓库之前捕获问题。在这里加入 AI 意味着即时反馈。

### Setup with Husky + Claude Code

```bash
# Install husky / 安装 husky
npm install -D husky
npx husky init
```

### AI Security Check Hook

```bash
#!/bin/bash
# .husky/pre-commit

# Get staged files / 获取暂存的文件
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|py|go|java)$')

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

echo "🔍 Running AI security check on staged files..."

# Quick security scan with Haiku (fast and cheap) / 用 Haiku 快速安全扫描
ISSUES=$(git diff --cached | claude -p \
  --model claude-haiku-4-20250514 \
  --max-turns 1 \
  "Scan this diff for security issues ONLY. Check for:
   - Hardcoded secrets/passwords/API keys
   - SQL injection
   - XSS vulnerabilities
   - Path traversal
   - Insecure deserialization

   If no issues found, respond with exactly: PASS
   If issues found, list them with file and line number.")

if echo "$ISSUES" | grep -q "PASS"; then
  echo "✅ Security check passed"
  exit 0
else
  echo "⚠️  Security issues found:"
  echo "$ISSUES"
  echo ""
  echo "Fix the issues above or use 'git commit --no-verify' to skip."
  exit 1
fi
```

### AI Lint + Format Hook

```bash
#!/bin/bash
# .husky/pre-commit (alternative: combined hook)

STAGED=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED" ]; then
  exit 0
fi

# Step 1: Standard linting (fast, free) / 标准 lint（快速、免费）
echo "Running ESLint..."
npx eslint $STAGED --fix
LINT_EXIT=$?

# Step 2: Auto-format / 自动格式化
echo "Running Prettier..."
npx prettier --write $STAGED

# Step 3: Re-stage fixed files / 重新暂存修复的文件
git add $STAGED

# Step 4: AI check only if lint passed (avoid wasting tokens on broken code)
# 只在 lint 通过后运行 AI 检查（避免在有问题的代码上浪费 token）
if [ $LINT_EXIT -eq 0 ]; then
  echo "Running AI quality check..."
  DIFF=$(git diff --cached)

  if [ -n "$DIFF" ]; then
    QUALITY=$(echo "$DIFF" | claude -p \
      --model claude-haiku-4-20250514 \
      --max-turns 1 \
      "Quick code review. Only flag CRITICAL issues:
       - Obvious bugs
       - Security vulnerabilities
       - Data loss risks
       Respond PASS if no critical issues. Be brief.")

    if ! echo "$QUALITY" | grep -q "PASS"; then
      echo "⚠️  AI found potential issues:"
      echo "$QUALITY"
      echo ""
      read -p "Commit anyway? (y/N) " -n 1 -r
      echo
      if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
      fi
    fi
  fi
fi
```

### Using Claude Code Hooks (Built-in)

Claude Code has a built-in hooks system that can run on specific events. This is different from git hooks — these run within Claude Code sessions.

> Claude Code 有内置的 hooks 系统，可以在特定事件上运行。这与 git hooks 不同。

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreCommit": [
      {
        "command": "npm run lint && npm test",
        "description": "Run lint and tests before committing"
      }
    ],
    "PostCommit": [
      {
        "command": "echo 'Commit successful'",
        "description": "Confirmation message"
      }
    ]
  }
}
```

---

## Automated Testing Pipeline

### AI Generates Tests, CI Runs Them

This pipeline uses AI to generate tests for untested code, then runs them immediately.

> 这个流水线让 AI 生成测试，然后立即运行。

```yaml
# .github/workflows/ai-test-generation.yml
name: AI Test Generation
on:
  push:
    branches: [develop]
    paths: ['src/**']

permissions:
  contents: write
  pull-requests: write

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run existing tests and get coverage
        run: |
          npx jest --coverage --coverageReporters=json-summary || true
          # Extract uncovered files / 提取未覆盖的文件
          node -e "
            const cov = require('./coverage/coverage-summary.json');
            const uncovered = Object.entries(cov)
              .filter(([k, v]) => k !== 'total' && v.lines.pct < 80)
              .map(([k]) => k.replace(process.cwd() + '/', ''));
            console.log(uncovered.join(' '));
          " > /tmp/uncovered.txt

      - name: Generate tests for uncovered code
        if: "hashFiles('/tmp/uncovered.txt') != ''"
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            These files have less than 80% test coverage:
            $(cat /tmp/uncovered.txt)

            For each file:
            1. Read the source code
            2. Check if a test file exists
            3. If yes, add missing test cases
            4. If no, create a complete test file

            Use the project's existing test patterns and framework.
            Place test files next to source files as *.test.js.

      - name: Run tests with new test files
        run: |
          npx jest --passWithNoTests
          echo "test_result=$?" >> $GITHUB_ENV

      - name: Create PR with new tests
        if: env.test_result == '0'
        run: |
          git config user.name "AI Test Bot"
          git config user.email "ai-tests@noreply.github.com"

          BRANCH="ai/tests-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"

          # Add only test files / 只添加测试文件
          git add '*.test.js' '*.test.ts' '*.spec.js' '*.spec.ts'

          if git diff --cached --quiet; then
            echo "No new tests generated"
            exit 0
          fi

          git commit -m "test: add AI-generated tests for uncovered code"
          git push origin "$BRANCH"

          gh pr create \
            --title "Add tests for uncovered code" \
            --body "AI-generated tests for files with <80% coverage.
                    Please review before merging." \
            --label "ai-generated,tests"
```

### Coverage Gate with AI Explanation

```yaml
# Add to your CI pipeline / 添加到你的 CI 流水线
coverage-gate:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - uses: actions/checkout@v4

    - name: Check coverage threshold
      id: coverage
      run: |
        TOTAL=$(node -e "console.log(require('./coverage/coverage-summary.json').total.lines.pct)")
        echo "coverage=$TOTAL" >> $GITHUB_OUTPUT
        if (( $(echo "$TOTAL < 80" | bc -l) )); then
          echo "below_threshold=true" >> $GITHUB_OUTPUT
        fi

    - name: AI Coverage Analysis
      if: steps.coverage.outputs.below_threshold == 'true'
      uses: anthropics/claude-code-action@v1
      with:
        anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
        model: claude-haiku-4-20250514
        prompt: |
          Test coverage is ${{ steps.coverage.outputs.coverage }}% (threshold: 80%).

          Analyze the coverage report and explain:
          1. Which files/functions are least covered?
          2. What are the most impactful tests to add?
          3. Estimate the effort to reach 80%

          Be specific and actionable. Output as a PR comment.
```

---

## Security Scanning in CI

### OWASP Vulnerability Check on PRs

> 在 PR 中检查 OWASP 漏洞。

```yaml
# .github/workflows/ai-security-scan.yml
name: AI Security Scan
on:
  pull_request:
    paths:
      - 'src/**'
      - 'api/**'
      - 'routes/**'
      - 'controllers/**'

permissions:
  pull-requests: write
  contents: read

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep -E '\.(js|ts|py|go|java|rb)$' \
            | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: AI Security Scan
        if: steps.changed.outputs.files != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            Perform a security audit on the changed files in this PR.
            Changed files: ${{ steps.changed.outputs.files }}

            Check for OWASP Top 10 vulnerabilities:
            1. **A01 Broken Access Control** — Missing auth checks, IDOR, privilege escalation
            2. **A02 Cryptographic Failures** — Weak hashing, plaintext secrets, insecure random
            3. **A03 Injection** — SQL, NoSQL, OS command, LDAP injection
            4. **A04 Insecure Design** — Missing rate limits, business logic flaws
            5. **A05 Security Misconfiguration** — Debug mode, default credentials, verbose errors
            6. **A06 Vulnerable Components** — Known CVEs in dependencies (check package.json)
            7. **A07 Auth Failures** — Weak passwords allowed, missing MFA, session issues
            8. **A08 Data Integrity Failures** — Deserialization, unsigned updates
            9. **A09 Logging Failures** — Missing audit logs, sensitive data in logs
            10. **A10 SSRF** — User-controlled URLs, unvalidated redirects

            For each vulnerability found:
            ```
            [SEVERITY: Critical/High/Medium/Low]
            File: path/to/file.js:line_number
            Issue: Description of the vulnerability
            Impact: What an attacker could do
            Fix: Specific code fix
            ```

            If no vulnerabilities found, state "No security issues found in changed files."
```

### Dependency Vulnerability Check

```yaml
# .github/workflows/ai-dependency-check.yml
name: AI Dependency Check
on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'
      - 'requirements.txt'
      - 'go.mod'
      - 'Cargo.toml'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        id: audit
        run: |
          npm audit --json > /tmp/audit.json 2>/dev/null || true
          VULNS=$(node -e "const a=require('/tmp/audit.json'); console.log(a.metadata?.vulnerabilities?.total || 0)")
          echo "vulnerabilities=$VULNS" >> $GITHUB_OUTPUT

      - name: AI Dependency Analysis
        if: steps.audit.outputs.vulnerabilities != '0'
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            npm audit found ${{ steps.audit.outputs.vulnerabilities }} vulnerabilities.
            Audit report: $(cat /tmp/audit.json)

            For each vulnerability:
            1. Explain the risk in plain language
            2. Is it exploitable in our usage context?
            3. What's the fix? (upgrade path or workaround)

            Prioritize by actual risk, not just severity score.
```

---

## Cost Control in CI

AI in CI can get expensive fast if not managed properly. Here are strategies to control costs.

> CI 中的 AI 如果管理不当会很快变得昂贵。以下是控制成本的策略。

### Strategy 1: Only Run on Changed Files

```yaml
# Don't analyze the entire repo — only changed files
# 不要分析整个仓库 — 只分析变更的文件
- name: Get changed files
  run: |
    FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
    echo "files=$FILES" >> $GITHUB_OUTPUT
```

### Strategy 2: Use Haiku for Simple Checks

```yaml
# Use Haiku ($0.25/M input) for simple checks, Sonnet ($3/M input) for deep review
# 简单检查用 Haiku（$0.25/M 输入），深度审查用 Sonnet（$3/M 输入）

# Haiku: lint, format check, simple security scan
- name: Quick AI Check
  uses: anthropics/claude-code-action@v1
  with:
    model: claude-haiku-4-20250514
    prompt: "Quick scan for critical issues only..."

# Sonnet: full code review, architecture review
- name: Deep AI Review
  uses: anthropics/claude-code-action@v1
  with:
    model: claude-sonnet-4-20250514
    prompt: "Comprehensive code review..."
```

### Strategy 3: Conditional Execution

```yaml
# Only run AI review on PRs with significant changes
# 只在有大量变更的 PR 上运行 AI 审查
- name: Check change size
  id: size
  run: |
    LINES=$(git diff --stat origin/${{ github.base_ref }}...HEAD | tail -1 | awk '{print $4+$6}')
    echo "lines_changed=$LINES" >> $GITHUB_OUTPUT

- name: AI Review (only for large PRs)
  if: steps.size.outputs.lines_changed > 50
  uses: anthropics/claude-code-action@v1
  with:
    # ...
```

### Strategy 4: Skip Certain File Types

```yaml
# Skip docs, configs, and generated files / 跳过文档、配置和生成的文件
- name: Filter files for review
  run: |
    FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
      | grep -v '\.md$' \
      | grep -v '\.json$' \
      | grep -v '\.lock$' \
      | grep -v 'dist/' \
      | grep -v 'build/' \
      | grep -v '__generated__/' \
      | tr '\n' ' ')
    echo "files=$FILES" >> $GITHUB_OUTPUT
```

### Strategy 5: Set Token Budgets

```yaml
# Use max-turns to limit token usage / 使用 max-turns 限制 token 用量
- name: Budget-controlled review
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    model: claude-haiku-4-20250514
    max_turns: 1
    prompt: "Review in a single pass. Be concise."
```

### Cost Estimate Table

| Scenario | Model | Files | Tokens | Cost per Run |
|----------|-------|-------|--------|-------------|
| PR review (small) | Haiku | 3 files | ~15K | ~$0.005 |
| PR review (medium) | Sonnet | 10 files | ~50K | ~$0.25 |
| PR review (large) | Sonnet | 30 files | ~150K | ~$0.75 |
| Security scan | Sonnet | 10 files | ~40K | ~$0.20 |
| Release notes | Haiku | N/A | ~10K | ~$0.003 |
| Test generation | Sonnet | 5 files | ~80K | ~$0.40 |

> **Monthly estimate for an active team (50 PRs/month):**
> - Haiku only: ~$5-10/month
> - Mixed Haiku + Sonnet: ~$20-50/month
> - Sonnet only: ~$50-100/month

---

## Complete Workflow Files

### All-in-One CI Pipeline

Copy-paste this complete workflow file. It combines review, security, and testing in one pipeline.

> 复制粘贴这个完整的工作流文件，它将审查、安全和测试合并在一个流水线中。

```yaml
# .github/workflows/ai-ci.yml
name: AI-Powered CI
on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches: [main]

permissions:
  contents: read
  pull-requests: write
  issues: write

env:
  NODE_VERSION: '18'

jobs:
  # ──────────────────────────────────────────
  # Job 1: Standard CI (no AI, always runs)
  # 任务 1：标准 CI（无 AI，始终运行）
  # ──────────────────────────────────────────
  standard-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  # ──────────────────────────────────────────
  # Job 2: AI Code Review (PRs only)
  # 任务 2：AI 代码审查（仅 PR）
  # ──────────────────────────────────────────
  ai-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    needs: standard-ci
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed source files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep -E '\.(js|ts|jsx|tsx|py|go|java|rb)$' \
            | grep -v '\.test\.' | grep -v '\.spec\.' \
            | grep -v 'dist/' | grep -v 'build/' \
            | tr '\n' ' ')
          COUNT=$(echo "$FILES" | wc -w)
          echo "files=$FILES" >> $GITHUB_OUTPUT
          echo "count=$COUNT" >> $GITHUB_OUTPUT

      - name: AI Review
        if: steps.changed.outputs.count > 0
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            Review this PR. Changed source files: ${{ steps.changed.outputs.files }}

            Focus on bugs, security, and performance. Skip style issues (linter handles that).
            Be specific: quote code, explain the issue, show the fix.
            If everything looks good, say so in one line.

  # ──────────────────────────────────────────
  # Job 3: AI Security Scan (PRs only)
  # 任务 3：AI 安全扫描（仅 PR）
  # ──────────────────────────────────────────
  ai-security:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    needs: standard-ci
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep -E '\.(js|ts|py|go|java)$' \
            | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: AI Security Scan
        if: steps.changed.outputs.files != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            Security-only scan of: ${{ steps.changed.outputs.files }}
            Check for: hardcoded secrets, injection, auth bypass, SSRF, data exposure.
            Only report confirmed or highly likely issues.
            If clean, respond: "No security issues found."

  # ──────────────────────────────────────────
  # Job 4: AI Coverage Analysis (main only)
  # 任务 4：AI 覆盖率分析（仅主分支）
  # ──────────────────────────────────────────
  ai-coverage:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: standard-ci
    steps:
      - uses: actions/checkout@v4

      - name: Download coverage
        uses: actions/download-artifact@v4
        with:
          name: coverage
          path: coverage/

      - name: Check coverage
        id: cov
        run: |
          TOTAL=$(node -e "console.log(require('./coverage/coverage-summary.json').total.lines.pct)")
          echo "total=$TOTAL" >> $GITHUB_OUTPUT

      - name: AI Coverage Report
        if: steps.cov.outputs.total < 80
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            Coverage is ${{ steps.cov.outputs.total }}% (target: 80%).
            Create a brief issue listing the top 5 files needing tests.
```

### GitLab Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - ai-review
  - deploy

variables:
  NODE_VERSION: "18"

# Standard testing / 标准测试
test:
  stage: test
  image: node:${NODE_VERSION}-alpine
  script:
    - npm ci
    - npm run lint
    - npm test -- --coverage
  artifacts:
    paths:
      - coverage/
    expire_in: 1 day

# AI review on merge requests / MR 上的 AI 审查
ai-review:
  stage: ai-review
  image: node:${NODE_VERSION}-alpine
  only:
    - merge_requests
  needs:
    - test
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      DIFF=$(git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD)

      if [ -z "$DIFF" ]; then
        echo "No changes to review"
        exit 0
      fi

      REVIEW=$(echo "$DIFF" | claude -p \
        --model claude-sonnet-4-20250514 \
        "Review this merge request. Focus on bugs and security.
         MR: $CI_MERGE_REQUEST_TITLE
         Be concise and actionable.")

      # Post to MR
      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --header "Content-Type: application/json" \
        --data "{\"body\": $(echo "$REVIEW" | jq -Rs .)}" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"

# AI security scan / AI 安全扫描
ai-security:
  stage: ai-review
  image: node:${NODE_VERSION}-alpine
  only:
    - merge_requests
  needs:
    - test
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      FILES=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD \
        | grep -E '\.(js|ts|py)$' | tr '\n' ' ')

      if [ -z "$FILES" ]; then
        echo "No source files changed"
        exit 0
      fi

      RESULT=$(claude -p \
        --model claude-haiku-4-20250514 \
        "Security scan these files: $FILES
         Check OWASP Top 10. Only report real issues.
         If clean, say PASS.")

      if echo "$RESULT" | grep -q "PASS"; then
        echo "Security scan passed"
      else
        echo "Security issues found:"
        echo "$RESULT"
        exit 1
      fi
```

---

## Troubleshooting

### Common Issues and Solutions

> 常见问题及解决方案。

#### 1. "Authentication failed" in CI

```
Error: 401 Unauthorized — Invalid API key
```

**Cause:** `ANTHROPIC_API_KEY` secret not set or has wrong value.

**Fix:**

```bash
# Verify the secret is accessible / 验证 secret 是否可访问
- name: Debug auth
  run: |
    if [ -z "$ANTHROPIC_API_KEY" ]; then
      echo "ERROR: ANTHROPIC_API_KEY is not set"
      exit 1
    fi
    echo "API key starts with: ${ANTHROPIC_API_KEY:0:10}..."
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

> Check: Did you add the secret to the correct repo? Is it a repository secret, not an environment secret?

#### 2. "Rate limited" in CI

```
Error: 429 Too Many Requests
```

**Cause:** Too many concurrent CI jobs calling the API.

**Fix:**

```yaml
# Add concurrency control / 添加并发控制
concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.sha }}
  cancel-in-progress: true

# Add retry with backoff / 添加退避重试
- name: AI Review with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 5
    max_attempts: 3
    retry_wait_seconds: 30
    command: |
      claude -p "Review this code..."
```

#### 3. Context too large

```
Error: Request too large — exceeds model context window
```

**Cause:** Trying to send too many files or a very large diff.

**Fix:**

```yaml
# Limit diff size / 限制 diff 大小
- name: Get manageable diff
  run: |
    DIFF=$(git diff origin/${{ github.base_ref }}...HEAD -- '*.js' '*.ts' | head -c 50000)
    echo "$DIFF" > /tmp/diff.txt

# Or split review by file / 或按文件分割审查
- name: Review per file
  run: |
    for file in $(git diff --name-only origin/${{ github.base_ref }}...HEAD | head -10); do
      echo "Reviewing $file..."
      git diff origin/${{ github.base_ref }}...HEAD -- "$file" | \
        claude -p --model claude-haiku-4-20250514 \
        "Quick review of $file. Critical issues only."
    done
```

#### 4. CI timeout

```
Error: The job exceeded the maximum time limit
```

**Cause:** Claude is taking too long (usually on very large reviews).

**Fix:**

```yaml
# Set job timeout / 设置任务超时
jobs:
  ai-review:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Kill after 10 minutes / 10 分钟后终止

    steps:
      - name: AI Review with timeout
        timeout-minutes: 5  # Per-step timeout / 单步超时
        uses: anthropics/claude-code-action@v1
        with:
          max_turns: 1  # Single pass, no back-and-forth / 单次通过
          # ...
```

#### 5. PR comments not posting

**Cause:** Missing permissions.

**Fix:**

```yaml
# Ensure correct permissions / 确保正确的权限
permissions:
  contents: read
  pull-requests: write  # Required for PR comments / 发布 PR 评论必需
  issues: write         # Required for issue comments / 发布 issue 评论必需
```

For GitHub Apps, also check: Settings > Actions > General > Workflow permissions > "Read and write permissions".

#### 6. Inconsistent review quality

**Cause:** Vague prompts produce vague reviews.

**Fix:** Be specific in your review prompt.

```yaml
# Bad: vague prompt / 差：模糊的提示
prompt: "Review this code"

# Good: specific prompt with criteria / 好：具体的提示和标准
prompt: |
  Review ONLY for these specific issues:
  1. SQL queries without parameterized inputs
  2. API endpoints without authentication checks
  3. User input used in file paths without sanitization
  4. Secrets or credentials in source code

  For each issue, show: file, line, issue, fix.
  If no issues, respond with "PASS".
```

#### 7. High costs from CI runs

**Symptoms:** Unexpected API bills.

**Fix checklist:**

```yaml
# 1. Use Haiku for simple checks / 用 Haiku 做简单检查
model: claude-haiku-4-20250514  # Not Sonnet or Opus

# 2. Skip unchanged files / 跳过未变更的文件
if: steps.changed.outputs.count > 0

# 3. Skip bot PRs / 跳过机器人 PR
if: github.actor != 'dependabot[bot]' && github.actor != 'renovate[bot]'

# 4. Skip draft PRs / 跳过草稿 PR
if: github.event.pull_request.draft == false

# 5. Limit to source files / 限制为源文件
FILES=$(git diff --name-only ... | grep -E '\.(js|ts|py)$')

# 6. Set max_turns: 1 / 设置单次通过
max_turns: 1

# 7. Add concurrency limits / 添加并发限制
concurrency:
  group: ai-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

### Monitoring AI CI Costs

Track your spending with a simple script:

```bash
#!/bin/bash
# scripts/check-ai-costs.sh
# Run monthly to track API usage / 每月运行以跟踪 API 使用情况

echo "=== AI CI Cost Report ==="
echo "Month: $(date +%Y-%m)"

# Count workflow runs this month / 统计本月工作流运行次数
RUNS=$(gh run list --workflow=ai-ci.yml --created ">=$(date +%Y-%m-01)" --json conclusion -q 'length')
echo "Total AI CI runs: $RUNS"

# Estimate cost (rough: $0.25 avg per run with mixed models)
# 估算费用（粗略：混合模型每次运行平均 $0.25）
COST=$(echo "$RUNS * 0.25" | bc)
echo "Estimated cost: \$$COST"
echo ""
echo "To reduce costs:"
echo "  - Switch more checks to Haiku"
echo "  - Add file-count thresholds"
echo "  - Reduce review frequency on low-risk PRs"
```

---

*Previous guide: [End-to-End Project](./11-end-to-end-project.md) — Build a complete project with AI.*
