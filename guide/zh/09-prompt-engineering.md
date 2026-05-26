# Claude Prompt 工程

> 通过有效地结构化 Prompt，从 Claude 获得显著更好的结果。从基础技巧到高级模式。

## 目录

- [核心原则](#核心原则)
- [Prompt 结构](#prompt-结构)
- [Claude 专属技巧](#claude-专属技巧)
- [代码场景的 Prompt](#代码场景的-prompt)
- [系统提示](#系统提示)
- [高级模式](#高级模式)
- [常见错误](#常见错误)

---

## 核心原则

### 1. 具体

第一原则。模糊的 Prompt 得到模糊的结果。

```
# 差
"改善这段代码"

# 好
"重构 UserService.createUser() 方法：
 1. 在数据库插入前验证邮箱格式
 2. 用 bcrypt 12 轮哈希密码
 3. 返回 UserDTO 而不是原始数据库模型"
```

### 2. 提供上下文

Claude 不知道你知道的。分享相关背景：

```
# 差
"修复认证 bug"

# 好
"用户在 JWT 过期后即使刷新令牌仍有效也收到 401 错误。
认证中间件在 src/middleware/auth.ts，
令牌刷新逻辑在 src/services/auth.ts。
刷新端点直接测试正常 — 问题似乎在中间件处理过期访问令牌的方式。"
```

### 3. 展示而不只是描述

示例比描述更有价值：

```
# 差
"把输出格式化得好看一些"

# 好
"每个条目格式如下：
[2024-01-15] ERROR  auth/login — 用户 user@example.com 凭证无效
[2024-01-15] WARN   api/rate  — IP 192.168.1.1 接近速率限制

日期左对齐，级别固定宽度（5字符），来源右填充。"
```

### 4. 约束输出

告诉 Claude 你要什么**和**不要什么：

```
"生成一个解析 CSV 文件的 Python 函数。

要求：
- 只用标准库的 csv 模块
- 处理 UTF-8 BOM
- 返回以列头为键的字典列表

约束：
- 不用 pandas 或外部依赖
- 不超过 30 行
- 包含文档字符串"
```

---

## Prompt 结构

### 有效 Prompt 模板

```
[角色 — Claude 应该扮演谁？]
[上下文 — 背景是什么？]
[任务 — 具体做什么？]
[格式 — 输出应该是什么样？]
[约束 — 避免什么？]
[示例 — 展示期望结果]
```

不是每个 Prompt 都需要所有部分，使用相关的即可。

---

## Claude 专属技巧

### 1. 用 XML 标签结构化

Claude 对 XML 标签的理解特别好：

```
<context>
这是一个使用 TypeScript 和 Zustand 的 React 18 应用。
</context>

<task>
重构 ShoppingCart 组件：
1. 拆分为 CartItem、CartSummary、CartActions 子组件
2. 将业务逻辑移到 useCart 自定义 hook
3. 为所有 props 添加 TypeScript 类型
</task>

<constraints>
- 暂时保持所有组件在同一个文件
- 不要改变 Zustand store 接口
</constraints>
```

### 2. 逐步思考

对复杂推理，明确要求 Claude 分步思考：

```
"逐步思考请求如何通过我们的中间件栈：
1. 请求到达 nginx 代理时发生什么？
2. 如何到达 Express 应用？
3. 哪些中间件按什么顺序运行？
4. 超时可能发生在哪里？

然后给出最可能的原因和修复方案。"
```

### 3. 预填充响应

引导 Claude 的输出格式（API）：

```python
messages = [
    {"role": "user", "content": "用 JSON 列出 5 种颜色"},
    {"role": "assistant", "content": "["}  # 强制输出 JSON 数组
]
```

### 4. 扩展思考

复杂问题启用扩展思考：

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=8000,
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[{"role": "user", "content": "设计数据库 schema..."}]
)
```

### 5. 多轮迭代

不要试图一个 Prompt 搞定一切，迭代推进：

```
第 1 轮："实现一个基本的 WebSocket 聊天服务器"
第 2 轮："添加认证 — 连接时必须发送 JWT"
第 3 轮："添加房间 — 用户可以加入/离开，消息只发给房间成员"
第 4 轮："添加输入指示器和已读回执"
```

---

## 代码场景的 Prompt

### 代码生成

```
"写一个 Python 函数 `parse_duration(s: str) -> int`，
将人类可读的时间字符串转换为秒。

示例：
- '5m' → 300
- '2h30m' → 9000
- '1d12h' → 129600

处理 d, h, m, s, ms 单位。无效输入抛出 ValueError。"
```

### 代码审查

```
"审查这个 PR diff：
1. Bug — 逻辑错误、边界条件、空值处理
2. 安全 — 注入、认证绕过、数据泄露
3. 性能 — N+1 查询、不必要的分配

对每个发现，解释问题并展示修复。跳过风格注释。"
```

### 调试

```
"这段代码在 src/api/orders.ts 第 42 行抛出
'TypeError: Cannot read property 'id' of undefined'。

输入数据：
{
  "items": [{"productId": "abc", "qty": 2}],
  "customer": null  // 访客结账时有时为 null
}

找出 bug 并修复，优雅地处理 null customer 的情况。"
```

---

## 系统提示

### 代码审查者

```
你是执行代码审查的高级工程师。关注：
- 正确性和边缘情况
- 安全漏洞
- 性能瓶颈

直接具体。对每个问题展示修复方案。
不要评论风格，除非影响可读性。
```

### 技术文档写手

```
你是技术文档写手，产出清晰、开发者友好的内容。
- 使用主动语态："配置服务器" 而非 "服务器可以被配置"
- 指令以动词开头："运行"、"创建"、"添加"
- 每个概念都包含代码示例
```

---

## 高级模式

### Few-Shot 提示

```
"将 API 错误消息转换为用户友好的消息。

示例：
输入："UNIQUE_VIOLATION: duplicate key value violates unique constraint"
输出："该邮箱已有账户。试试登录？"

现在转换：
输入："CHECK_VIOLATION: new row violates check constraint on column 'age'"
```

### 对抗性测试

```
"扮演恶意用户试图突破输入验证。
对表单的每个字段（邮箱、姓名、年龄、简介）：
1. 列出 5 个可能绕过验证的边界输入
2. 解释成功后可能造成什么后果
3. 建议修复方案

要有创意 — SQL 注入、XSS、Unicode 技巧等。"
```

---

## 常见错误

### 1. 指令过多

```
# 差 — 太多指令让 Claude 困惑
"写函数。确保干净。用好名字。加注释。处理错误。
让它快。写测试。用 TypeScript。遵循 SOLID..."

# 好 — 聚焦清晰
"写一个 TypeScript 函数验证邮箱地址。
用正则匹配常见格式。返回 { valid: boolean, reason?: string }。"
```

### 2. 太抽象

```
# 差
"实现代码库的最佳实践"

# 好
"用 Zod schema 为 src/api/ 中所有 API 端点添加输入验证"
```

### 3. 不提供示例

对于重要的输出格式，展示一个示例。不要假设 Claude 会匹配你脑中的模型。

---

## 模板

即用 Prompt 模板：

- [代码审查 Prompt](../../templates/system-prompts/code-reviewer.md)
- [技术文档 Prompt](../../templates/system-prompts/technical-writer.md)
- [数据分析 Prompt](../../templates/system-prompts/data-analyst.md)

---

<p align="center">
  <strong>下一篇：</strong> <a href="10-advanced-workflows.md">高级工作流</a> — 复杂的实际自动化模式
</p>

---

[← 上一章：Agent SDK](08-agent-sdk.md) | [目录](../../README_zh.md) | [下一章：高级工作流 →](10-advanced-workflows.md)
