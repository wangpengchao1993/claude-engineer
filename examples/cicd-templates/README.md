# CI/CD Templates for AI-Assisted Development

# AI 辅助开发的 CI/CD 模板

---

## Overview / 概述

This directory contains ready-to-use CI/CD templates that integrate Claude into your development pipeline. Copy these templates into your project and configure the required secrets to get started.

本目录包含可直接使用的 CI/CD 模板，将 Claude 集成到你的开发流程中。将这些模板复制到你的项目中并配置所需的密钥即可开始使用。

---

## Templates / 模板列表

### GitHub Actions

| Template / 模板 | Description / 描述 |
|---|---|
| [`ai-code-review.yml`](github-actions/ai-code-review.yml) | Automated PR code review using Claude. / 使用 Claude 自动审查 PR 代码。 |
| [`ai-test-gen.yml`](github-actions/ai-test-gen.yml) | Auto-generate missing tests for changed files. / 为变更文件自动生成缺失的测试。 |
| [`claude-code-action.yml`](github-actions/claude-code-action.yml) | Comprehensive workflow: review, test, and security check. / 综合工作流：审查、测试和安全检查。 |

### GitLab CI

| Template / 模板 | Description / 描述 |
|---|---|
| [`ai-review.yml`](gitlab-ci/ai-review.yml) | MR code review using Claude API. / 使用 Claude API 审查合并请求代码。 |

---

## Prerequisites / 前提条件

### GitHub Actions

1. **GitHub Account** — A repository where you have admin or write access.
   **GitHub 账户** — 拥有管理员或写入权限的仓库。

2. **Anthropic API Key** — Store it as a repository secret named `ANTHROPIC_API_KEY`.
   **Anthropic API 密钥** — 将其存储为名为 `ANTHROPIC_API_KEY` 的仓库密钥。
   - Go to: Repository > Settings > Secrets and variables > Actions > New repository secret
   - 前往：仓库 > Settings > Secrets and variables > Actions > New repository secret

3. **GitHub Token** — The built-in `GITHUB_TOKEN` is used for posting PR comments. For cross-repo operations, create a Personal Access Token (PAT).
   **GitHub Token** — 内置的 `GITHUB_TOKEN` 用于发布 PR 评论。跨仓库操作需创建个人访问令牌 (PAT)。

### GitLab CI

1. **GitLab Account** — A project where you have Maintainer access or higher.
   **GitLab 账户** — 拥有 Maintainer 或更高权限的项目。

2. **Anthropic API Key** — Store it as a CI/CD variable named `ANTHROPIC_API_KEY` (masked and protected).
   **Anthropic API 密钥** — 将其存储为名为 `ANTHROPIC_API_KEY` 的 CI/CD 变量（启用掩码和保护）。
   - Go to: Project > Settings > CI/CD > Variables > Add variable
   - 前往：项目 > Settings > CI/CD > Variables > Add variable

---

## How to Use / 使用方法

### GitHub Actions

```bash
# Copy the desired workflow into your project
# 将所需的工作流复制到你的项目中
mkdir -p .github/workflows
cp examples/cicd-templates/github-actions/ai-code-review.yml .github/workflows/
```

Then commit and push. The workflow will trigger automatically based on the configured events.

然后提交并推送。工作流将根据配置的事件自动触发。

### GitLab CI

```bash
# Copy and include in your .gitlab-ci.yml
# 复制并在 .gitlab-ci.yml 中引用
cp examples/cicd-templates/gitlab-ci/ai-review.yml .gitlab/
```

Then add to your `.gitlab-ci.yml`:

然后添加到你的 `.gitlab-ci.yml` 中：

```yaml
include:
  - local: '.gitlab/ai-review.yml'
```

---

## Cost Considerations / 成本考虑

AI-powered CI/CD workflows consume API tokens on every run. Plan accordingly.

AI 驱动的 CI/CD 工作流每次运行都会消耗 API 令牌。请合理规划。

### Recommended Model Selection / 推荐模型选择

| Use Case / 使用场景 | Recommended Model / 推荐模型 | Reason / 原因 |
|---|---|---|
| Quick PR review (small diffs) / 快速 PR 审查（小差异） | `claude-sonnet-4-20250514` | Fast, cost-effective. / 速度快，性价比高。 |
| Deep code review / 深度代码审查 | `claude-opus-4-20250514` | Thorough analysis. / 分析更深入。 |
| Test generation / 测试生成 | `claude-sonnet-4-20250514` | Good balance of quality and cost. / 质量和成本的良好平衡。 |
| Security audit / 安全审计 | `claude-opus-4-20250514` | Maximum accuracy for security. / 安全方面需要最高准确度。 |
| Commit message drafts / 提交消息草稿 | `claude-haiku-4-20250514` | Simple task, lowest cost. / 简单任务，成本最低。 |

### Cost Control Tips / 成本控制技巧

1. **Limit trigger scope** — Only review changed files, not the entire codebase.
   **限制触发范围** — 仅审查变更的文件，而非整个代码库。

2. **Use labels to gate reviews** — Require a specific label (e.g., `ai-review`) before triggering.
   **使用标签控制审查** — 需要特定标签（如 `ai-review`）才触发审查。

3. **Set max_tokens** — Cap the response length to control costs.
   **设置 max_tokens** — 限制响应长度以控制成本。

4. **Skip draft PRs** — Don't review PRs that are still in draft.
   **跳过草稿 PR** — 不审查仍处于草稿状态的 PR。

5. **Cache results** — Avoid re-reviewing unchanged files.
   **缓存结果** — 避免重复审查未变更的文件。

---

## Security Reminders / 安全提醒

- **Never** hardcode API keys in workflow files. Always use secrets/variables.
  **绝对不要** 在工作流文件中硬编码 API 密钥。始终使用密钥/变量。

- Review AI-generated suggestions before merging — they may introduce vulnerabilities.
  在合并前审查 AI 生成的建议 — 它们可能引入安全漏洞。

- See [`templates/security/security-checklist.md`](../../templates/security/security-checklist.md) for a comprehensive security checklist.
  参见 [`templates/security/security-checklist.md`](../../templates/security/security-checklist.md) 获取完整的安全检查清单。
