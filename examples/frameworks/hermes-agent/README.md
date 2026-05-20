# Hermes Agent — The Self-Evolving AI Agent / 自进化 AI 智能体

> **~140k GitHub Stars** | By [Nous Research](https://nousresearch.com) | Open Source
>
> **~14万 GitHub Stars** | 由 [Nous Research](https://nousresearch.com) 开发 | 开源

---

## What is Hermes Agent? / 什么是 Hermes Agent？

Hermes Agent is an AI agent that **learns and improves from every interaction**.
Unlike other frameworks where skills are static and hand-coded, Hermes **evolves**.

Hermes Agent 是一个**从每次交互中学习和改进**的 AI 智能体。
不同于其他技能固定、手动编写的框架，Hermes 会**自我进化**。

Think of it as **"an intern that gets better every day and never forgets what it learned."**

可以把它想象成**"一个每天都在进步、永远不会忘记所学知识的实习生。"**

Launched in February 2026, Hermes hit 140k stars in under 3 months and became
the #1 most-used AI agent on OpenRouter (224B tokens/day).

Hermes 于 2026 年 2 月发布，不到 3 个月即获得 14 万 stars，成为 OpenRouter 上
使用量最大的 AI 智能体（每日 2240 亿 tokens）。

---

## Core Differentiator / 核心差异化优势

Three pillars make Hermes unique:

三大支柱使 Hermes 与众不同：

1. **Self-Improving Skills / 自改进技能** — Skills get better each time they are used.
   技能在每次使用后都会变得更好。

2. **Persistent Memory / 持久记忆** — Context and knowledge carry across sessions.
   上下文和知识跨会话保留。

3. **Closed Learning Loop / 闭环学习** — Do, evaluate, learn, improve. Automatically.
   执行、评估、学习、改进，全自动。

---

## How It Learns / 学习原理

```
Task Execution  ──>  Evaluate Results  ──>  Update Skills  ──>  Better Next Time
  执行任务      ──>    评估结果        ──>    更新技能     ──>    下次做得更好
```

Each time Hermes completes a task, it:

每次 Hermes 完成任务时，它会：

1. **Execute** the task using its current skills / 用当前技能**执行**任务
2. **Evaluate** the outcome (Did it work? How well?) / **评估**结果（成功了吗？效果如何？）
3. **Extract patterns** from successes and failures / 从成功和失败中**提取模式**
4. **Update skills** so the next run is better / **更新技能**使下次执行更好

---

## Integration with Claude Code / 与 Claude Code 的集成

Hermes can **delegate coding tasks** to Claude Code via the terminal.
When Hermes needs to write code, edit files, or manage git, it hands off to Claude Code.

Hermes 可以通过终端**将编码任务委派**给 Claude Code。
当 Hermes 需要编写代码、编辑文件或管理 git 时，它会交给 Claude Code 处理。

### hermes-CCC — The Native Claude Code Port / 原生 Claude Code 移植版

**hermes-CCC** is the native port that runs entirely inside Claude Code:

**hermes-CCC** 是完全在 Claude Code 内部运行的原生移植版：

- **46 native skills** built for Claude Code / 为 Claude Code 构建的 **46 个原生技能**
- **No OAuth required** — works immediately / **无需 OAuth** — 开箱即用
- Runs as a Claude Code plugin / 作为 Claude Code 插件运行

---

## Key Features / 主要特性

| Feature / 特性 | Description / 描述 |
|---|---|
| **Persistent Memory** / 持久记忆 | Remembers context across sessions / 跨会话记忆上下文 |
| **Skill Marketplace** / 技能市场 | Share and download community skills / 分享和下载社区技能 |
| **Model-Agnostic** / 模型无关 | Works with any LLM backend / 兼容任何 LLM 后端 |
| **Self-Improving** / 自我改进 | Skills evolve with use / 技能随使用而进化 |

---

## Installation / 安装

### Option 1: Standalone / 独立安装

```bash
pip install hermes-agent
hermes init
```

### Option 2: Claude Code Plugin (hermes-CCC) / Claude Code 插件

```bash
claude install hermes-ccc
```

That's it — 46 skills are immediately available inside Claude Code.

就这么简单 — 46 个技能立即在 Claude Code 中可用。

---

## Hermes vs Superpowers / Hermes 与 Superpowers 对比

| Aspect / 方面 | Hermes Agent | Superpowers |
|---|---|---|
| **Skills** / 技能 | Self-evolving / 自进化 | Static methodology / 静态方法论 |
| **Learning** / 学习 | Automatic from usage / 自动从使用中学习 | Manual configuration / 手动配置 |
| **Memory** / 记忆 | Persistent across sessions / 跨会话持久 | Per-session / 每次会话 |
| **Approach** / 方式 | Adaptive agent / 自适应智能体 | Structured workflow / 结构化工作流 |

Both are excellent tools — Hermes excels when you want an agent that gets smarter over time,
while Superpowers excels at providing a consistent, structured development methodology.

两者都是优秀工具 — 当你想要一个随时间变聪明的智能体时 Hermes 更佳，
而 Superpowers 在提供一致的结构化开发方法论方面更强。

---

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

| Requirement / 要求 | Version / 版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for Claude Code / Claude Code 运行时 |
| **Claude Code CLI** | Latest / 最新 | AI coding assistant / AI 编码助手 |
| **Git** | 2.30+ | Version control / 版本控制 |
| **Python** | 3.10+ | Required for standalone Hermes / 独立版 Hermes 所需 |

#### Install Prerequisites / 安装前置条件

**Windows:**
```powershell
# Install Node.js via winget / 通过 winget 安装 Node.js
winget install OpenJS.NodeJS.LTS

# Install Git / 安装 Git
winget install Git.Git

# Install Python / 安装 Python
winget install Python.Python.3.12

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**macOS:**
```bash
# Install via Homebrew / 通过 Homebrew 安装
brew install node@18 git python@3.12

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**Linux (Ubuntu/Debian):**
```bash
# Install Node.js 18+ / 安装 Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs git python3 python3-pip

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### Step-by-Step Installation / 分步安装

#### Option A: Claude Code Plugin (Recommended) / Claude Code 插件（推荐）

```bash
# 1. Install the hermes-CCC plugin / 安装 hermes-CCC 插件
claude install hermes-ccc

# 2. Verify installation / 验证安装
claude
> /hermes status
# Should show: "Hermes CCC v2.x — 46 skills loaded"
# 应显示: "Hermes CCC v2.x — 46 skills loaded"
```

#### Option B: Standalone / 独立安装

```bash
# 1. Install Hermes Agent / 安装 Hermes Agent
pip install hermes-agent

# 2. Initialize Hermes / 初始化 Hermes
hermes init

# 3. Verify installation / 验证安装
hermes --version
# Should show: hermes-agent 2.x.x
```

### Verification / 验证

```bash
# Check all components / 检查所有组件
node --version          # Should be v18.x or higher / 应为 v18.x 或更高
claude --version        # Should show Claude Code CLI version / 应显示 Claude Code CLI 版本
hermes --version        # (Standalone only) Should show hermes-agent version / （仅独立版）
claude
> /hermes status        # (Plugin only) Should show 46 skills loaded / （仅插件版）应显示已加载 46 个技能
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete session showing Hermes learning and evolving across tasks.

以下是一个完整的会话演示，展示 Hermes 如何在任务中学习和进化。

### Step 1: Install hermes-CCC into Claude Code / 步骤1：安装 hermes-CCC 到 Claude Code

```
$ claude install hermes-ccc

Installing hermes-ccc...
✓ Downloaded hermes-ccc v2.4.1
✓ Registered 46 native skills
✓ Memory store initialized at ~/.hermes/memory.db

Plugin hermes-ccc installed successfully.
46 skills are now available in Claude Code.
```

### Step 2: First Task — Hermes Uses Baseline Skill / 步骤2：第一个任务 — Hermes 使用基线技能

```
$ claude
> Write a Python function to parse CSV files with error handling

Hermes [skill: file-parser v1] Executing with baseline skill...

I'll create a CSV parser with comprehensive error handling:

  def parse_csv(filepath, delimiter=',', encoding='utf-8'):
      """Parse CSV file with error handling."""
      import csv
      try:
          with open(filepath, 'r', encoding=encoding) as f:
              reader = csv.DictReader(f, delimiter=delimiter)
              return list(reader)
      except FileNotFoundError:
          raise ValueError(f"File not found: {filepath}")
      except csv.Error as e:
          raise ValueError(f"CSV parsing error at line {reader.line_num}: {e}")

Hermes [learning] Task completed. Outcome: SUCCESS
  - Pattern extracted: "CSV parsing benefits from DictReader over reader"
  - Skill 'file-parser' updated: v1 → v1.1 (added DictReader preference)
```

### Step 3: Second Task — Hermes Applies What It Learned / 步骤3：第二个任务 — Hermes 应用学到的知识

```
> Now parse a TSV file with the same approach

Hermes [skill: file-parser v1.1] Applying learned patterns...
  - Recalled: "DictReader preferred for tabular data"
  - Recalled: "delimiter should be parameterized"

I'll reuse the pattern from the CSV parser with TSV defaults:

  def parse_tsv(filepath, encoding='utf-8'):
      """Parse TSV file, reusing learned CSV patterns."""
      return parse_csv(filepath, delimiter='\t', encoding=encoding)

Hermes [learning] Task completed. Outcome: SUCCESS
  - Pattern extracted: "Tabular parsers should share a common base"
  - Skill 'file-parser' updated: v1.1 → v1.2 (generalized to any delimiter)
```

### Step 4: Memory Persists Across Sessions / 步骤4：跨会话记忆保持

```
$ claude   # Close and reopen Claude Code / 关闭并重新打开 Claude Code
> Parse an Excel file with similar error handling

Hermes [memory] Loading persistent context...
  - Recalled 2 prior interactions about file parsing
  - Active skill: file-parser v1.2

Hermes [skill: file-parser v1.2] Applying cross-session knowledge...

I remember our CSV/TSV work. For Excel, I'll follow the same
error-handling pattern but use openpyxl:

  def parse_excel(filepath, sheet_name=None):
      """Parse Excel file following established error patterns."""
      import openpyxl
      try:
          wb = openpyxl.load_workbook(filepath, read_only=True)
          sheet = wb[sheet_name] if sheet_name else wb.active
          headers = [cell.value for cell in next(sheet.iter_rows())]
          return [dict(zip(headers, [c.value for c in row]))
                  for row in sheet.iter_rows(min_row=2)]
      except FileNotFoundError:
          raise ValueError(f"File not found: {filepath}")
      except openpyxl.utils.exceptions.InvalidFileException:
          raise ValueError(f"Invalid Excel file: {filepath}")

Hermes [learning] Skill 'file-parser' updated: v1.2 → v1.3
  - Added: Excel support via openpyxl
  - Pattern: "All file parsers return list of dicts for consistency"
```

### Step 5: Skill Evolution Summary / 步骤5：技能进化总结

```
> /hermes skills show file-parser

Skill: file-parser
  Version: v1.3 (evolved through 3 tasks)
  Evolution history:
    v1.0  — Baseline CSV parser
    v1.1  — Learned: prefer DictReader
    v1.2  — Learned: generalize delimiters
    v1.3  — Learned: extend to Excel, consistent dict output

  Patterns learned:
    1. "DictReader preferred for tabular data"
    2. "Tabular parsers should share a common base"
    3. "All file parsers return list of dicts for consistency"

  Memory entries: 3 interactions, 3 patterns
```

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `claude install hermes-ccc` fails | npm not in PATH or outdated | Run `npm install -g @anthropic-ai/claude-code` first, then retry / 先运行 `npm install -g @anthropic-ai/claude-code`，然后重试 |
| `pip install hermes-agent` permission error | System Python restricted | Use `pip install --user hermes-agent` or a virtual environment / 使用 `pip install --user hermes-agent` 或虚拟环境 |
| `/hermes status` shows 0 skills | Plugin not properly loaded | Run `claude plugins list` to verify; reinstall with `claude install hermes-ccc` / 运行 `claude plugins list` 验证；用 `claude install hermes-ccc` 重装 |
| Memory not persisting | Memory database path issue | Check `~/.hermes/memory.db` exists; run `hermes init` to recreate / 检查 `~/.hermes/memory.db` 是否存在；运行 `hermes init` 重新创建 |
| Skills not evolving | Learning loop disabled | Ensure `hermes config set learning.enabled true` / 确保设置 `hermes config set learning.enabled true` |
| `hermes init` hangs on Windows | Python PATH conflict | Use full path: `py -3 -m hermes init` / 使用完整路径：`py -3 -m hermes init` |
| Slow skill execution | Large memory database | Run `hermes memory compact` to optimize / 运行 `hermes memory compact` 优化 |
| Claude Code cannot find Hermes | Node.js version too old | Upgrade to Node.js 18+: `nvm install 18 && nvm use 18` / 升级到 Node.js 18+ |

---

## Learn More / 了解更多

- GitHub: [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Documentation / 文档: [docs.hermes-agent.ai](https://docs.hermes-agent.ai)
- Skill Marketplace / 技能市场: [skills.hermes-agent.ai](https://skills.hermes-agent.ai)
