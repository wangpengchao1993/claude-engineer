# CI/CD 集成：AI 进入你的流水线

> 将 AI 从本地开发扩展到构建、测试和部署流水线。自动化代码审查、测试和发布说明。

## 目录

- [为什么要在 CI/CD 中使用 AI](#为什么要在-cicd-中使用-ai)
- [GitHub Actions 与 Claude Code Action](#github-actions-与-claude-code-action)
- [GitLab CI 集成](#gitlab-ci-集成)
- [预提交钩子与 AI](#预提交钩子与-ai)
- [自动化测试流水线](#自动化测试流水线)
- [CI 中的安全扫描](#ci-中的安全扫描)
- [成本控制](#成本控制)
- [完整工作流文件](#完整工作流文件)
- [故障排除](#故障排除)

---

## 为什么要在 CI/CD 中使用 AI

大多数团队只在开发阶段使用 Claude Code。这浪费了 AI 的巨大潜力。将 AI 集成到 CI/CD 中可以实现：

| 收益 | 示例 |
|------|------|
| **自动化 PR 审查** | 每个 PR 在人工审查前先由 AI 审查 |
| **测试缺口检测** | 每次推送时 AI 识别未测试的代码路径 |
| **发布说明** | 从提交历史自动生成 |
| **安全扫描** | AI 检查变更代码中的 OWASP 漏洞 |
| **文档更新** | 自动检测过时的文档 |

**核心原则：** 人类审查重要的事情，AI 处理其余的。

---

## GitHub Actions 与 Claude Code Action

### `anthropics/claude-code-action` 是什么

官方 GitHub Action，可以在 CI 流水线中运行 Claude Code。能力包括：

- 读取仓库文件
- 分析差异和 Pull Request
- 直接在 PR 上发布审查评论
- 在 CI 环境中执行命令
- 生成报告和摘要

### 设置：将 API 密钥添加到 Secrets

**第一步：** 在仓库 Secrets 中添加 Anthropic API 密钥。

```
GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-...
```

**第二步：**（可选）添加模型偏好设置：

```
Name: CLAUDE_MODEL
Value: claude-sonnet-4-20250514
```

### 示例一：AI 驱动的 PR 审查

每个 Pull Request 创建或更新时自动运行 AI 审查并发布评论。

```yaml
# .github/workflows/ai-review.yml
name: AI PR 审查
on:
  pull_request:
    types: [opened, synchronize, reopened]

# 发布评论所需的权限
permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest
    # 跳过草稿和机器人 PR
    if: github.event.pull_request.draft == false && github.actor != 'dependabot[bot]'

    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 获取变更文件
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT
          echo "count=$(echo $FILES | wc -w)" >> $GITHUB_OUTPUT

      - name: AI 审查
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: ${{ vars.CLAUDE_MODEL || 'claude-sonnet-4-20250514' }}
          prompt: |
            你是一名高级代码审查员。审查这个 Pull Request。

            PR 标题：${{ github.event.pull_request.title }}
            PR 描述：${{ github.event.pull_request.body }}
            变更文件（${{ steps.changed.outputs.count }} 个）：${{ steps.changed.outputs.files }}

            审查以下方面：
            1. **Bug**：逻辑错误、空值处理、竞争条件、边界情况
            2. **安全**：注入、认证问题、数据泄露、SSRF
            3. **性能**：N+1 查询、缺失索引、不必要的计算
            4. **测试**：新代码路径是否有测试？遗漏的边界情况测试？
            5. **代码质量**：DRY 违反、命名不清晰、缺少文档

            对每个发现的问题：
            - 说明严重程度（严重 / 警告 / 建议）
            - 引用具体代码
            - 解释为什么是问题
            - 展示修复方案

            如果代码没有问题，简要说明即可。不要编造问题。
```

### 示例二：AI 测试建议

推送代码时检测未测试的代码并建议测试用例。

```yaml
# .github/workflows/ai-test-suggestions.yml
name: AI 测试建议
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

      - name: 获取变更的源文件
        id: changed
        run: |
          # 只获取源文件，排除测试文件
          FILES=$(git diff --name-only HEAD~1 HEAD -- 'src/' | grep -v '\.test\.' | grep -v '\.spec\.' | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: 检查对应的测试文件
        id: coverage
        run: |
          MISSING=""
          for file in ${{ steps.changed.outputs.files }}; do
            test_file=$(echo "$file" | sed 's/\.js/.test.js/' | sed 's/\.ts/.test.ts/')
            if [ ! -f "$test_file" ]; then
              MISSING="$MISSING $file"
            fi
          done
          echo "missing=$MISSING" >> $GITHUB_OUTPUT

      - name: AI 测试建议
        if: steps.coverage.outputs.missing != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            以下源文件被修改了但没有对应的测试文件：
            ${{ steps.coverage.outputs.missing }}

            对每个文件：
            1. 阅读源代码
            2. 识别关键函数/方法
            3. 编写完整的测试文件（使用项目现有的测试框架）
            4. 覆盖：正常路径、错误情况、边界情况

            输出每个测试文件的路径和完整内容。
```

### 示例三：AI 辅助发布说明

创建 Release 时自动从提交历史生成发布说明。

```yaml
# .github/workflows/ai-release-notes.yml
name: AI 发布说明
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

      - name: 获取上次发布以来的提交
        id: commits
        run: |
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREV_TAG" ]; then
            COMMITS=$(git log --oneline)
          else
            COMMITS=$(git log --oneline "$PREV_TAG"..HEAD)
          fi
          echo "$COMMITS" > /tmp/commits.txt
          echo "count=$(echo "$COMMITS" | wc -l)" >> $GITHUB_OUTPUT

      - name: 生成发布说明
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            为版本 ${{ github.event.release.tag_name }} 生成发布说明。

            上次发布以来的提交：
            $(cat /tmp/commits.txt)

            格式要求：
            ## 新功能
            - 功能描述（来自 feat: 提交）

            ## Bug 修复
            - 修复描述（来自 fix: 提交）

            ## 改进
            - 其他变更（重构、性能等）

            ## 破坏性变更
            - 任何破坏性变更（来自包含 BREAKING CHANGE 的提交）

            面向终端用户而非开发者编写。简洁明了。

      - name: 更新 Release 正文
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release edit ${{ github.event.release.tag_name }} \
            --notes-file /tmp/release-notes.md
```

---

## GitLab CI 集成

### GitLab CI 等效配置

GitLab CI 没有预构建的 Claude Code Action，所以我们直接使用 CLI。

### MR 上的 AI 审查

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
      # 获取差异
      DIFF=$(git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD)

      # 运行 Claude 审查
      REVIEW=$(echo "$DIFF" | claude -p \
        --model claude-sonnet-4-20250514 \
        "审查这个合并请求的差异。重点关注 bug、安全和性能问题。
         MR 标题：$CI_MERGE_REQUEST_TITLE
         以 Markdown 格式输出。")

      # 发布评论到 MR
      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --header "Content-Type: application/json" \
        --data "{\"body\": $(echo "$REVIEW" | jq -Rs .)}" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
```

### GitLab 上的 AI 测试建议

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
      # 找到没有测试的变更源文件
      CHANGED=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD \
        | grep -E '\.(js|ts|py)$' \
        | grep -v '\.test\.' \
        | grep -v '\.spec\.' \
        | grep -v '__tests__')

      if [ -z "$CHANGED" ]; then
        echo "没有源文件变更，跳过。"
        exit 0
      fi

      echo "没有测试的变更文件：$CHANGED"

      claude -p \
        --model claude-sonnet-4-20250514 \
        "这些文件被修改了但可能缺少测试：$CHANGED
         阅读每个文件并建议测试用例。以 Markdown 格式输出。"
```

---

## 预提交钩子与 AI

### 为什么要用预提交钩子？

预提交钩子在代码进入仓库**之前**捕获问题。在这里加入 AI 意味着：

- 安全问题在提交前就被发现，而不是在 CI 中（节省时间和费用）
- 代码质量反馈是即时的
- 开发者能立即从 AI 建议中学习

### 使用 Husky + Claude Code 设置

```bash
# 安装 husky
npm install -D husky
npx husky init
```

### AI 安全检查钩子

```bash
#!/bin/bash
# .husky/pre-commit

# 获取暂存的源文件
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|py|go|java)$')

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

echo "正在对暂存文件运行 AI 安全检查..."

# 用 Haiku 做快速安全扫描（速度快、成本低）
ISSUES=$(git diff --cached | claude -p \
  --model claude-haiku-4-20250514 \
  --max-turns 1 \
  "仅扫描安全问题。检查以下方面：
   - 硬编码的密钥/密码/API key
   - SQL 注入
   - XSS 漏洞
   - 路径遍历
   - 不安全的反序列化

   如果没有问题，只回复：PASS
   如果有问题，列出文件和行号。")

if echo "$ISSUES" | grep -q "PASS"; then
  echo "安全检查通过"
  exit 0
else
  echo "发现安全问题："
  echo "$ISSUES"
  echo ""
  echo "请修复上述问题，或使用 'git commit --no-verify' 跳过检查。"
  exit 1
fi
```

### AI 代码质量检查钩子

```bash
#!/bin/bash
# .husky/pre-commit（组合钩子版本）

STAGED=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED" ]; then
  exit 0
fi

# 第一步：标准 lint（快速、免费）
echo "运行 ESLint..."
npx eslint $STAGED --fix
LINT_EXIT=$?

# 第二步：自动格式化
echo "运行 Prettier..."
npx prettier --write $STAGED

# 第三步：重新暂存修复的文件
git add $STAGED

# 第四步：只在 lint 通过后运行 AI 检查（避免在有语法错误的代码上浪费 token）
if [ $LINT_EXIT -eq 0 ]; then
  echo "运行 AI 质量检查..."
  DIFF=$(git diff --cached)

  if [ -n "$DIFF" ]; then
    QUALITY=$(echo "$DIFF" | claude -p \
      --model claude-haiku-4-20250514 \
      --max-turns 1 \
      "快速代码审查。只标记严重问题：
       - 明显的 bug
       - 安全漏洞
       - 数据丢失风险
       没有严重问题则回复 PASS。简洁回复。")

    if ! echo "$QUALITY" | grep -q "PASS"; then
      echo "AI 发现潜在问题："
      echo "$QUALITY"
      echo ""
      read -p "仍然提交？(y/N) " -n 1 -r
      echo
      if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
      fi
    fi
  fi
fi
```

### 使用 Claude Code 内置 Hooks

Claude Code 有内置的 hooks 系统，可以在特定事件上运行。这与 git hooks 不同 — 这些在 Claude Code 会话内运行。

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreCommit": [
      {
        "command": "npm run lint && npm test",
        "description": "提交前运行 lint 和测试"
      }
    ],
    "PostCommit": [
      {
        "command": "echo '提交成功'",
        "description": "确认消息"
      }
    ]
  }
}
```

---

## 自动化测试流水线

### AI 生成测试，CI 运行测试

这个流水线让 AI 为未测试的代码生成测试，然后立即运行验证。

```yaml
# .github/workflows/ai-test-generation.yml
name: AI 测试生成
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

      - name: 安装依赖
        run: npm ci

      - name: 运行现有测试并获取覆盖率
        run: |
          npx jest --coverage --coverageReporters=json-summary || true
          # 提取覆盖率低于 80% 的文件
          node -e "
            const cov = require('./coverage/coverage-summary.json');
            const uncovered = Object.entries(cov)
              .filter(([k, v]) => k !== 'total' && v.lines.pct < 80)
              .map(([k]) => k.replace(process.cwd() + '/', ''));
            console.log(uncovered.join(' '));
          " > /tmp/uncovered.txt

      - name: 为未覆盖的代码生成测试
        if: "hashFiles('/tmp/uncovered.txt') != ''"
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            这些文件的测试覆盖率低于 80%：
            $(cat /tmp/uncovered.txt)

            对每个文件：
            1. 阅读源代码
            2. 检查是否已有测试文件
            3. 如果有，添加缺失的测试用例
            4. 如果没有，创建完整的测试文件

            使用项目现有的测试模式和框架。
            将测试文件放在源文件旁边，命名为 *.test.js。

      - name: 运行包含新测试的测试套件
        run: |
          npx jest --passWithNoTests
          echo "test_result=$?" >> $GITHUB_ENV

      - name: 创建包含新测试的 PR
        if: env.test_result == '0'
        run: |
          git config user.name "AI 测试机器人"
          git config user.email "ai-tests@noreply.github.com"

          BRANCH="ai/tests-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"

          # 只添加测试文件
          git add '*.test.js' '*.test.ts' '*.spec.js' '*.spec.ts'

          if git diff --cached --quiet; then
            echo "没有生成新测试"
            exit 0
          fi

          git commit -m "test: 为未覆盖的代码添加 AI 生成的测试"
          git push origin "$BRANCH"

          gh pr create \
            --title "添加未覆盖代码的测试" \
            --body "AI 为覆盖率低于 80% 的文件生成的测试。
                    请在合并前审查。" \
            --label "ai-generated,tests"
```

### 覆盖率关卡与 AI 分析

```yaml
coverage-gate:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - uses: actions/checkout@v4

    - name: 检查覆盖率阈值
      id: coverage
      run: |
        TOTAL=$(node -e "console.log(require('./coverage/coverage-summary.json').total.lines.pct)")
        echo "coverage=$TOTAL" >> $GITHUB_OUTPUT
        if (( $(echo "$TOTAL < 80" | bc -l) )); then
          echo "below_threshold=true" >> $GITHUB_OUTPUT
        fi

    - name: AI 覆盖率分析
      if: steps.coverage.outputs.below_threshold == 'true'
      uses: anthropics/claude-code-action@v1
      with:
        anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
        model: claude-haiku-4-20250514
        prompt: |
          测试覆盖率为 ${{ steps.coverage.outputs.coverage }}%（阈值：80%）。

          分析覆盖率报告并说明：
          1. 哪些文件/函数覆盖率最低？
          2. 添加哪些测试影响最大？
          3. 估算达到 80% 需要的工作量

          要具体可行。以 PR 评论格式输出。
```

---

## CI 中的安全扫描

### PR 中的 OWASP 漏洞检查

```yaml
# .github/workflows/ai-security-scan.yml
name: AI 安全扫描
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

      - name: 获取变更文件
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep -E '\.(js|ts|py|go|java|rb)$' \
            | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: AI 安全扫描
        if: steps.changed.outputs.files != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            对这个 PR 中的变更文件进行安全审计。
            变更文件：${{ steps.changed.outputs.files }}

            检查 OWASP Top 10 漏洞：
            1. **A01 访问控制失效** — 缺少认证检查、IDOR、权限提升
            2. **A02 密码学失败** — 弱哈希、明文密钥、不安全的随机数
            3. **A03 注入** — SQL、NoSQL、OS 命令、LDAP 注入
            4. **A04 不安全设计** — 缺少速率限制、业务逻辑缺陷
            5. **A05 安全配置错误** — 调试模式、默认凭据、详细错误
            6. **A06 易受攻击的组件** — 依赖中的已知 CVE
            7. **A07 认证失败** — 允许弱密码、缺少 MFA、会话问题
            8. **A08 数据完整性失败** — 反序列化、未签名的更新
            9. **A09 日志记录失败** — 缺少审计日志、日志中的敏感数据
            10. **A10 SSRF** — 用户控制的 URL、未验证的重定向

            对每个发现的漏洞：
            ```
            [严重程度：严重/高/中/低]
            文件：path/to/file.js:行号
            问题：漏洞描述
            影响：攻击者可以做什么
            修复：具体的代码修复
            ```

            如果没有发现漏洞，回复"变更文件中未发现安全问题。"
```

### 依赖漏洞检查

```yaml
# .github/workflows/ai-dependency-check.yml
name: AI 依赖检查
on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'
      - 'requirements.txt'
      - 'go.mod'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 运行 npm audit
        id: audit
        run: |
          npm audit --json > /tmp/audit.json 2>/dev/null || true
          VULNS=$(node -e "const a=require('/tmp/audit.json'); console.log(a.metadata?.vulnerabilities?.total || 0)")
          echo "vulnerabilities=$VULNS" >> $GITHUB_OUTPUT

      - name: AI 依赖分析
        if: steps.audit.outputs.vulnerabilities != '0'
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            npm audit 发现 ${{ steps.audit.outputs.vulnerabilities }} 个漏洞。
            审计报告：$(cat /tmp/audit.json)

            对每个漏洞：
            1. 用通俗语言解释风险
            2. 在我们的使用场景中是否可被利用？
            3. 修复方案是什么？（升级路径或替代方案）

            按实际风险排序，而非仅按严重程度评分。
```

---

## 成本控制

CI 中的 AI 如果管理不当会很快变得昂贵。以下是控制成本的策略。

### 策略一：只分析变更的文件

```yaml
# 不要分析整个仓库 — 只分析变更的文件
- name: 获取变更文件
  run: |
    FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
    echo "files=$FILES" >> $GITHUB_OUTPUT
```

### 策略二：简单检查用 Haiku

```yaml
# Haiku（$0.25/M 输入）用于简单检查
# Sonnet（$3/M 输入）用于深度审查

# Haiku：lint、格式检查、简单安全扫描
- name: 快速 AI 检查
  uses: anthropics/claude-code-action@v1
  with:
    model: claude-haiku-4-20250514
    prompt: "只扫描严重问题..."

# Sonnet：完整代码审查、架构审查
- name: 深度 AI 审查
  uses: anthropics/claude-code-action@v1
  with:
    model: claude-sonnet-4-20250514
    prompt: "全面的代码审查..."
```

### 策略三：条件执行

```yaml
# 只在有大量变更的 PR 上运行 AI 审查
- name: 检查变更规模
  id: size
  run: |
    LINES=$(git diff --stat origin/${{ github.base_ref }}...HEAD | tail -1 | awk '{print $4+$6}')
    echo "lines_changed=$LINES" >> $GITHUB_OUTPUT

- name: AI 审查（仅大型 PR）
  if: steps.size.outputs.lines_changed > 50
  uses: anthropics/claude-code-action@v1
  with:
    # ...
```

### 策略四：跳过特定文件类型

```yaml
# 跳过文档、配置和生成的文件
- name: 过滤待审查文件
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

### 策略五：设置 Token 预算

```yaml
# 使用 max-turns 限制 token 用量
- name: 预算控制的审查
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    model: claude-haiku-4-20250514
    max_turns: 1
    prompt: "单次审查。简洁回复。"
```

### 成本估算表

| 场景 | 模型 | 文件数 | Token 数 | 单次费用 |
|------|------|--------|---------|---------|
| PR 审查（小型） | Haiku | 3 文件 | ~15K | ~$0.005 |
| PR 审查（中型） | Sonnet | 10 文件 | ~50K | ~$0.25 |
| PR 审查（大型） | Sonnet | 30 文件 | ~150K | ~$0.75 |
| 安全扫描 | Sonnet | 10 文件 | ~40K | ~$0.20 |
| 发布说明 | Haiku | N/A | ~10K | ~$0.003 |
| 测试生成 | Sonnet | 5 文件 | ~80K | ~$0.40 |

> **活跃团队月度估算（50 个 PR/月）：**
> - 仅 Haiku：约 $5-10/月
> - Haiku + Sonnet 混合：约 $20-50/月
> - 仅 Sonnet：约 $50-100/月

---

## 完整工作流文件

### 一体化 CI 流水线

复制粘贴这个完整的工作流文件，它将审查、安全和测试合并在一个流水线中。

```yaml
# .github/workflows/ai-ci.yml
name: AI 驱动的 CI
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

      - name: 上传覆盖率
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  # ──────────────────────────────────────────
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

      - name: 获取变更的源文件
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

      - name: AI 审查
        if: steps.changed.outputs.count > 0
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-20250514
          prompt: |
            审查这个 PR。变更的源文件：${{ steps.changed.outputs.files }}

            重点关注 bug、安全和性能。跳过代码风格问题（linter 会处理）。
            具体说明：引用代码，解释问题，展示修复方案。
            如果一切正常，用一行话说明。

  # ──────────────────────────────────────────
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

      - name: 获取变更文件
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep -E '\.(js|ts|py|go|java)$' \
            | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: AI 安全扫描
        if: steps.changed.outputs.files != ''
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            仅安全扫描：${{ steps.changed.outputs.files }}
            检查：硬编码密钥、注入、认证绕过、SSRF、数据泄露。
            只报告确认或高度可能的问题。
            如果没有问题，回复："未发现安全问题。"

  # ──────────────────────────────────────────
  # 任务 4：AI 覆盖率分析（仅主分支）
  # ──────────────────────────────────────────
  ai-coverage:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: standard-ci
    steps:
      - uses: actions/checkout@v4

      - name: 下载覆盖率
        uses: actions/download-artifact@v4
        with:
          name: coverage
          path: coverage/

      - name: 检查覆盖率
        id: cov
        run: |
          TOTAL=$(node -e "console.log(require('./coverage/coverage-summary.json').total.lines.pct)")
          echo "total=$TOTAL" >> $GITHUB_OUTPUT

      - name: AI 覆盖率报告
        if: steps.cov.outputs.total < 80
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-haiku-4-20250514
          prompt: |
            覆盖率为 ${{ steps.cov.outputs.total }}%（目标：80%）。
            创建简要 issue，列出最需要测试的前 5 个文件。
```

### GitLab 完整流水线

```yaml
# .gitlab-ci.yml
stages:
  - test
  - ai-review
  - deploy

variables:
  NODE_VERSION: "18"

# 标准测试
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

# MR 上的 AI 审查
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
        echo "没有变更需要审查"
        exit 0
      fi

      REVIEW=$(echo "$DIFF" | claude -p \
        --model claude-sonnet-4-20250514 \
        "审查这个合并请求。重点关注 bug 和安全问题。
         MR：$CI_MERGE_REQUEST_TITLE
         简洁且可操作。")

      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --header "Content-Type: application/json" \
        --data "{\"body\": $(echo "$REVIEW" | jq -Rs .)}" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"

# AI 安全扫描
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
        echo "没有源文件变更"
        exit 0
      fi

      RESULT=$(claude -p \
        --model claude-haiku-4-20250514 \
        "安全扫描这些文件：$FILES
         检查 OWASP Top 10。只报告真实问题。
         如果没有问题，回复 PASS。")

      if echo "$RESULT" | grep -q "PASS"; then
        echo "安全扫描通过"
      else
        echo "发现安全问题："
        echo "$RESULT"
        exit 1
      fi
```

---

## 故障排除

### 常见问题及解决方案

#### 1. CI 中认证失败

```
Error: 401 Unauthorized — Invalid API key
```

**原因：** `ANTHROPIC_API_KEY` secret 未设置或值错误。

**解决：**

```bash
# 验证 secret 是否可访问
- name: 调试认证
  run: |
    if [ -z "$ANTHROPIC_API_KEY" ]; then
      echo "错误：ANTHROPIC_API_KEY 未设置"
      exit 1
    fi
    echo "API key 开头：${ANTHROPIC_API_KEY:0:10}..."
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

> 检查：是否添加到了正确的仓库？是 repository secret 还是 environment secret？

#### 2. 速率限制

```
Error: 429 Too Many Requests
```

**原因：** 太多并发 CI 任务调用 API。

**解决：**

```yaml
# 添加并发控制
concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.sha }}
  cancel-in-progress: true

# 添加退避重试
- name: 带重试的 AI 审查
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 5
    max_attempts: 3
    retry_wait_seconds: 30
    command: |
      claude -p "审查这段代码..."
```

#### 3. 上下文过大

```
Error: Request too large — exceeds model context window
```

**原因：** 发送了太多文件或非常大的 diff。

**解决：**

```yaml
# 限制 diff 大小
- name: 获取可管理的 diff
  run: |
    DIFF=$(git diff origin/${{ github.base_ref }}...HEAD -- '*.js' '*.ts' | head -c 50000)
    echo "$DIFF" > /tmp/diff.txt

# 或按文件分割审查
- name: 逐文件审查
  run: |
    for file in $(git diff --name-only origin/${{ github.base_ref }}...HEAD | head -10); do
      echo "审查 $file..."
      git diff origin/${{ github.base_ref }}...HEAD -- "$file" | \
        claude -p --model claude-haiku-4-20250514 \
        "快速审查 $file。只报告严重问题。"
    done
```

#### 4. CI 超时

```
Error: The job exceeded the maximum time limit
```

**原因：** Claude 处理时间过长（通常是非常大的审查）。

**解决：**

```yaml
jobs:
  ai-review:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # 10 分钟后终止

    steps:
      - name: 带超时的 AI 审查
        timeout-minutes: 5  # 单步超时
        uses: anthropics/claude-code-action@v1
        with:
          max_turns: 1  # 单次通过，不来回对话
          # ...
```

#### 5. PR 评论未发布

**原因：** 权限不足。

**解决：**

```yaml
# 确保正确的权限
permissions:
  contents: read
  pull-requests: write  # 发布 PR 评论必需
  issues: write         # 发布 issue 评论必需
```

对于 GitHub Apps，还需检查：Settings > Actions > General > Workflow permissions > "Read and write permissions"。

#### 6. 审查质量不稳定

**原因：** 模糊的提示产生模糊的审查。

**解决：** 在审查提示中要具体。

```yaml
# 差：模糊的提示
prompt: "审查这段代码"

# 好：具体的提示和标准
prompt: |
  只检查以下具体问题：
  1. 没有参数化的 SQL 查询
  2. 没有认证检查的 API 端点
  3. 用户输入用于文件路径但未做清洗
  4. 源代码中的密钥或凭据

  对每个问题，展示：文件、行号、问题、修复方案。
  如果没有问题，回复 "PASS"。
```

#### 7. CI 运行费用过高

**症状：** 意外的 API 账单。

**检查清单：**

```yaml
# 1. 简单检查用 Haiku
model: claude-haiku-4-20250514  # 不是 Sonnet 或 Opus

# 2. 跳过无变更的情况
if: steps.changed.outputs.count > 0

# 3. 跳过机器人 PR
if: github.actor != 'dependabot[bot]' && github.actor != 'renovate[bot]'

# 4. 跳过草稿 PR
if: github.event.pull_request.draft == false

# 5. 限制为源文件
FILES=$(git diff --name-only ... | grep -E '\.(js|ts|py)$')

# 6. 设置单次通过
max_turns: 1

# 7. 添加并发限制
concurrency:
  group: ai-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

### 监控 AI CI 费用

用简单脚本跟踪支出：

```bash
#!/bin/bash
# scripts/check-ai-costs.sh
# 每月运行以跟踪 API 使用情况

echo "=== AI CI 费用报告 ==="
echo "月份：$(date +%Y-%m)"

# 统计本月工作流运行次数
RUNS=$(gh run list --workflow=ai-ci.yml --created ">=$(date +%Y-%m-01)" --json conclusion -q 'length')
echo "AI CI 总运行次数：$RUNS"

# 估算费用（粗略：混合模型每次运行平均 $0.25）
COST=$(echo "$RUNS * 0.25" | bc)
echo "预估费用：\$$COST"
echo ""
echo "降低费用的建议："
echo "  - 更多检查切换到 Haiku"
echo "  - 添加文件数量阈值"
echo "  - 降低低风险 PR 的审查频率"
```

---

*上一篇指南：[端到端实战项目](./11-end-to-end-project.md) — 用 AI 构建完整项目。*

---

## AI 产出的可观测性

将 AI 引入 CI/CD 后，需要监控 AI 本身的表现，而不仅仅是代码质量。

### 关键指标

| 指标 | 含义 | 告警阈值建议 |
|------|------|-------------|
| AI Review 误报率 | AI 标记的问题中实际不是问题的比例 | > 30% 需调优 prompt |
| AI 建议采纳率 | 开发者接受 AI 建议的比例 | < 40% 说明 AI 建议质量下降 |
| Token 消耗/PR | 每个 PR 的 AI 处理成本 | 突然翻倍需排查 |
| AI 处理延迟 | 从 PR 提交到 AI 审查完成的时间 | > 5分钟影响工作流 |

### AI 代码标记

在 commit 或 PR 中标记 AI 参与度，便于后续追溯：

```bash
# commit message 中标注
git commit -m "feat: add user auth

Co-Authored-By: Claude <noreply@anthropic.com>
AI-Assisted: code-generation"

# 或通过 PR label 自动标记
gh pr edit --add-label "ai-assisted"
```

### AI 代码的发布策略

AI 生成的代码在发布时需要额外谨慎：

- **Feature Flag 守护**：新功能默认关闭，灰度开放，确认无问题再全量
- **金丝雀发布**：AI 重构的模块先部署到 5% 流量，监控错误率
- **自动回滚触发**：错误率超过阈值（如 2x 基线）自动回滚，不等人工介入

---

[← 上一章：端到端实战](11-end-to-end-project.md) | [目录](../../README_zh.md) | [下一章：成本与模型选择 →](13-cost-and-model-selection.md)
