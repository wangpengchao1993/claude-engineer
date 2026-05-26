# MCP Servers — Extend Claude's Capabilities

> Model Context Protocol (MCP) lets you give Claude new tools beyond its built-in set. Connect databases, APIs, browsers, and more.

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [How MCP Works](#how-mcp-works)
- [Adding MCP Servers](#adding-mcp-servers)
- [Popular MCP Servers](#popular-mcp-servers)
- [Configuration](#configuration)
- [Use Cases](#use-cases)
- [Building Custom MCP Servers](#building-custom-mcp-servers)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that lets you extend Claude with custom tools. Think of it as a plugin system:

- **Without MCP**: Claude can read files, edit code, and run shell commands
- **With MCP**: Claude can also query databases, call APIs, control browsers, search the web, and anything else you can build

MCP servers are lightweight processes that expose tools to Claude via a standardized protocol.

---

## How MCP Works

```
┌─────────────┐         ┌─────────────────┐
│ Claude Code  │ ◄─MCP──► │ MCP Server       │
│ (Client)     │         │ (e.g., database)  │
└─────────────┘         └─────────────────┘
       │
       │                 ┌─────────────────┐
       └────────MCP────► │ MCP Server       │
                         │ (e.g., GitHub)    │
                         └─────────────────┘
```

1. You configure MCP servers in Claude Code settings
2. Claude Code starts the servers automatically
3. The servers register their tools with Claude
4. Claude can call these tools like built-in ones
5. Results come back through the MCP protocol

---

## Adding MCP Servers

### Via CLI (Easiest)

```bash
# Add a server
claude mcp add <name> <command> [args...]

# Examples
claude mcp add filesystem npx @anthropic-ai/mcp-filesystem /path/to/dir
claude mcp add github npx @anthropic-ai/mcp-github

# With scope (project or global)
claude mcp add --scope project database npx mcp-server-postgres "postgresql://localhost/mydb"
claude mcp add --scope global github npx @anthropic-ai/mcp-github

# List configured servers
claude mcp list

# Remove a server
claude mcp remove <name>
```

### Via Settings File

In `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```jsonc
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["package-name", "arg1", "arg2"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

### Via Interactive Mode

```
/mcp
```

This opens an interactive menu to manage MCP servers.

---

## Popular MCP Servers

### File System Access

```jsonc
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@anthropic-ai/mcp-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

Gives Claude controlled access to files outside the project directory.

### GitHub

```jsonc
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token"
      }
    }
  }
}
```

Tools: Create issues, manage PRs, search repositories, read files from other repos.

### PostgreSQL

```jsonc
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "mcp-server-postgres",
        "postgresql://user:pass@localhost:5432/mydb"
      ]
    }
  }
}
```

Tools: Run SQL queries, list tables, describe schemas.

### SQLite

```jsonc
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "mcp-server-sqlite",
        "--db-path", "./data/app.db"
      ]
    }
  }
}
```

### Puppeteer (Browser Automation)

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

Tools: Navigate pages, take screenshots, click elements, fill forms.

### Web Search (Brave)

```jsonc
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["mcp-server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-key"
      }
    }
  }
}
```

### Memory (Persistent Knowledge)

```jsonc
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["mcp-server-memory"]
    }
  }
}
```

Tools: Store and retrieve persistent knowledge across sessions.

### Fetch (HTTP Requests)

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

Tools: Make HTTP requests to any URL, useful for API testing.

---

## Configuration

### Full Config Example

A real-world setup with multiple servers:

```jsonc
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["mcp-server-postgres", "postgresql://dev:dev@localhost:5432/myapp"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-filesystem", "/home/user/docs"],
      "env": {}
    }
  }
}
```

### Project vs Global Config

| Scope | File | Use For |
|-------|------|---------|
| Project | `.claude/settings.json` | Project-specific databases, APIs |
| Global | `~/.claude/settings.json` | GitHub, web search, personal tools |

### Security Considerations

- **Never commit API keys** in settings files — use environment variables
- **Limit file system access** to specific directories
- **Use read-only database users** for query-only access
- **Review MCP server code** before adding community servers

```jsonc
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"  // Reference env var
      }
    }
  }
}
```

---

## Use Cases

### 1. Database-Driven Development

```
"Show me the schema for the users table and write a migration
 to add an 'avatar_url' column"

"Query the database for the top 10 users by order count and
 optimize the query if it's slow"

"Check if the user_sessions table has proper indexes for
 our most common queries"
```

### 2. Cross-Repository Work

With the GitHub MCP server:

```
"Check what issues are open in our API repo and see if any
 relate to the auth changes we're making here"

"Create an issue in the frontend repo about the API change
 we just made that requires a UI update"
```

### 3. Documentation Research

With filesystem + fetch servers:

```
"Read the API specs from /docs/api-spec and check if our
 implementation matches"

"Fetch the latest React docs and help me migrate this
 component to the new API"
```

### 4. Browser Testing

With the Puppeteer server:

```
"Open localhost:3000, navigate to the login page,
 and take a screenshot"

"Fill in the signup form with test data and submit it,
 then check if the success page appears"
```

---

## Building Custom MCP Servers

### Minimal TypeScript Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-custom-server",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "get_weather",
  "Get current weather for a city",
  {
    city: z.string().describe("City name"),
  },
  async ({ city }) => {
    // Your implementation here
    const weather = await fetchWeather(city);
    return {
      content: [{ type: "text", text: JSON.stringify(weather) }],
    };
  }
);

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Minimal Python Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("my-custom-server")

@server.tool()
async def get_weather(city: str) -> list[types.TextContent]:
    """Get current weather for a city."""
    weather = await fetch_weather(city)
    return [types.TextContent(type="text", text=str(weather))]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Register Your Custom Server

```bash
# If it's a local script
claude mcp add my-tool node /path/to/my-server.js

# If it's a Python script
claude mcp add my-tool python /path/to/my-server.py
```

---

## Best Practices

### 1. Start Small

Don't add 10 MCP servers at once. Start with one or two that solve immediate problems.

### 2. Use Project Scope for Project-Specific Servers

```bash
# Database for this project only
claude mcp add --scope project db npx mcp-server-postgres "$DATABASE_URL"
```

### 3. Keep Servers Lightweight

MCP servers run as background processes. Heavy servers slow down Claude Code startup.

### 4. Use Descriptive Names

```jsonc
// Bad
"s1": { ... }

// Good
"project-database": { ... }
```

### 5. Document MCP Setup in CLAUDE.md

```markdown
## MCP Servers
This project uses the following MCP servers:
- `database` — PostgreSQL access (read-only)
- `github` — For cross-repo issue tracking

To set up: run `./scripts/setup-mcp.sh`
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | Check `claude mcp list` and verify the command exists |
| "Tool not found" | Restart Claude Code after adding MCP server |
| Connection timeout | Check if the server process is running: `ps aux \| grep mcp` |
| Authentication errors | Verify env vars are set correctly |
| Server crashes | Check server logs, run the command manually to see errors |

### Debug Mode

Run the MCP server manually to check for errors:

```bash
# Run the server directly to see output
npx mcp-server-postgres "postgresql://localhost/mydb"

# Check if the process is running
claude mcp list
```

---

<p align="center">
  <strong>Next:</strong> <a href="06-multi-agent.md">Multi-Agent Patterns</a> — Orchestrate multiple Claude agents
</p>

---

[← Previous: Hooks & Automation](04-hooks-and-automation.md) | [Table of Contents](../../README.md) | [Next: Multi-Agent Patterns →](06-multi-agent.md)
