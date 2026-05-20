# Claude Code MCP 服务器配置说明

## 概述

本文件 (`full-stack-dev.json`) 用于配置 Claude Code 的 MCP（Model Context Protocol）服务器。由于 JSON 格式不支持注释，本文档作为配套说明文件，解释各配置项的含义和用途。

## 什么是 MCP 服务器？

MCP（模型上下文协议）是一种开放协议，允许 Claude 与外部工具和数据源进行交互。每个 MCP 服务器是一个独立的进程，为 Claude 提供特定的能力扩展，例如访问数据库、调用 GitHub API、读取文件系统或抓取网页内容。

通过配置 MCP 服务器，Claude Code 可以：
- 直接查询和操作数据库
- 与 GitHub 仓库交互（查看 issue、PR 等）
- 访问指定目录下的文件
- 获取网页内容

## 服务器配置详解

所有服务器定义在 `mcpServers` 对象中，每个键名即为服务器的标识名称。

### database — PostgreSQL 数据库服务器

```json
"database": {
  "command": "npx",
  "args": [
    "mcp-server-postgres",
    "postgresql://dev:devpassword@localhost:5432/myapp_dev"
  ],
  "env": {}
}
```

| 字段 | 说明 |
|------|------|
| `command` | `npx` — 使用 Node.js 的 npx 命令运行包 |
| `args[0]` | `mcp-server-postgres` — PostgreSQL MCP 服务器包名 |
| `args[1]` | 数据库连接字符串，格式为 `postgresql://用户名:密码@主机:端口/数据库名` |
| `env` | 无需额外环境变量 |

**用途**: 允许 Claude 直接查询开发环境的 PostgreSQL 数据库，执行 SQL 查询、查看表结构等操作。

> **注意**: 示例中使用的是本地开发数据库连接。在生产环境中，建议通过环境变量传递敏感的连接信息，而非直接写在配置文件中。

### github — GitHub 服务器

```json
"github": {
  "command": "npx",
  "args": ["@anthropic-ai/mcp-github"],
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

| 字段 | 说明 |
|------|------|
| `command` | `npx` — 使用 npx 运行包 |
| `args[0]` | `@anthropic-ai/mcp-github` — Anthropic 官方 GitHub MCP 服务器包 |
| `env.GITHUB_TOKEN` | `${GITHUB_TOKEN}` — 引用系统环境变量中的 GitHub 个人访问令牌 |

**用途**: 允许 Claude 与 GitHub 交互，包括查看仓库、issue、pull request、代码审查等操作。

**环境变量准备**: 使用前需确保已设置 `GITHUB_TOKEN` 环境变量：
```bash
export GITHUB_TOKEN="ghp_你的GitHub个人访问令牌"
```

### filesystem — 文件系统服务器

```json
"filesystem": {
  "command": "npx",
  "args": [
    "@anthropic-ai/mcp-filesystem",
    "/home/user/docs/api-specs"
  ],
  "env": {}
}
```

| 字段 | 说明 |
|------|------|
| `command` | `npx` — 使用 npx 运行包 |
| `args[0]` | `@anthropic-ai/mcp-filesystem` — Anthropic 官方文件系统 MCP 服务器包 |
| `args[1]` | `/home/user/docs/api-specs` — 允许访问的目录路径 |
| `env` | 无需额外环境变量 |

**用途**: 允许 Claude 访问指定目录下的文件，例如 API 规范文档。通过限制目录路径来控制访问范围，确保 Claude 只能读取授权的文件。

> **提示**: 可根据项目需要修改路径，指向你的文档目录或其他需要 Claude 访问的资源目录。

### fetch — 网页抓取服务器

```json
"fetch": {
  "command": "npx",
  "args": ["mcp-server-fetch"],
  "env": {}
}
```

| 字段 | 说明 |
|------|------|
| `command` | `npx` — 使用 npx 运行包 |
| `args[0]` | `mcp-server-fetch` — 网页抓取 MCP 服务器包 |
| `env` | 无需额外环境变量 |

**用途**: 允许 Claude 获取网页内容，例如查阅在线 API 文档、获取远程资源等。

## 配置字段通用说明

每个 MCP 服务器条目包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `command` | 字符串 | 启动服务器的命令（如 `npx`、`node`、`python` 等） |
| `args` | 字符串数组 | 传递给命令的参数列表 |
| `env` | 对象 | 服务器运行时需要的环境变量，`${VAR}` 语法表示引用系统环境变量 |

## 环境变量汇总

| 变量名 | 用于 | 说明 |
|--------|------|------|
| `GITHUB_TOKEN` | github 服务器 | GitHub 个人访问令牌，用于 API 认证 |
