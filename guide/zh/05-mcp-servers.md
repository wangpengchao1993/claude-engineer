# MCP 服务器 — 扩展 Claude 的能力

> Model Context Protocol (MCP) 让你给 Claude 添加内置工具之外的新能力。连接数据库、API、浏览器等。

## 目录

- [什么是 MCP？](#什么是-mcp)
- [工作原理](#工作原理)
- [添加 MCP 服务器](#添加-mcp-服务器)
- [常用 MCP 服务器](#常用-mcp-服务器)
- [配置方法](#配置方法)
- [使用场景](#使用场景)
- [构建自定义 MCP 服务器](#构建自定义-mcp-服务器)
- [最佳实践](#最佳实践)

---

## 什么是 MCP？

**Model Context Protocol (MCP)** 是一个开放标准，让你用自定义工具扩展 Claude。可以理解为插件系统：

- **没有 MCP**：Claude 可以读文件、编辑代码、运行 Shell 命令
- **有了 MCP**：Claude 还可以查询数据库、调用 API、控制浏览器、搜索网页，以及你能构建的任何东西

---

## 工作原理

```
┌─────────────┐         ┌─────────────────┐
│ Claude Code  │ ◄─MCP──► │ MCP 服务器       │
│ (客户端)     │         │ (如：数据库)      │
└─────────────┘         └─────────────────┘
       │
       │                 ┌─────────────────┐
       └────────MCP────► │ MCP 服务器       │
                         │ (如：GitHub)      │
                         └─────────────────┘
```

1. 在 Claude Code 设置中配置 MCP 服务器
2. Claude Code 自动启动服务器
3. 服务器向 Claude 注册工具
4. Claude 可以像使用内置工具一样使用这些工具

---

## 添加 MCP 服务器

### 通过 CLI（最简单）

```bash
# 添加服务器
claude mcp add <名称> <命令> [参数...]

# 示例
claude mcp add filesystem npx @anthropic-ai/mcp-filesystem /path/to/dir
claude mcp add github npx @anthropic-ai/mcp-github

# 指定范围（项目或全局）
claude mcp add --scope project database npx mcp-server-postgres "postgresql://localhost/mydb"
claude mcp add --scope global github npx @anthropic-ai/mcp-github

# 列出已配置的服务器
claude mcp list

# 移除服务器
claude mcp remove <名称>
```

### 通过配置文件

在 `.claude/settings.json` 中：

```jsonc
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["package-name", "arg1"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

---

## 常用 MCP 服务器

### PostgreSQL 数据库

```jsonc
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["mcp-server-postgres", "postgresql://user:pass@localhost:5432/mydb"]
    }
  }
}
```
工具：运行 SQL 查询、列出表、描述 Schema。

### GitHub

```jsonc
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-github"],
      "env": { "GITHUB_TOKEN": "ghp_your_token" }
    }
  }
}
```
工具：创建 Issue、管理 PR、搜索仓库。

### 浏览器自动化 (Puppeteer)

```jsonc
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["mcp-server-puppeteer"]
    }
  }
}
```
工具：导航页面、截图、点击元素、填写表单。

### 文件系统

```jsonc
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```
让 Claude 访问项目目录之外的文件。

### Web 搜索 (Brave)

```jsonc
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["mcp-server-brave-search"],
      "env": { "BRAVE_API_KEY": "your-key" }
    }
  }
}
```

### HTTP 请求 (Fetch)

```jsonc
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

---

## 使用场景

### 1. 数据库驱动开发

```
"查看 users 表的 schema，写一个迁移添加 'avatar_url' 列"
"查询订单最多的前 10 个用户，优化慢查询"
```

### 2. 跨仓库工作

```
"检查 API 仓库有哪些未关闭的 issue，看看是否与我们的认证修改相关"
"在前端仓库创建一个 issue，说明我们刚做的 API 变更需要 UI 更新"
```

### 3. 浏览器测试

```
"打开 localhost:3000，导航到登录页，截个图"
"用测试数据填写注册表单并提交，检查成功页面是否出现"
```

---

## 构建自定义 MCP 服务器

### TypeScript 最小示例

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.tool(
  "get_weather",
  "获取城市的当前天气",
  { city: z.string().describe("城市名称") },
  async ({ city }) => {
    const weather = await fetchWeather(city);
    return { content: [{ type: "text", text: JSON.stringify(weather) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python 最小示例

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("my-server")

@server.tool()
async def get_weather(city: str) -> list[types.TextContent]:
    """获取城市的当前天气。"""
    weather = await fetch_weather(city)
    return [types.TextContent(type="text", text=str(weather))]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)
```

---

## 最佳实践

1. **从小开始** — 不要一次添加 10 个服务器，从解决直接问题的 1-2 个开始
2. **项目范围** — 项目特定的服务器用 `--scope project`
3. **安全考虑** — 不要在配置中明文写 API 密钥，使用环境变量
4. **描述性命名** — `project-database` 而不是 `s1`
5. **在 CLAUDE.md 中记录** — 写明项目用了哪些 MCP 服务器

---

<p align="center">
  <strong>下一篇：</strong> <a href="06-multi-agent.md">多 Agent 模式</a> — 编排多个 Claude Agent
</p>
