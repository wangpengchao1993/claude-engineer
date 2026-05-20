# Security Checklist for AI-Generated Code

# AI 生成代码安全检查清单

---

This checklist covers critical security concerns when using AI (such as Claude) to generate, review, or modify code. AI-generated code can introduce subtle vulnerabilities that automated tools may miss.

本检查清单涵盖使用 AI（如 Claude）生成、审查或修改代码时的关键安全问题。AI 生成的代码可能引入自动化工具难以发现的细微漏洞。

---

## 1. Secrets Management / 密钥管理

- [ ] **Never include secrets in prompts** — API keys, passwords, and tokens must not appear in prompts sent to AI services.
  **绝不在提示中包含密钥** — API 密钥、密码和令牌不得出现在发送给 AI 服务的提示中。

- [ ] **Use environment variables** — All secrets must be loaded from environment variables or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).
  **使用环境变量** — 所有密钥必须从环境变量或密钥管理器（如 AWS Secrets Manager、HashiCorp Vault）加载。

- [ ] **Check AI output for leaked secrets** — AI may generate placeholder secrets like `sk-abc123` that look real. Scan all generated code.
  **检查 AI 输出是否泄露密钥** — AI 可能生成看起来像真实密钥的占位符（如 `sk-abc123`）。扫描所有生成的代码。

- [ ] **Use .gitignore** — Ensure `.env`, credentials files, and private keys are in `.gitignore`.
  **使用 .gitignore** — 确保 `.env`、凭证文件和私钥在 `.gitignore` 中。

- [ ] **Rotate secrets if exposed** — If a secret was accidentally included in a prompt or committed, rotate it immediately.
  **如果泄露则轮换密钥** — 如果密钥意外包含在提示中或被提交，请立即轮换。

---

## 2. OWASP Top 10 for AI-Generated Code / AI 生成代码的 OWASP 十大

### A01: Broken Access Control / 失效的访问控制

- [ ] AI-generated endpoints include proper authorization checks.
  AI 生成的端点包含适当的授权检查。
- [ ] Role-based access control (RBAC) is implemented, not just authentication.
  实施了基于角色的访问控制 (RBAC)，而不仅仅是认证。
- [ ] AI did not generate overly permissive CORS configurations.
  AI 未生成过于宽松的 CORS 配置。

### A02: Cryptographic Failures / 加密失败

- [ ] AI-generated code uses current cryptographic standards (AES-256, SHA-256+, not MD5/SHA-1).
  AI 生成的代码使用当前的加密标准（AES-256、SHA-256+，而非 MD5/SHA-1）。
- [ ] Sensitive data is encrypted at rest and in transit.
  敏感数据在静态和传输中都已加密。
- [ ] No hardcoded encryption keys or IVs in generated code.
  生成的代码中没有硬编码的加密密钥或 IV。

### A03: Injection / 注入

- [ ] All database queries use parameterized queries or ORM methods (see SQL Injection section below).
  所有数据库查询使用参数化查询或 ORM 方法（参见下方 SQL 注入部分）。
- [ ] No `eval()`, `exec()`, or dynamic code execution with user input.
  没有使用 `eval()`、`exec()` 或带用户输入的动态代码执行。
- [ ] Template rendering uses auto-escaping (see XSS section below).
  模板渲染使用自动转义（参见下方 XSS 部分）。

### A04: Insecure Design / 不安全的设计

- [ ] AI-generated architecture follows the principle of least privilege.
  AI 生成的架构遵循最小权限原则。
- [ ] Error handling does not expose internal details to users.
  错误处理不会向用户暴露内部细节。

### A05: Security Misconfiguration / 安全配置错误

- [ ] AI-generated Docker/K8s configs do not run as root.
  AI 生成的 Docker/K8s 配置不以 root 运行。
- [ ] Debug mode is disabled in production configurations.
  生产配置中已禁用调试模式。
- [ ] Default credentials are not present in generated configs.
  生成的配置中不存在默认凭证。

### A06: Vulnerable and Outdated Components / 易受攻击和过时的组件

- [ ] AI-suggested dependencies are checked for known vulnerabilities (see Dependency Security below).
  AI 建议的依赖已检查已知漏洞（参见下方依赖安全）。

### A07: Identification and Authentication Failures / 身份识别和认证失败

- [ ] Password storage uses bcrypt, scrypt, or Argon2 (not plain text or simple hashing).
  密码存储使用 bcrypt、scrypt 或 Argon2（而非明文或简单哈希）。
- [ ] Session management follows security best practices.
  会话管理遵循安全最佳实践。

### A08: Software and Data Integrity Failures / 软件和数据完整性失败

- [ ] AI-generated CI/CD pipelines pin dependency versions.
  AI 生成的 CI/CD 流水线固定依赖版本。
- [ ] Deserialization of untrusted data is avoided or validated.
  避免或验证了不受信任数据的反序列化。

### A09: Security Logging and Monitoring Failures / 安全日志和监控失败

- [ ] Security events are logged (see Logging section below).
  安全事件已记录（参见下方日志部分）。

### A10: Server-Side Request Forgery (SSRF) / 服务器端请求伪造

- [ ] AI-generated code that makes HTTP requests validates and restricts URLs.
  AI 生成的发起 HTTP 请求的代码验证并限制 URL。
- [ ] Internal network addresses (127.0.0.1, 10.x, 169.254.x) are blocked in URL inputs.
  URL 输入中阻止了内部网络地址（127.0.0.1、10.x、169.254.x）。

---

## 3. Dependency Security / 依赖安全

AI frequently suggests packages that may be outdated or vulnerable.

AI 经常建议可能已过时或存在漏洞的包。

- [ ] **Verify package names** — AI may hallucinate package names that don't exist or suggest typo-squatting packages.
  **验证包名称** — AI 可能臆造不存在的包名称或建议仿冒包。

- [ ] **Check version currency** — AI training data has a cutoff date. Suggested versions may be outdated.
  **检查版本时效** — AI 训练数据有截止日期。建议的版本可能已过时。

- [ ] **Run vulnerability scans** — Use `npm audit`, `pip audit`, `cargo audit`, `snyk`, or `trivy` on all dependencies.
  **运行漏洞扫描** — 对所有依赖使用 `npm audit`、`pip audit`、`cargo audit`、`snyk` 或 `trivy`。

- [ ] **Pin versions** — Use exact versions, not ranges (e.g., `1.2.3` not `^1.2.3`).
  **固定版本** — 使用精确版本，而非范围（如 `1.2.3` 而非 `^1.2.3`）。

- [ ] **Verify package authenticity** — Check that the package is the official one from the correct publisher.
  **验证包真实性** — 检查包是否来自正确发布者的官方包。

---

## 4. Input Validation / 输入验证

AI-generated code often accepts user input without proper validation.

AI 生成的代码经常接受用户输入而没有适当的验证。

- [ ] **Validate all user inputs** — Type, length, format, and range checks on every input.
  **验证所有用户输入** — 对每个输入进行类型、长度、格式和范围检查。

- [ ] **Whitelist over blacklist** — Prefer allowlists over denylists for input validation.
  **白名单优于黑名单** — 输入验证优先使用允许列表而非拒绝列表。

- [ ] **Sanitize file paths** — Prevent path traversal attacks (`../../../etc/passwd`).
  **清理文件路径** — 防止路径遍历攻击（`../../../etc/passwd`）。

- [ ] **Validate file uploads** — Check file type, size, and content (not just the extension).
  **验证文件上传** — 检查文件类型、大小和内容（不仅仅是扩展名）。

- [ ] **Limit request body size** — Set maximum payload sizes on all endpoints.
  **限制请求体大小** — 在所有端点上设置最大载荷大小。

---

## 5. Authentication and Authorization / 认证和授权

- [ ] **Multi-factor authentication** — AI-generated auth flows should support MFA where appropriate.
  **多因素认证** — AI 生成的认证流程应在适当情况下支持 MFA。

- [ ] **Token expiration** — JWT and session tokens have reasonable expiration times.
  **令牌过期** — JWT 和会话令牌具有合理的过期时间。

- [ ] **Secure token storage** — Tokens stored in httpOnly cookies, not localStorage.
  **安全令牌存储** — 令牌存储在 httpOnly cookie 中，而非 localStorage。

- [ ] **Authorization on every request** — Every API endpoint checks permissions, not just the login.
  **每次请求都进行授权** — 每个 API 端点都检查权限，而不仅仅是登录。

- [ ] **Avoid broken object-level authorization** — Users should only access their own resources.
  **避免失效的对象级授权** — 用户应只能访问自己的资源。

---

## 6. SQL Injection Prevention / SQL 注入防护

AI-generated database code is a common source of injection vulnerabilities.

AI 生成的数据库代码是注入漏洞的常见来源。

- [ ] **Always use parameterized queries** — Never concatenate user input into SQL strings.
  **始终使用参数化查询** — 绝不将用户输入拼接到 SQL 字符串中。

  ```python
  # BAD / 错误
  cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

  # GOOD / 正确
  cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
  ```

- [ ] **Use ORM methods** — Prefer ORM query builders over raw SQL.
  **使用 ORM 方法** — 优先使用 ORM 查询构建器而非原始 SQL。

- [ ] **Validate dynamic table/column names** — If AI generates dynamic SQL, validate identifiers against an allowlist.
  **验证动态表/列名** — 如果 AI 生成动态 SQL，请对照允许列表验证标识符。

- [ ] **Limit database permissions** — Application database users should have minimal privileges.
  **限制数据库权限** — 应用程序数据库用户应具有最小权限。

---

## 7. XSS Prevention / XSS 防护

- [ ] **Enable auto-escaping** — Use template engines that auto-escape output (Jinja2, React JSX, etc.).
  **启用自动转义** — 使用自动转义输出的模板引擎（Jinja2、React JSX 等）。

- [ ] **Avoid `dangerouslySetInnerHTML`** — AI often generates React code using this. Review every instance.
  **避免 `dangerouslySetInnerHTML`** — AI 经常生成使用此方法的 React 代码。审查每个实例。

- [ ] **Set Content-Security-Policy headers** — Restrict inline scripts and external resources.
  **设置 Content-Security-Policy 头** — 限制内联脚本和外部资源。

- [ ] **Sanitize user-generated HTML** — Use a library like DOMPurify if you must render HTML from users.
  **清理用户生成的 HTML** — 如果必须渲染用户的 HTML，请使用 DOMPurify 等库。

- [ ] **Validate URLs in links and redirects** — Prevent `javascript:` and data URLs.
  **验证链接和重定向中的 URL** — 防止 `javascript:` 和 data URL。

---

## 8. Rate Limiting / 速率限制

AI-generated APIs often lack rate limiting entirely.

AI 生成的 API 通常完全缺少速率限制。

- [ ] **Add rate limiting to all public endpoints** — Especially login, registration, and password reset.
  **为所有公共端点添加速率限制** — 特别是登录、注册和密码重置。

- [ ] **Implement per-user and per-IP limits** — Prevent both authenticated and unauthenticated abuse.
  **实施每用户和每 IP 限制** — 防止认证和未认证的滥用。

- [ ] **Use 429 status codes** — Return proper `429 Too Many Requests` with `Retry-After` headers.
  **使用 429 状态码** — 返回正确的 `429 Too Many Requests` 并包含 `Retry-After` 头。

- [ ] **Rate limit AI API calls** — Your own calls to Claude/OpenAI should have circuit breakers.
  **对 AI API 调用进行速率限制** — 你自己对 Claude/OpenAI 的调用应有熔断机制。

---

## 9. Logging and Audit / 日志和审计

- [ ] **Log security events** — Failed logins, permission denials, input validation failures.
  **记录安全事件** — 登录失败、权限拒绝、输入验证失败。

- [ ] **Never log secrets** — Ensure API keys, passwords, and tokens are never written to logs.
  **绝不记录密钥** — 确保 API 密钥、密码和令牌绝不写入日志。

- [ ] **Log AI interactions** — Record what prompts were sent and what code was generated (for audit).
  **记录 AI 交互** — 记录发送了哪些提示和生成了哪些代码（用于审计）。

- [ ] **Structured logging** — Use structured log formats (JSON) for easy analysis.
  **结构化日志** — 使用结构化日志格式 (JSON) 以便分析。

- [ ] **Log retention policy** — Define how long logs are kept and where they are stored.
  **日志保留策略** — 定义日志保留多长时间以及存储在哪里。

- [ ] **Monitor for anomalies** — Set up alerts for unusual patterns in AI-generated code deployment.
  **监控异常** — 为 AI 生成代码部署中的异常模式设置告警。

---

## Quick Reference / 快速参考

| Priority / 优先级 | Check / 检查项 | Risk if Missed / 遗漏风险 |
|---|---|---|
| Critical / 严重 | No secrets in prompts or code / 提示或代码中无密钥 | Full system compromise / 系统完全被攻破 |
| Critical / 严重 | Parameterized SQL queries / 参数化 SQL 查询 | Data breach via SQL injection / 通过 SQL 注入泄露数据 |
| Critical / 严重 | Input validation / 输入验证 | Injection attacks / 注入攻击 |
| High / 高 | Dependency vulnerability scan / 依赖漏洞扫描 | Known CVE exploitation / 已知 CVE 利用 |
| High / 高 | Authentication on all endpoints / 所有端点认证 | Unauthorized access / 未授权访问 |
| High / 高 | XSS prevention / XSS 防护 | Account takeover / 账户接管 |
| Medium / 中 | Rate limiting / 速率限制 | Service abuse, DoS / 服务滥用、DoS |
| Medium / 中 | Security logging / 安全日志 | Undetected breaches / 未检测到的入侵 |
| Low / 低 | Structured logging format / 结构化日志格式 | Slow incident response / 事件响应缓慢 |
