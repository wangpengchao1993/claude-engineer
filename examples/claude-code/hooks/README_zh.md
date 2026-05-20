# Claude Code Hooks 配置说明

## 概述

本文件 (`settings.json`) 用于配置 Claude Code 的权限和钩子（hooks）。由于 JSON 格式不支持注释，本文档作为配套说明文件，解释各配置项的含义和用途。

## 权限配置 (permissions)

`permissions.allow` 数组定义了 Claude Code 可以**自动执行**而无需用户确认的操作。

```json
"permissions": {
  "allow": [
    "Read",
    "Glob",
    "Grep",
    "Bash(npm test)",
    "Bash(npm run lint)",
    "Bash(npm run build)",
    "Bash(pnpm test)",
    "Bash(pnpm lint)",
    "Bash(cargo test)",
    "Bash(cargo clippy)",
    "Bash(make test)",
    "Bash(make lint)"
  ]
}
```

### 各权限条目说明

| 权限 | 说明 |
|------|------|
| `Read` | 允许读取文件内容，无需用户确认 |
| `Glob` | 允许使用通配符模式搜索文件路径 |
| `Grep` | 允许在文件内容中进行正则搜索 |
| `Bash(npm test)` | 允许执行 `npm test` 命令（运行项目测试） |
| `Bash(npm run lint)` | 允许执行 `npm run lint` 命令（代码风格检查） |
| `Bash(npm run build)` | 允许执行 `npm run build` 命令（构建项目） |
| `Bash(pnpm test)` | 允许执行 `pnpm test` 命令（pnpm 包管理器下运行测试） |
| `Bash(pnpm lint)` | 允许执行 `pnpm lint` 命令（pnpm 包管理器下代码检查） |
| `Bash(cargo test)` | 允许执行 `cargo test` 命令（Rust 项目测试） |
| `Bash(cargo clippy)` | 允许执行 `cargo clippy` 命令（Rust 代码静态分析） |
| `Bash(make test)` | 允许执行 `make test` 命令（Makefile 驱动的测试） |
| `Bash(make lint)` | 允许执行 `make lint` 命令（Makefile 驱动的代码检查） |

> **注意**：未列入 `allow` 的操作（如 `Edit`、`Write`、或其他 `Bash` 命令）仍需要用户手动确认后才能执行。

## 钩子配置 (hooks)

钩子（hooks）允许你在 Claude Code 执行特定操作的前后自动运行自定义脚本。配置中定义了三种钩子类型：

### PreToolUse — 工具使用前钩子

在 Claude Code 调用指定工具**之前**执行。可用于拦截或验证操作。

```json
"PreToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      "./scripts/check-protected-files.sh $CLAUDE_FILE_PATH"
    ]
  }
]
```

- **matcher**: `"Edit|Write"` — 使用正则表达式匹配工具名称，`|` 表示"或"，即当 Claude 尝试使用 `Edit` 或 `Write` 工具时触发
- **脚本**: `check-protected-files.sh` — 在文件被编辑或写入之前检查目标文件是否为受保护文件（如配置文件、锁文件等）。通过环境变量 `$CLAUDE_FILE_PATH` 获取即将操作的文件路径
- **用途**: 防止 Claude 意外修改关键文件。如果脚本返回非零退出码，该操作将被阻止

### PostToolUse — 工具使用后钩子

在 Claude Code 调用指定工具**之后**执行。可用于后处理或验证结果。

```json
"PostToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      "./scripts/auto-lint.sh $CLAUDE_FILE_PATH"
    ]
  }
]
```

- **matcher**: `"Edit|Write"` — 同样匹配 `Edit` 或 `Write` 工具
- **脚本**: `auto-lint.sh` — 在文件被修改后自动对该文件执行代码格式化/风格检查（lint），确保修改后的代码符合项目规范
- **用途**: 自动保持代码质量，无需手动运行 lint 工具

### Stop — 停止钩子

在 Claude Code 完成所有操作并**即将停止**时执行。

```json
"Stop": [
  {
    "matcher": "",
    "hooks": [
      "./scripts/notify-done.sh"
    ]
  }
]
```

- **matcher**: `""` — 空字符串表示匹配所有情况，即无论 Claude 因何种原因停止都会触发
- **脚本**: `notify-done.sh` — 发送通知告知用户 Claude Code 已完成任务（例如通过系统通知、Slack 消息等）
- **用途**: 当 Claude 在执行长时间任务时，用户可以离开，任务完成后会自动收到通知

## matcher 匹配规则总结

| 模式 | 含义 |
|------|------|
| `"Edit\|Write"` | 匹配 `Edit` 或 `Write` 工具（正则表达式"或"语法） |
| `""` | 空字符串，匹配所有情况 |
| `"Bash"` | 仅匹配 `Bash` 工具（示例，本文件未使用） |

## 环境变量

钩子脚本中可使用以下 Claude Code 提供的环境变量：

| 变量 | 说明 |
|------|------|
| `$CLAUDE_FILE_PATH` | Claude 当前操作的目标文件路径 |
