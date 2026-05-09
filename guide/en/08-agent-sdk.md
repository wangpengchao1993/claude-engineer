# Claude Agent SDK

> Build production-ready AI agents with Claude Agent SDK — tool use, memory, guardrails, and multi-agent orchestration.

## Table of Contents

- [What is the Agent SDK?](#what-is-the-agent-sdk)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Defining Tools](#defining-tools)
- [Agent Configuration](#agent-configuration)
- [Guardrails](#guardrails)
- [Multi-Agent Orchestration](#multi-agent-orchestration)
- [Patterns & Best Practices](#patterns--best-practices)

---

## What is the Agent SDK?

The Claude Agent SDK provides a framework for building AI agents that can:

- **Use tools** to interact with the real world (databases, APIs, file systems)
- **Reason** through multi-step problems
- **Follow guardrails** to stay within defined boundaries
- **Orchestrate** multiple specialized agents

It abstracts the tool-use loop, error handling, and agent coordination so you can focus on your application logic.

---

## Installation

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

---

## Quick Start

### Minimal Agent

```python
from claude_agent_sdk import Agent, tool

@tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().isoformat()

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    # Use ast.literal_eval for safety
    import ast
    result = eval(compile(ast.parse(expression, mode='eval'), '<string>', 'eval'))
    return str(result)

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[get_current_time, calculate],
    system_prompt="You are a helpful assistant with access to a clock and calculator.",
)

result = agent.run("What time is it, and what's 2^32?")
print(result)
```

### Agent with Context

```python
agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[search_docs, query_database, send_email],
    system_prompt="""You are a customer support agent for Acme Corp.

    Rules:
    - Always search docs before answering product questions
    - Escalate billing issues to human support
    - Never share internal pricing or discount codes
    """,
    max_turns=20,
)

# Run with conversation history
result = agent.run(
    "I can't log into my account",
    context={"user_id": "usr_123", "plan": "pro"}
)
```

---

## Defining Tools

### Basic Tool

```python
from claude_agent_sdk import tool

@tool
def search_products(query: str, category: str = None, max_results: int = 10) -> list[dict]:
    """Search the product catalog.

    Args:
        query: Search query string
        category: Optional category filter (electronics, clothing, etc.)
        max_results: Maximum number of results to return (default: 10)
    """
    # Your implementation
    results = db.products.search(query, category=category, limit=max_results)
    return [{"id": p.id, "name": p.name, "price": p.price} for p in results]
```

### Async Tool

```python
@tool
async def fetch_url(url: str) -> str:
    """Fetch the content of a web page."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### Tool with Validation

```python
from pydantic import BaseModel, Field

class CreateOrderInput(BaseModel):
    product_id: str = Field(description="Product ID to order")
    quantity: int = Field(ge=1, le=100, description="Quantity (1-100)")
    shipping_address: str = Field(description="Full shipping address")

@tool(input_model=CreateOrderInput)
def create_order(input: CreateOrderInput) -> dict:
    """Create a new order for a product."""
    order = OrderService.create(
        product_id=input.product_id,
        quantity=input.quantity,
        address=input.shipping_address
    )
    return {"order_id": order.id, "status": "created"}
```

### Tool Error Handling

```python
from claude_agent_sdk import tool, ToolError

@tool
def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """Transfer funds between accounts."""
    if amount <= 0:
        raise ToolError("Amount must be positive")
    if amount > 10000:
        raise ToolError("Transfers over $10,000 require manual approval")

    try:
        result = bank.transfer(from_account, to_account, amount)
        return {"transaction_id": result.id, "status": "completed"}
    except InsufficientFunds:
        raise ToolError("Insufficient funds in source account")
```

---

## Agent Configuration

### Full Configuration

```python
agent = Agent(
    # Model settings
    model="claude-sonnet-4-6-20250514",
    max_tokens=4096,
    temperature=0.7,

    # Agent behavior
    system_prompt="...",
    tools=[tool1, tool2, tool3],
    max_turns=30,           # Maximum tool-use iterations

    # Extended thinking for complex reasoning
    thinking={
        "type": "enabled",
        "budget_tokens": 5000
    },
)
```

### Dynamic System Prompts

```python
def build_system_prompt(user_context: dict) -> str:
    return f"""You are a support agent for {user_context['company']}.

    The customer's plan: {user_context['plan']}
    Account age: {user_context['account_age_days']} days
    Previous tickets: {user_context['ticket_count']}

    Adjust your tone and depth based on the customer's history.
    """

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=support_tools,
    system_prompt=build_system_prompt(user_ctx),
)
```

---

## Guardrails

### Input Guardrails

Validate user input before the agent processes it:

```python
from claude_agent_sdk import Agent, InputGuardrail

def check_pii(user_message: str) -> str | None:
    """Block messages containing credit card numbers."""
    import re
    if re.search(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', user_message):
        return "Please don't share credit card numbers. I can help you update payment info through our secure portal."
    return None  # None means "allowed"

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=support_tools,
    input_guardrails=[InputGuardrail(check_pii)],
)
```

### Output Guardrails

Validate agent responses before returning to the user:

```python
from claude_agent_sdk import OutputGuardrail

def check_no_internal_info(response: str) -> str | None:
    """Ensure agent doesn't leak internal information."""
    blocked_terms = ["internal-api", "admin-panel", "secret-key"]
    for term in blocked_terms:
        if term in response.lower():
            return "I apologize, but I can't share that information. Let me help you in another way."
    return None

agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=support_tools,
    output_guardrails=[OutputGuardrail(check_no_internal_info)],
)
```

### Tool Guardrails

Control which tools can be used and when:

```python
def limit_database_writes(tool_name: str, tool_input: dict) -> str | None:
    """Prevent destructive database operations."""
    if tool_name == "execute_sql":
        sql = tool_input.get("query", "").upper()
        if any(kw in sql for kw in ["DELETE", "DROP", "TRUNCATE", "UPDATE"]):
            return "Write operations are not allowed. Please use read-only queries."
    return None
```

---

## Multi-Agent Orchestration

### Handoff Pattern

```python
from claude_agent_sdk import Agent, handoff

# Specialized agents
billing_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_balance, process_refund, update_plan],
    system_prompt="You handle billing questions and refunds.",
)

technical_agent = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[check_logs, restart_service, run_diagnostic],
    system_prompt="You handle technical issues and debugging.",
)

# Router agent
router = Agent(
    model="claude-sonnet-4-6-20250514",
    tools=[
        handoff(billing_agent, "Transfer to billing support"),
        handoff(technical_agent, "Transfer to technical support"),
    ],
    system_prompt="""You are a front-desk agent. Determine the user's issue
    and transfer them to the appropriate specialist:
    - Billing: payments, refunds, plan changes, invoices
    - Technical: bugs, errors, outages, configuration""",
)

# User talks to router, gets handed off automatically
result = router.run("My API keeps returning 503 errors")
```

### Pipeline Pattern

```python
# Sequential processing
async def process_document(document: str) -> dict:
    # Step 1: Extract data
    extractor = Agent(
        model="claude-haiku-4-5-20251001",  # Fast model for extraction
        tools=[],
        system_prompt="Extract structured data from documents. Return JSON.",
    )
    extracted = await extractor.run(f"Extract key fields from:\n{document}")

    # Step 2: Validate and enrich
    validator = Agent(
        model="claude-sonnet-4-6-20250514",
        tools=[lookup_company, verify_address],
        system_prompt="Validate and enrich extracted data using tools.",
    )
    validated = await validator.run(f"Validate this data:\n{extracted}")

    # Step 3: Generate report
    reporter = Agent(
        model="claude-sonnet-4-6-20250514",
        tools=[],
        system_prompt="Generate concise business reports from data.",
    )
    report = await reporter.run(f"Generate a report from:\n{validated}")

    return {"report": report}
```

---

## Patterns & Best Practices

### 1. Keep Tools Focused

```python
# Bad: one mega-tool
@tool
def do_everything(action: str, params: dict) -> dict:
    """Does everything based on action parameter."""
    ...

# Good: focused, single-purpose tools
@tool
def search_orders(customer_id: str, status: str = None) -> list[dict]:
    """Search orders for a customer, optionally filtered by status."""
    ...

@tool
def cancel_order(order_id: str, reason: str) -> dict:
    """Cancel an order and initiate refund."""
    ...
```

### 2. Write Detailed Tool Descriptions

The description is how Claude decides when to use a tool. Be specific:

```python
@tool
def search_knowledge_base(query: str, category: str = None) -> list[dict]:
    """Search the company knowledge base for articles matching the query.

    Use this tool when:
    - User asks a product question you don't know the answer to
    - User needs step-by-step instructions for a feature
    - You need to verify a fact about our product

    Do NOT use this tool for:
    - Account-specific questions (use get_account instead)
    - Billing inquiries (use check_billing instead)

    Args:
        query: Natural language search query
        category: Optional filter: "getting-started", "api", "billing", "troubleshooting"
    """
    ...
```

### 3. Implement Graceful Degradation

```python
@tool
def query_database(sql: str) -> dict:
    """Run a read-only SQL query."""
    try:
        result = db.execute(sql)
        if len(result.rows) > 100:
            return {
                "rows": result.rows[:100],
                "total": len(result.rows),
                "truncated": True,
                "message": "Showing first 100 of {len(result.rows)} rows"
            }
        return {"rows": result.rows, "total": len(result.rows)}
    except DatabaseError as e:
        raise ToolError(f"Query failed: {e}. Try simplifying the query.")
```

### 4. Use the Right Model for Each Agent

| Agent Role | Recommended Model |
|-----------|-------------------|
| Router / Classifier | Haiku 4.5 (fast, cheap) |
| Data extraction | Haiku 4.5 |
| Business logic | Sonnet 4.6 |
| Complex reasoning | Opus 4.6 |
| Code generation | Sonnet 4.6 or Opus 4.6 |

---

<p align="center">
  <strong>Next:</strong> <a href="09-prompt-engineering.md">Prompt Engineering</a> — Get the best results from Claude
</p>
