# AI 生成代码的安全与合规

> 了解安全模型、保护密钥、防止 AI 生成代码中的常见漏洞、管理依赖安全性以及满足合规要求。

## 目录

- [安全模型](#安全模型)
- [密钥管理](#密钥管理)
- [AI 代码的 OWASP Top 10](#ai-代码的-owasp-top-10)
- [依赖安全](#依赖安全)
- [合规工作流](#合规工作流)
- [安全 Hooks 配置](#安全-hooks-配置)

---

## 安全模型

### 哪些数据会发送到 Anthropic API？

使用 Claude Code 时，代码上下文会被发送到 Anthropic API 进行处理。

```
会发送的内容：
- Claude 读取的文件内容（仅限你要求它读取或它需要的文件）
- 你的提示和指令
- Claude 运行的命令的终端输出
- CLAUDE.md 文件的内容

不会发送的内容：
- Claude 在会话中未访问的文件
- 你的整个文件系统
- 环境变量（除非你把它们粘贴到提示中）
- Git 凭证或 SSH 密钥
```

### API 数据留存

```
Anthropic API 数据处理：
- API 输入/输出不会用于训练模型
- 数据留存取决于你的计划：
  - 标准 API：30 天留存用于信任和安全
  - 企业版：可选零留存
- 查看 https://anthropic.com/policies 了解当前政策
```

### 企业安全选项

```bash
# 对于企业部署，配置零留存
# 这在 API 密钥 / 组织级别设置

# 检查你的 API 密钥的组织设置
claude "/config" # 检查当前配置

# 企业团队应该：
# 1. 使用组织管理的 API 密钥
# 2. 在组织级别启用零留存
# 3. 使用 SSO 进行团队成员认证
# 4. 设置 API 使用的审计日志
```

### 本地操作

一些操作永远不会离开你的机器：

```
始终在本地：
- 文件读写（Claude 在本地读取，将上下文发送到 API）
- Git 操作
- Shell 命令执行
- Hook 执行
- CLAUDE.md 解析

流程：
1. Claude 在本地读取文件
2. 将相关上下文发送到 API
3. 从 API 接收响应
4. 在本地执行操作（文件写入、命令）
```

---

## 密钥管理

### 规则：永远不要在提示或 CLAUDE.md 中放置密钥

```markdown
# 错误 - CLAUDE.md 中包含密钥
## 数据库
连接字符串：postgres://admin:s3cret_p4ss@db.example.com:5432/prod

## API 密钥
Stripe：sk_live_abc123...
SendGrid：SG.xyz789...
```

```markdown
# 正确 - CLAUDE.md 中使用引用
## 数据库
连接字符串在 DATABASE_URL 环境变量中。格式参见 .env.example。

## API 密钥
所有 API 密钥在 .env 中（已 gitignore）。所需变量参见 .env.example。
```

### 环境变量策略

```bash
# .env.example（提交到仓库 - 显示所需变量但不含值）
DATABASE_URL=postgres://user:password@localhost:5432/dbname
STRIPE_SECRET_KEY=sk_test_...
REDIS_URL=redis://localhost:6379
JWT_SECRET=generate-a-random-string-here

# .env（gitignore 排除 - 实际值）
DATABASE_URL=postgres://admin:real_password@localhost:5432/myapp
STRIPE_SECRET_KEY=sk_test_actual_key_here
REDIS_URL=redis://localhost:6379
JWT_SECRET=a8f2e1b5c3d4...
```

```bash
# .gitignore 必须包含：
.env
.env.local
.env.production
*.pem
*.key
credentials.json
service-account.json
```

### 生产环境的 Vault 方案

```typescript
// src/config/secrets.ts - 在生产环境从 vault 加载密钥
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

interface AppSecrets {
  databaseUrl: string;
  stripeKey: string;
  jwtSecret: string;
}

async function loadSecrets(): Promise<AppSecrets> {
  if (process.env.NODE_ENV === 'development') {
    // 开发环境使用 .env 文件
    return {
      databaseUrl: process.env.DATABASE_URL!,
      stripeKey: process.env.STRIPE_SECRET_KEY!,
      jwtSecret: process.env.JWT_SECRET!,
    };
  }

  // 生产环境使用 AWS Secrets Manager
  const client = new SecretsManager({ region: 'us-east-1' });
  const response = await client.getSecretValue({
    SecretId: 'myapp/production',
  });

  return JSON.parse(response.SecretString!);
}

export const secrets = await loadSecrets();
```

### 阻止密钥提交的 Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit 或通过 .claude/settings.json hooks 配置

# 表示密钥的模式
PATTERNS=(
  'AKIA[0-9A-Z]{16}'                    # AWS Access Key ID
  'sk_live_[a-zA-Z0-9]+'                # Stripe 生产密钥
  'sk-[a-zA-Z0-9]{48}'                  # OpenAI API 密钥
  'ghp_[a-zA-Z0-9]{36}'                 # GitHub 个人访问令牌
  'xoxb-[0-9]+-[a-zA-Z0-9]+'           # Slack bot 令牌
  'password\s*=\s*["\x27][^"\x27]+'     # 硬编码密码
  'secret\s*=\s*["\x27][^"\x27]+'       # 硬编码密钥
  'jdbc:.*password=[^&\s]+'             # 含密码的 JDBC 连接字符串
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR)

for file in $STAGED_FILES; do
  for pattern in "${PATTERNS[@]}"; do
    if git show ":$file" 2>/dev/null | grep -qE "$pattern"; then
      echo "错误：在 $file 中检测到潜在密钥"
      echo "匹配模式：$pattern"
      echo "请移除密钥并使用环境变量替代。"
      exit 1
    fi
  done
done

exit 0
```

配置为 Claude Code hook：

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

## AI 代码的 OWASP Top 10

AI 生成的代码经常引入特定的漏洞模式。以下是最常见的类型及防范方法。

### 1. SQL 注入

```typescript
// 错误：AI 经常为查询生成字符串拼接
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const result = await db.query(`SELECT * FROM users WHERE name = '${name}'`);
  res.json(result.rows);
});

// 正确：参数化查询
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const result = await db.query('SELECT * FROM users WHERE name = $1', [name]);
  res.json(result.rows);
});

// 最佳：使用 ORM 自动处理参数化
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const users = await db.select().from(usersTable).where(eq(usersTable.name, name));
  res.json(users);
});
```

### 2. 跨站脚本攻击（XSS）

```typescript
// 错误：AI 可能使用 dangerouslySetInnerHTML 或跳过清理
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// 正确：使用文本内容（React 自动转义）
function Comment({ text }: { text: string }) {
  return <div>{text}</div>;
}

// 当需要 HTML 时，显式清理
import DOMPurify from 'dompurify';

function RichComment({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

### 3. 不安全的认证

```typescript
// 错误：AI 有时生成弱认证模式
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await db.findUser(username);
  if (user.password === password) {  // 明文比较！
    const token = jwt.sign({ id: user.id }, 'hardcoded-secret');  // 硬编码！
    res.json({ token });
  }
});

// 正确：适当的认证实现
import bcrypt from 'bcrypt';

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await db.findUser(username);

  if (!user) {
    // 用户不存在和密码错误返回相同响应（防止用户枚举）
    return res.status(401).json({ error: '凭证无效' });
  }

  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) {
    return res.status(401).json({ error: '凭证无效' });
  }

  const token = jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '1h', algorithm: 'HS256' }
  );

  res.json({ token });
});
```

### 4. 路径遍历

```typescript
// 错误：AI 可能不验证文件路径
app.get('/files/:name', (req, res) => {
  const filePath = path.join('/uploads', req.params.name);
  res.sendFile(filePath);  // ../../../etc/passwd 可以得逞！
});

// 正确：验证解析后的路径在允许的目录内
app.get('/files/:name', (req, res) => {
  const uploadsDir = path.resolve('/uploads');
  const filePath = path.resolve(uploadsDir, req.params.name);

  if (!filePath.startsWith(uploadsDir)) {
    return res.status(403).json({ error: '访问被拒绝' });
  }

  res.sendFile(filePath);
});
```

### CLAUDE.md 安全审查提示

将此添加到 CLAUDE.md 以使 Claude Code 具有安全意识：

```markdown
## 安全要求

生成代码时始终：
- 所有数据库操作使用参数化查询
- 在 HTML 中渲染前清理用户输入
- 使用 bcrypt 或 argon2 进行密码哈希（密码永远不用 MD5/SHA）
- 从环境变量加载密钥，永不硬编码
- 验证文件路径以防止路径遍历
- 设置适当的 CORS 头（生产环境不用通配符）
- 使用仅 HTTPS 的 cookie 并设置 SameSite 属性
- 在认证端点实现限流
- 在 API 边界验证和清理所有用户输入
- 使用 Content-Security-Policy 头
```

---

## 依赖安全

### AI 可能建议有漏洞的包

```bash
# AI 安装或建议依赖后，始终进行审计

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

### 依赖变更后自动审计

```jsonc
// .claude/settings.json - 任何依赖变更后运行审计
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
            "command": "pip-audit 2>/dev/null || echo 'pip-audit 未安装，运行：pip install pip-audit'"
          }
        ]
      }
    ]
  }
}
```

### Lockfile 验证

```bash
# 确保 lockfile 已提交且一致
# 添加到 CI 流水线

# Node.js - 验证 lockfile 完整性
npm ci  # 如果 lockfile 与 package.json 不同步则失败

# Python - 验证固定版本
pip install --require-hashes -r requirements.txt

# 始终审查 AI 生成 PR 中的依赖变更
git diff package-lock.json | head -50  # 检查变更内容
```

### CLAUDE.md 依赖策略

```markdown
## 依赖管理

- 不要在未讨论前添加新依赖
- 优先选择维护良好的包（>1000 GitHub star，有近期提交）
- 不使用有已知严重漏洞的包
- 添加依赖后始终运行 `npm audit`
- 在 package.json 中固定精确版本（不使用 ^ 或 ~ 前缀）
- 审查传递依赖的已知问题
```

---

## 合规工作流

### 审计日志

为合规性跟踪 AI 辅助开发：

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

// 使用示例：在 git hook 中
// 每次 AI 辅助提交后，记录操作
logAIActivity({
  timestamp: new Date().toISOString(),
  developer: process.env.USER || 'unknown',
  sessionId: process.env.CLAUDE_SESSION_ID || 'unknown',
  action: 'code_committed',
  summary: 'AI 辅助实现限流中间件',
  filesModified: ['src/middleware/rate-limiter.ts', 'tests/rate-limiter.test.ts'],
});
```

### SOC 2 考量

```markdown
## AI 开发的 SOC 2 检查清单

### 访问控制
- [ ] API 密钥通过组织管理，而非个人账户
- [ ] API 密钥轮换计划已到位（每 90 天）
- [ ] 开发者对 AI 工具的访问已记录
- [ ] 离职时撤销 AI 工具访问权限

### 变更管理
- [ ] AI 生成的代码经过与人工代码相同的审查流程
- [ ] AI 辅助的变更在提交信息中标记
- [ ] 存在 AI 被要求做什么的审计轨迹
- [ ] 没有 AI 生成的代码绕过代码审查

### 数据保护
- [ ] 生产数据永不用于 AI 提示
- [ ] 客户 PII 永不包含在代码上下文中
- [ ] 敏感项目启用零留存 API 选项
- [ ] 数据流图包含 AI API 交互

### 监控
- [ ] API 使用量被监控以发现异常
- [ ] AI 生成的代码包含在安全扫描中
- [ ] 依赖审计覆盖 AI 建议的包
```

### GDPR：AI 上下文中的个人数据

```bash
# 永远不要在提示中包含个人数据

# 错误
claude "修复用户 john.doe@example.com 的 bug，他的订单 #12345
  金额 $499.99 发货到 123 Main St 但不在仪表板中显示"

# 正确
claude "修复用户订单不在仪表板中显示的 bug。
  订单状态为 'shipped' 但仪表板查询过滤掉了它。
  重现方法：npm run seed && npm test -- --grep 'order display'"
```

```markdown
# 为受 GDPR 约束的项目添加到 CLAUDE.md

## 数据隐私规则
- 永不在提示或代码注释中包含真实客户数据
- 所有示例和测试使用合成数据
- 种子脚本必须生成假数据（使用 @faker-js/faker）
- 日志文件必须从 AI 上下文中排除（.claude/settings.json）
- 数据库转储永不加载到 AI 会话中
```

### 标记 AI 辅助的提交

```bash
# 约定：标记有 AI 辅助的提交
git commit -m "feat(auth): 添加 OAuth2 PKCE 流程

实现了公共客户端的 OAuth2 PKCE 流程。

AI-assisted: yes
AI-tool: claude-code
AI-scope: 实现和测试"
```

```bash
# 提示添加 AI 辅助标记的 Git hook
# .git/hooks/prepare-commit-msg

#!/bin/bash
COMMIT_MSG_FILE=$1

# 检查是否已有 AI 辅助标记
if ! grep -q "AI-assisted:" "$COMMIT_MSG_FILE"; then
  echo "" >> "$COMMIT_MSG_FILE"
  echo "AI-assisted: yes/no" >> "$COMMIT_MSG_FILE"
  echo "AI-tool: claude-code" >> "$COMMIT_MSG_FILE"
fi
```

---

## 安全 Hooks 配置

### 全面的安全 Hook 设置

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
            "command": "bash -c 'echo \"$CLAUDE_FILE_PATH\" | xargs -I{} grep -lE \"(password|secret|key)\\s*=\\s*[\\x27\\\"][^\\x27\\\"]+\" {} && echo \"警告：{} 中可能有硬编码密钥\" || true'"
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

### 命令验证脚本

```python
#!/usr/bin/env python3
# scripts/validate-command.py
"""在 Claude Code 执行命令前验证命令。"""

import json
import sys

BLOCKED_PATTERNS = [
    'curl.*|.*sh',          # 将远程脚本管道到 shell
    'wget.*|.*sh',          # wget 同理
    'eval ',                # 任意代码执行
    'rm -rf /',             # 破坏性命令
    'chmod 777',            # 过于宽松的权限
    '> /etc/',              # 写入系统文件
    'nc -l',               # 网络监听
    'ssh-keygen',          # 密钥生成应手动进行
]

def validate_command(tool_input: str) -> bool:
    import re
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, tool_input):
            print(f"已阻止：命令匹配危险模式：{pattern}")
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

### 安全扫描集成

```bash
#!/bin/bash
# scripts/security-scan.sh
# 在 AI 生成代码后、提交前运行

set -e

echo "=== 运行安全扫描 ==="

# 安全问题静态分析
if command -v semgrep &> /dev/null; then
  echo "运行 Semgrep..."
  semgrep --config auto --error --quiet .
fi

# 依赖审计
if [ -f "package-lock.json" ]; then
  echo "运行 npm audit..."
  npm audit --audit-level=high
fi

if [ -f "requirements.txt" ]; then
  echo "运行 pip-audit..."
  pip-audit -r requirements.txt 2>/dev/null || echo "pip-audit 不可用"
fi

# 检查暂存文件中的密钥
echo "检查密钥..."
if command -v gitleaks &> /dev/null; then
  gitleaks detect --staged --no-banner
else
  # 后备方案：基本模式匹配
  git diff --cached --name-only | xargs grep -lE \
    'AKIA|sk_live|ghp_|xoxb-|password\s*=' 2>/dev/null && {
    echo "错误：暂存文件中发现潜在密钥"
    exit 1
  } || true
fi

echo "=== 安全扫描通过 ==="
```

---

## 总结

AI 生成代码的安全需要纵深防御：

1. **了解数据流向**：知道什么发送到 API、什么留在本地
2. **永不暴露密钥**：使用环境变量、vault 和 pre-commit hook
3. **关注 OWASP 模式**：AI 经常生成注入、XSS 和弱认证代码
4. **审计依赖**：AI 可能建议过时或有漏洞的包
5. **保持合规**：记录 AI 使用、标记提交、保护个人数据
6. **自动化安全检查**：Hook 在问题到达生产环境前捕获它们

---

[← 上一章：团队协作](15-team-workflows.md) | [目录](../../README_zh.md) | [下一章：大项目管理 →](17-large-codebase.md)
