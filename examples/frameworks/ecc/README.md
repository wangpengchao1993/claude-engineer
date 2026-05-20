# Everything Claude Code (ECC) — The All-in-One Agent Harness / 全能型 Agent 工具集

> ~100k+ GitHub stars | By Affaan M | MIT License
>
> ~10万+ GitHub 星标 | 作者：Affaan M | MIT 开源协议

---

## What Is ECC? / ECC 是什么？

ECC (Everything Claude Code) is a comprehensive harness that gives Claude Code
**skills, instincts, memory, security, and research-first development**. Think
of it as "an entire engineering department in a box" — 28 specialized agents
covering every stage of the software development lifecycle.

ECC（Everything Claude Code）是一个全面的 Agent 工具集，为 Claude Code 赋予
**技能、直觉、记忆、安全性和研究优先的开发方式**。可以把它想象成"一整个工程部门
装进一个工具箱"——28 个专业化 Agent 覆盖软件开发的每一个阶段。

### Origin / 起源

ECC won the **Anthropic hackathon** at Cerebral Valley in February 2026. It
started as a weekend project and has since grown into the most-starred agent
harness on GitHub.

ECC 于 2026 年 2 月在 Cerebral Valley 的 **Anthropic 黑客马拉松**中获奖。它最初
只是一个周末项目，如今已成长为 GitHub 上星标最多的 Agent 工具集。

---

## Key Components / 核心组件

| Component / 组件 | Count / 数量 | Examples / 示例 |
|---|---|---|
| **Agents / Agent** | 28 | Planning, TDD, Security Review, Build Error, Code Review (per language) / 规划、TDD、安全审查、构建错误、代码审查（按语言） |
| **Skills / 技能** | 119 | Research, refactor, test generation, dependency analysis / 研究、重构、测试生成、依赖分析 |
| **Commands / 命令** | 60 | `/plan`, `/tdd`, `/review`, `/secure`, `/build-fix` |
| **AgentShield Tests** | 1,282 | Injection detection, secret scanning, policy enforcement / 注入检测、密钥扫描、策略执行 |

---

## Supported Platforms / 支持的平台

ECC works across multiple AI coding tools, not just Claude Code:

ECC 可在多种 AI 编程工具中使用，不仅限于 Claude Code：

- **Claude Code** — primary / 主要平台
- **Cursor** — full support / 完全支持
- **Codex** — full support / 完全支持
- **OpenCode** — full support / 完全支持
- **Gemini** — community support / 社区支持
- **Zed** — community support / 社区支持

---

## Installation / 安装

ECC uses a **selective-install architecture** — you only install the agents
and skills you need, keeping your setup lean.

ECC 使用**按需安装架构**——你只需安装所需的 Agent 和技能，保持配置精简。

```bash
# Install the core harness / 安装核心工具集
npx ecc init

# Add specific agents / 添加特定 Agent
npx ecc add agent:planning agent:tdd agent:security

# Add a skill pack / 添加技能包
npx ecc add skills:research skills:refactor

# List all available agents / 列出所有可用 Agent
npx ecc list agents
```

---

## The 28 Agents / 28 个 Agent

ECC ships with agents for every stage of development:

ECC 为开发的每个阶段都配备了 Agent：

1. **Planning Agent / 规划 Agent** — breaks tasks into steps / 将任务拆分为步骤
2. **Research Agent / 研究 Agent** — research-first development / 研究优先开发
3. **TDD Agent / 测试驱动 Agent** — writes tests before code / 先写测试再写代码
4. **Security Review Agent / 安全审查 Agent** — finds vulnerabilities / 发现漏洞
5. **Build Error Agent / 构建错误 Agent** — diagnoses and fixes build failures / 诊断并修复构建失败
6. **Code Review Agents / 代码审查 Agent** — language-specific review for TypeScript, Python, Go, Rust, Java, Kotlin, C++ / 针对各语言的代码审查
7. **Refactor Agent / 重构 Agent** — safe, incremental refactoring / 安全的增量重构
8. **Documentation Agent / 文档 Agent** — generates and updates docs / 生成和更新文档
9. **Performance Agent / 性能 Agent** — profiles and optimizes / 分析和优化性能
10. **Migration Agent / 迁移 Agent** — handles version upgrades / 处理版本升级
11. ...and more (dependency, deployment, monitoring, etc.) / 以及更多（依赖、部署、监控等）

---

## Security: AgentShield / 安全：AgentShield

AgentShield is ECC's built-in security scanner. It protects your codebase from
prompt injection, secret leaks, and policy violations.

AgentShield 是 ECC 的内置安全扫描器。它保护你的代码库免受提示注入、密钥泄露和
策略违规的影响。

| Feature / 功能 | Detail / 详情 |
|---|---|
| **Test suite / 测试套件** | 1,282 tests covering injection, exfiltration, and abuse patterns / 1,282 项测试覆盖注入、数据泄露和滥用模式 |
| **Static analysis / 静态分析** | 102 rules for common vulnerabilities / 102 条常见漏洞规则 |
| **`--opus` flag / `--opus` 标志** | Activates the red-team/blue-team/auditor pipeline for deep security review / 激活红队/蓝队/审计员流水线进行深度安全审查 |

```bash
# Run a security scan / 运行安全扫描
npx ecc secure --scan

# Deep review with red-team pipeline / 使用红队流水线进行深度审查
npx ecc secure --opus
```

---

## Language Support / 语言支持

ECC provides language-specific agents and skills for:

ECC 为以下语言提供专门的 Agent 和技能：

- **TypeScript / JavaScript**
- **Python**
- **Go**
- **Rust**
- **Java**
- **Kotlin**
- **C++**

Each language has a dedicated code review agent that understands idiomatic
patterns, common pitfalls, and best practices for that ecosystem.

每种语言都有专门的代码审查 Agent，了解该生态系统的惯用模式、常见陷阱和最佳实践。

---

## ECC vs Superpowers / ECC 与 Superpowers 对比

| Aspect / 方面 | ECC | Superpowers |
|---|---|---|
| **Scope / 范围** | Broad — 28 agents, 119 skills, security scanner / 广泛——28 个 Agent、119 个技能、安全扫描器 | Focused — methodology-driven workflow / 专注——方法论驱动的工作流 |
| **Philosophy / 理念** | "Everything in one harness" / "一个工具集包含一切" | "Do fewer things, do them well" / "少做事，做好事" |
| **Security / 安全** | AgentShield with 1,282 tests / AgentShield 含 1,282 项测试 | Basic guardrails / 基本防护 |
| **Best for / 最适合** | Large teams, complex projects, security-critical work / 大型团队、复杂项目、安全关键工作 | Solo devs, rapid prototyping, learning / 独立开发者、快速原型、学习 |

Both are excellent tools. ECC is broader in scope; Superpowers offers a more
focused methodology. Many developers use both.

两者都是出色的工具。ECC 范围更广；Superpowers 提供更专注的方法论。许多开发者两者兼用。

---

## Learn More / 了解更多

- GitHub: [github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- Documentation / 文档: included in the repository / 包含在仓库中
- Community / 社区: GitHub Discussions

---

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

Before installing ECC, you need:
在安装 ECC 之前，你需要：

1. **Node.js 18+**
   - Windows: Download from https://nodejs.org → run installer → restart terminal
   - macOS: `brew install node` or download from https://nodejs.org
   - Linux: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs`
   - Verify: `node --version` (should show v18.x or higher)

2. **Claude Code CLI**
   - Install: `npm install -g @anthropic-ai/claude-code`
   - Verify: `claude --version`
   - Login: `claude` (follow prompts to authenticate with your Anthropic API key)

3. **Git**
   - Windows: Download from https://git-scm.com
   - macOS: `xcode-select --install` or `brew install git`
   - Linux: `sudo apt install git`

### Step-by-Step Installation / 分步安装

ECC uses a **selective-install architecture** -- you pick only the agents and skills you need.
ECC 使用**按需安装架构** -- 你只需选择所需的 Agent 和技能。

#### All Platforms (Windows / macOS / Linux) / 所有平台

```bash
# Step 1: Open your project directory / 打开你的项目目录
cd /path/to/your/project

# Step 2: Initialize the ECC core harness / 初始化 ECC 核心工具集
npx ecc init

# Step 3: Add the agents you need / 添加你需要的 Agent
# Common starter set / 常用入门组合:
npx ecc add agent:planning agent:tdd agent:security agent:research

# Step 4: Add skill packs / 添加技能包
npx ecc add skills:research skills:refactor skills:test-generation

# Step 5: Verify installation / 验证安装
npx ecc list agents
# Should show: planning, tdd, security, research
# 应该显示：planning, tdd, security, research

# Step 6: Open Claude Code / 打开 Claude Code
claude
```

#### Platform-Specific Notes / 平台特定注意事项

**Windows (PowerShell):**
```powershell
# If npx is not found, ensure Node.js is in your PATH
# 如果 npx 未找到，确保 Node.js 在你的 PATH 中
$env:PATH += ";C:\Program Files\nodejs"

# Use PowerShell (not CMD) for best compatibility
# 使用 PowerShell（不要用 CMD）以获得最佳兼容性
npx ecc init
```

**macOS:**
```bash
# If you get permission errors / 如果遇到权限错误:
sudo npm install -g npx
# Or use nvm to manage Node.js versions / 或使用 nvm 管理 Node.js 版本
```

**Linux:**
```bash
# If npx hangs, ensure you have the latest npm / 如果 npx 卡住，确保 npm 是最新版本
sudo npm install -g npm@latest
npx ecc init
```

### Real-World Walkthrough / 真实操作演示

Here's a complete session building a "REST API authentication system" with ECC:
以下是使用 ECC 构建"REST API 认证系统"的完整会话：

```
# Step 1: Start Claude Code in your project
cd my-api-project
claude

# Step 2: Select the right agents for the task
You:    I need to add JWT authentication to my Express.js API

# Step 3: Research Agent kicks in first (research-first development!)
Claude: [Research Agent] Before implementing, let me research the current
        best practices for JWT auth in Express.js...
        [研究 Agent] 在实现之前，让我先研究 Express.js 中 JWT 认证的最新最佳实践...

        Findings / 研究结果:
        - Use `jsonwebtoken` v9+ with RS256 (not HS256) for production
          生产环境使用 RS256（而非 HS256）
        - Store refresh tokens in httpOnly cookies, not localStorage
          将刷新令牌存储在 httpOnly cookie 中，而非 localStorage
        - Implement token rotation for refresh tokens
          对刷新令牌实施轮换机制

        Should I proceed with these recommendations? (yes/no/changes)
        是否按照这些建议继续？（是/否/修改）

You:    yes

# Step 4: Planning Agent creates the implementation plan
Claude: [Planning Agent] Breaking this into 6 tasks:
        [规划 Agent] 将此拆分为 6 个任务：

        Task 1: Set up auth middleware skeleton + tests
        Task 2: Implement JWT token generation (access + refresh) + tests
        Task 3: Implement login endpoint with password hashing + tests
        Task 4: Implement token refresh endpoint + tests
        Task 5: Add role-based authorization (RBAC) + tests
        Task 6: Error handling and edge cases + tests

# Step 5: TDD Agent writes tests before code
Claude: [TDD Agent] Starting Task 1...
        [TDD Agent] 开始任务 1...

        Writing test: auth.middleware.test.js
        先写测试：auth.middleware.test.js
        ✅ Test written (RED - fails, middleware doesn't exist yet)
           测试已写好（红灯 - 失败，中间件尚不存在）

        Implementing: auth.middleware.js
        实现：auth.middleware.js
        ✅ Implementation done (GREEN - test passes!)
           实现完成（绿灯 - 测试通过！）

# Step 6: Security Review Agent scans the implementation
Claude: [Security Agent] Running AgentShield scan on auth code...
        [安全 Agent] 正在对认证代码运行 AgentShield 扫描...

        Scan results / 扫描结果:
        ⚠️  Warning: JWT secret loaded from hardcoded string
            警告：JWT 密钥从硬编码字符串加载
            Fix: Move to environment variable → process.env.JWT_SECRET
            修复：移至环境变量 → process.env.JWT_SECRET

        ⚠️  Warning: No rate limiting on login endpoint
            警告：登录端点没有速率限制
            Fix: Add express-rate-limit middleware
            修复：添加 express-rate-limit 中间件

        ✅ No injection vulnerabilities found
           未发现注入漏洞
        ✅ No secret leaks detected
           未检测到密钥泄露

        Applying fixes automatically...
        正在自动应用修复...

# Step 7: Code Review Agent (TypeScript-specific) reviews the final code
Claude: [Code Review Agent - TypeScript] Final review:
        [代码审查 Agent - TypeScript] 最终审查：

        ✅ All 24 tests passing
           全部 24 个测试通过
        ✅ Type safety: all functions properly typed
           类型安全：所有函数已正确类型化
        ✅ Error handling: all edge cases covered
           错误处理：所有边缘情况已覆盖
        ✅ Security scan: all warnings resolved
           安全扫描：所有警告已解决
        ✅ Code follows Express.js best practices
           代码遵循 Express.js 最佳实践
```

### Troubleshooting / 常见问题

| Problem / 问题 | Solution / 解决方案 |
|----------------|---------------------|
| `npx ecc init` fails with "command not found" / 命令未找到 | Ensure Node.js 18+ is installed: `node --version`. Reinstall Node.js if needed / 确保已安装 Node.js 18+，必要时重新安装 |
| Agents not responding in Claude Code / Agent 在 Claude Code 中无响应 | Run `npx ecc list agents` to verify installation. Re-add agents with `npx ecc add agent:<name>` / 运行 `npx ecc list agents` 验证安装，重新添加 Agent |
| AgentShield scan hangs / AgentShield 扫描卡住 | Try running with verbose output: `npx ecc secure --scan --verbose`. Check network connectivity / 尝试详细输出：`npx ecc secure --scan --verbose`，检查网络连接 |
| "Too many agents" performance issues / "Agent 过多"性能问题 | Use selective install -- only add agents you actually need: `npx ecc remove agent:<name>` / 使用按需安装，只保留实际需要的 Agent |
| Windows: `npx` permission denied / Windows 权限被拒绝 | Run PowerShell as Administrator, or use `npm exec ecc init` instead / 以管理员身份运行 PowerShell，或使用 `npm exec ecc init` |
| `--opus` flag not working / `--opus` 标志不起作用 | Ensure you have an Anthropic API key with Opus access configured / 确保已配置具有 Opus 访问权限的 Anthropic API 密钥 |

---

*This guide is part of the Claude Code Frameworks collection.*

*本指南是 Claude Code 框架合集的一部分。*
