# GStack -- Garry Tan's Virtual Engineering Team

# GStack -- YC CEO 的虚拟工程团队

> **~83k stars** | By **Garry Tan** (Y Combinator CEO) | MIT License
>
> GitHub: [github.com/garrytan/gstack](https://github.com/garrytan/gstack)

---

## What is GStack? / 什么是 GStack？

GStack turns Claude Code into a **complete engineering team** with specialized roles.
Think of it as having a CTO, designer, eng manager, QA lead, security officer,
and release engineer -- all AI, all opinionated, all working for you.

GStack 把 Claude Code 变成一个**完整的工程团队**，每个角色各司其职。
就像同时拥有 CTO、设计师、工程经理、QA 负责人、安全官和发布工程师——全部由 AI 担任。

Garry Tan averaged **10,000 lines of code** and **100 pull requests per week** using this setup.
After months of personal use, he open-sourced it in March 2026.

Garry Tan 使用这套系统平均每周产出 **10,000 行代码**和 **100 个 PR**。
经过数月的个人使用后，于 2026 年 3 月开源。

---

## The Virtual Team / 虚拟团队

GStack assigns Claude Code **strong, opinionated roles**. Each role has firm beliefs
about what "good" looks like -- that's the secret sauce.

GStack 为 Claude Code 分配了**有主见的角色**。每个角色对"什么是好的"都有坚定的看法——这是秘诀所在。

| Role / 角色 | What They Do / 职责 | Key Trait / 关键特质 |
|---|---|---|
| **CEO** | Rethinks the product -- is this worth building? / 重新审视产品——值得做吗？ | Vision-driven / 愿景驱动 |
| **Eng Manager** | Locks architecture, defines constraints / 锁定架构、定义约束 | Consistency-obsessed / 一致性强迫症 |
| **Designer** | Catches "AI slop" -- generic, lifeless UI / 捕捉"AI 水货"——模板化、无生气的界面 | Taste-driven / 审美驱动 |
| **Code Reviewer** | Finds production bugs before they ship / 在上线前发现生产级 Bug | Paranoid / 偏执型审查 |
| **QA Lead** | Opens a real browser, runs test scenarios / 打开真实浏览器、运行测试场景 | Hands-on testing / 实操测试 |
| **Security Officer** | Runs OWASP + STRIDE threat audits / 执行 OWASP + STRIDE 威胁审计 | Zero-trust mindset / 零信任思维 |
| **Release Engineer** | Ships the PR, handles changelog / 发布 PR、维护变更日志 | Ship-it mentality / 发布至上 |

---

## 23+ Slash Commands / 23+ 斜杠命令

GStack provides 23 opinionated slash commands (Claude Code "skills") that map to
the roles above. Some highlights:

GStack 提供 23 个有主见的斜杠命令（Claude Code "技能"），对应上面的角色。部分命令如下：

```
/ceo-review        -- CEO perspective: should we build this?
                      CEO 视角：我们该不该做这个？

/arch-lock         -- Lock down architecture decisions
                      锁定架构决策

/design-review     -- Check UI for AI slop and generic patterns
                      检查界面是否有 AI 水货和模板化问题

/code-review       -- Deep review for production bugs
                      深度审查生产级 Bug

/qa-browser        -- Launch real browser testing
                      启动真实浏览器测试

/security-audit    -- OWASP + STRIDE threat modeling
                      OWASP + STRIDE 威胁建模

/ship-pr           -- Create and ship the pull request
                      创建并发布 PR

/standup           -- Daily standup summary
                      每日站会摘要

/retro             -- Sprint retrospective
                      迭代回顾
```

Each command embeds domain expertise. `/design-review` knows what AI slop looks like.
`/security-audit` runs through real OWASP checklists. These are not generic prompts.

每个命令都内嵌了领域专业知识。`/design-review` 知道 AI 水货长什么样。
`/security-audit` 会遍历真实的 OWASP 检查清单。这些不是泛泛的提示词。

---

## Installation / 安装

Add GStack's commands to your project's `.claude/` directory:

将 GStack 的命令添加到项目的 `.claude/` 目录：

```bash
# Clone the repo / 克隆仓库
git clone https://github.com/garrytan/gstack.git

# Copy commands into your project / 将命令复制到你的项目
cp -r gstack/commands/ your-project/.claude/commands/
```

That's it. Claude Code will automatically discover the slash commands.

就这样。Claude Code 会自动发现这些斜杠命令。

---

## Key Insight: Opinionated Roles / 核心理念：有主见的角色

The word **opinionated** is central to GStack. Each role doesn't just "help" --
it has **strong opinions** about what good looks like:

**有主见**是 GStack 的核心理念。每个角色不只是"帮忙"——它对什么是好的有**强烈的看法**：

- The **Designer** will reject bland, template-driven UI and push for personality.
  **设计师**会拒绝乏味的模板化 UI，并要求注入个性。

- The **Security Officer** assumes everything is compromised until proven otherwise.
  **安全官**假设一切都已被攻破，除非证明安全。

- The **Code Reviewer** looks for the bug that will wake you up at 3 AM.
  **代码审查员**寻找那些会在凌晨 3 点把你叫醒的 Bug。

- The **Eng Manager** won't let you introduce a new pattern that conflicts with existing ones.
  **工程经理**不会让你引入与现有模式冲突的新模式。

This opinionated approach is what makes GStack effective. Generic advice is cheap;
strong, specific feedback is valuable.

这种有主见的方法正是 GStack 有效的原因。泛泛的建议廉价；强烈、具体的反馈才有价值。

---

## GStack vs Superpowers / GStack 与 Superpowers 对比

Both are popular Claude Code frameworks, but they take different approaches:

两者都是流行的 Claude Code 框架，但采用不同的策略：

| Aspect / 方面 | GStack | Superpowers |
|---|---|---|
| **Mental model / 思维模型** | Role-based team / 基于角色的团队 | Phase-based workflow / 基于阶段的流程 |
| **Core idea / 核心理念** | Each command = a team member / 每个命令=一个团队成员 | Each phase = a development stage / 每个阶段=一个开发环节 |
| **Strength / 优势** | Deep domain expertise per role / 每个角色深度领域专长 | Structured progression / 结构化推进 |
| **Best for / 适合** | Solo devs who want a team / 想要团队的独立开发者 | Teams wanting process / 想要流程的团队 |
| **Philosophy / 哲学** | Opinionated specialists / 有主见的专家 | Guided steps / 引导式步骤 |

They are complementary. Some developers use both.

两者是互补的。有些开发者同时使用。

---

## Learn More / 了解更多

- **GitHub**: [github.com/garrytan/gstack](https://github.com/garrytan/gstack)
- **Author**: Garry Tan -- CEO of Y Combinator
- **License**: MIT
- **Stars**: ~83,000

---

*GStack shows that the best AI coding isn't about one mega-prompt --
it's about assembling a team of specialists, each with strong opinions.*

*GStack 证明了最好的 AI 编程不是靠一个超级提示词——而是组建一支专家团队，每位专家都有强烈的主见。*
