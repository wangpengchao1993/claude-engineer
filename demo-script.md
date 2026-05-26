# AI 编程新范式：Claude Code 从入门到落地

> 一份完整的演讲讲义，适合 30-45 分钟线下/线上分享。
> 面向混合受众：AI 编码新手、有经验的开发者、技术管理者。

---

## 开场（3 分钟）

### 一个问题

> "在座有多少人每天在用 AI 写代码？"

不管你举没举手，接下来的 30 分钟会改变你对 AI 编程的认知——

**我们不缺工具，缺的是使用工具的思维方式。**

今天分享三件事：

1. **认知** — AI 编程到底该怎么想
2. **工具** — Claude Code 到底怎么用
3. **落地** — 团队和项目到底怎么接入

---

## 第一部分：认知升级（8 分钟）

### 1.1 AI 编程的"自动驾驶"类比

我们做自动驾驶的人都知道 SAE L0→L5 的分级。AI 编程其实一模一样：

| 等级 | 自动驾驶 | AI 编程 | 你在做什么 |
|------|---------|---------|-----------|
| L0 | 纯人工驾驶 | 不用 AI | 全靠自己 |
| L1 | 车道保持 | 代码补全（Copilot tab-tab） | AI 帮你打字 |
| L2 | 自适应巡航 | Chat 问答 + 片段生成 | 你问 AI 答 |
| L3 | 有条件自动驾驶 | **Agent 模式** — 读写文件、运行命令 | AI 干活，你审查 |
| L4 | 高度自动驾驶 | CI/CD + 多 Agent 编排 | AI 自主完成任务链 |
| L5 | 完全自动驾驶 | ？ | 还没到 |

**大多数人卡在 L1-L2。今天讲的是怎么安全地用好 L3-L4。**

关键洞察：自动驾驶从来不是"信不信任系统"的问题，而是**在什么场景下、给多大权限、怎么监控**的问题。AI 编程也是一样。

### 1.2 AI 擅长什么、不擅长什么

别把 AI 当全能选手。它有明确的能力边界：

| AI 很强 | AI 一般 | AI 很弱 |
|---------|---------|---------|
| 局部代码生成（CRUD、工具函数） | 跨模块重构 | 产品决策、需求判断 |
| 模式匹配（套路化任务） | 性能优化 | 理解"为什么不做" |
| 解释/文档/翻译 | 复杂并发/分布式 | 项目间的权衡取舍 |
| 测试生成 | 安全审计 | 感知组织政治/历史包袱 |
| Bug 定位 + 修复 | 架构设计 | 知道什么代码"不该动" |

**一句话总结：AI 是顶级的执行者，但不是合格的决策者。**

你的角色不是被 AI 替代，而是从"写代码的人"变成"指挥 AI 写代码的人"——决策权始终在你手里。

### 1.3 Context Engineering — 2025 最重要的概念

你有没有这样的体验：
- 同样的问题，换一种问法结果完全不同
- AI 第一轮回答很棒，后面越来越差
- 别人用同一个工具效率是你的 3 倍

**差距不在 prompt 技巧，而在上下文设计。**

Context Engineering（上下文工程）= 系统性地设计 AI 看到的所有信息：

```
上下文 = CLAUDE.md + 代码 + git history + 你的提问 + memory
         ─────────   ────   ──────────   ────────   ──────
         你提前准备的  AI读的  AI参考的     你当下说的  跨对话记忆
```

这就像给新员工入职：你不会让他第一天就写核心代码。你会给他：
- 项目文档（CLAUDE.md）
- 代码权限（工具访问）
- 一个有经验的同事指导（你的 prompt）

**CLAUDE.md 不是配置文件，它是你给 AI 的"入职手册"。**

---

## 第二部分：工具 — Claude Code 实战（12 分钟）

### 2.1 为什么是 Claude Code？

> 这里简要提一下，详细对比可以看我们的 [工具对比文档](comparison.md)。

| 维度 | Claude Code 的长处 |
|------|-------------------|
| **上下文** | 200K 默认，Bedrock/Vertex 可达 1M — 能塞下整个大型项目 |
| **多平台** | CLI + 桌面应用 + Web + VS Code / JetBrains 插件 |
| **Agent** | 原生 Agent 能力，读写文件、运行命令、启动子 Agent |
| **可编程** | CLI 优先，`claude -p` 可嵌入任何脚本/流水线 |
| **可扩展** | Hooks（29 种事件）+ MCP（工具协议）+ Custom Commands |
| **可控** | CLAUDE.md 多层级配置，权限精细管控 |
| **可审计** | CLI 源码公开，可私有部署（Bedrock/Vertex） |

一句话：**Claude Code 是面向工程师的 AI 编程工具，不是面向演示的。**

### 2.2 Live Demo：从零到 CRUD API

> （切到终端，现场演示）

**第一步：/init — 建立上下文**

```bash
claude
> /init
```

"看，它扫描了项目结构，生成了一份 CLAUDE.md。这就是我刚才说的上下文工程——你的第一步不是写代码，而是让 AI 了解你的项目。"

**第二步：自然语言 → 代码**

```
帮我添加一个 /api/todos 的 CRUD 接口：
- GET /api/todos — 列出所有待办
- POST /api/todos — 创建待办（title 字段必填）
- PUT /api/todos/:id — 更新待办
- DELETE /api/todos/:id — 删除待办
先用内存数组存储。
```

"注意看——它自动读了现有代码，理解了项目结构，然后生成符合项目风格的代码。每一步都有 diff 可以审查。"

**第三步：验证**

```
启动服务器，用 curl 测试这四个接口
```

"AI 写完自己测。如果有 bug，它会自动修。这就是 L3 — Agent 模式。"

**第四步：Plan 模式 — 复杂任务先想再做**

（按 `Shift+Tab`）

```
给 todos 加上 SQLite 持久化，需要数据迁移
```

"Plan 模式下它只输出方案不执行。你审查通过了再做。这就是'信任但验证'。"

**第五步：一键提交**

```
提交这些改动
```

"看下 `/cost` — 整个 demo 花了不到一块钱。"

### 2.3 进阶玩法速览

#### 管道模式 — 嵌入你的工作流

```bash
# 代码审查
git diff HEAD~1 | claude -p "review，关注安全问题"

# 解释报错
cat error.log | claude -p "什么原因，怎么修"

# 批量生成
cat src/models/*.py | claude -p "为每个 model 写单元测试" > tests.py
```

#### Hooks — 自动化质量守护

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": ["npm run lint --fix $CLAUDE_FILE_PATH"]
    }]
  }
}
```

"每次 AI 编辑文件后自动 lint。AI 写的代码也得过你的质量关。"

#### MCP — 无限扩展

```bash
# 让 Claude 能查数据库
claude mcp add postgres npx @anthropic-ai/mcp-postgres

# 让 Claude 能操作 GitHub
claude mcp add github npx @anthropic-ai/mcp-github
```

"MCP 是 Model Context Protocol——给 AI 装插件。数据库、搜索引擎、内部系统，都可以接进来。"

---

## 第三部分：落地 — 团队和项目怎么接入（7 分钟）

### 3.1 CLAUDE.md 的正确写法

CLAUDE.md 不只是"告诉 AI 用什么技术栈"。好的 CLAUDE.md 要包含**你脑子里那些没写在文档里的知识**：

```markdown
## 注意事项
- 不要碰 src/legacy/ 下的代码，那是旧系统，下个月迁移
- 所有数据库操作必须走 Repository 层，不要直接写 SQL
- commit message 用 conventional commits 格式
- 测试覆盖率不能低于 80%，PR 合并前 CI 必须全绿
```

这些才是 AI 真正需要的信息 — **不是"这个项目用 React"（它看 package.json 就知道），而是"什么不能做"和"为什么要这样做"。**

上下文预算建议：

| 上下文窗口 | CLAUDE.md 长度 | 策略 |
|-----------|---------------|------|
| 200K tokens | 500-1000 行 | 核心规范 + 关键约束 |
| 1M tokens | 1000-3000 行 | 可以加架构细节、示例代码 |

### 3.2 团队落地三步走

**第一步：标准化配置（第 1 周）**

- 为项目创建 CLAUDE.md，提交到 git（团队共享）
- 统一 `.claude/settings.json` 的 Hooks 和权限
- 选定模型策略：日常 Sonnet、复杂任务 Opus、批处理 Haiku

**第二步：嵌入工作流（第 2-4 周）**

- PR 流程加入 AI Review（Claude Code Action）
- 新功能开发先用 Plan 模式出方案
- 代码审查：人 + AI 双重 review

**第三步：度量和优化（持续）**

- 跟踪 `/cost` — 关注 token 消耗趋势
- 收集团队反馈 — 什么任务 AI 做得好、什么做得差
- 迭代 CLAUDE.md — 把踩过的坑写进去

### 3.3 AI 代码的质量意识

三个容易被忽视的陷阱：

**陷阱一：过度工程**

AI 特别喜欢"做多"——加抽象层、加 error handling、加注释。三行能解决的事，AI 给你写出一个带 Factory Pattern 的 30 行方案。

应对：在 CLAUDE.md 里明确写 "Keep it simple. Don't add abstractions unless there are 3+ use cases."

**陷阱二：风格不一致**

AI 生成的代码可能每次风格不同。单独看没问题，合在一起就不像一个人写的。

应对：CLAUDE.md 里写清楚代码规范 + PostToolUse Hook 自动格式化。

**陷阱三：AI 债务**

像技术债一样——盲目接受 AI 代码，不审查不理解，会积累你不理解的代码。有一天出了问题，谁都修不了。

应对：**理解你接受的每一行代码。** 用 AI 生成但不理解，比不用 AI 更危险。

---

## 第四部分：学习路径（2 分钟）

> 详细路线：[roadmap.md](roadmap.md)

```
🟢 第 1 周：入门                    → 装好工具，写好 CLAUDE.md
🔵 第 2-3 周：日常使用              → 交互模式、Plan 模式、管道
🟡 第 1-2 月：进阶                  → Hooks、MCP、Prompt 工程
🔴 第 3 月+：团队落地               → CI/CD、多 Agent、工作流框架
```

资源全在这个 repo 里：
- **17 章教程**（中英双语）
- **6 套项目模板**（Python / TypeScript / Rust / C++ / Java / 全栈）
- **10 个工作流框架对比**
- **可运行的代码示例**

---

## 收尾（2 分钟）

### 三个带走的观点

1. **AI 编程不是"让 AI 写代码"，是"设计 AI 的上下文让它写出好代码"** — Context Engineering
2. **信任但验证** — 和自动驾驶一个道理，不是信不信的问题，是怎么监控的问题
3. **AI 放大你的能力，不替代你的判断** — 决策权始终在你

### 一个挑战

> 回去之后，花 10 分钟给你的项目写一个 CLAUDE.md。然后用 Claude Code 做一个你一直拖着没做的小任务。你会惊讶于效果。

---

## 附录：Q&A 常见问题预案

| 问题 | 回答要点 |
|------|---------|
| "和 Cursor/Copilot 比怎么样？" | 见 [comparison.md](comparison.md)，核心差异是 CLI 优先 + Agent 深度 + 可编程 |
| "安全吗？代码会泄露吗？" | API 模式代码不用于训练；可用 Bedrock/Vertex 私有部署；Hooks 可以拦截敏感操作 |
| "多少钱？" | Pro $20/月 含量够个人用；API 按量付费，日常开发每天几块钱 |
| "AI 写的代码出了 bug 谁负责？" | 和用 Stack Overflow 复制代码一样——你接受了就是你的责任。所以要理解每一行 |
| "适合什么规模的项目？" | 小到脚本大到百万行。默认 200K 上下文，Bedrock/Vertex 可达 1M，配合好 CLAUDE.md 大项目也能用 |
| "我的语言/框架支持吗？" | Claude 支持所有主流语言。CLAUDE.md 告诉它你的具体技术栈就行 |
| "英文 prompt 效果是不是比中文好？" | 差距很小，中文完全可以。技术术语可以混用英文（变量名、命令等本来就是英文） |

---

<p align="center">
  <sub>来自 <a href="README.md">claude-engineer</a> — 觉得有用请给个 Star！</sub>
</p>
