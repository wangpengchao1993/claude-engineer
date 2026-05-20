# LlamaIndex -- The Best Framework for RAG Applications

# LlamaIndex -- 最好的 RAG 应用框架

> **GitHub Stars**: ~35k | **Language**: Python | **License**: MIT
>
> Website: https://www.llamaindex.ai/ | Docs: https://docs.llamaindex.ai/

---

## What is LlamaIndex? / 什么是 LlamaIndex?

**English:**
LlamaIndex is a framework for connecting Large Language Models (LLMs) with your
own data. It specializes in **indexing**, **retrieving**, and **querying** data
from documents, databases, and APIs.

Think of it as a **"smart librarian"**: you give it a pile of books (your data),
it organizes them onto shelves (indexing), and when you ask a question, it knows
exactly which page to flip to (retrieval) before giving you an answer (query).

**中文：**
LlamaIndex 是一个将大语言模型（LLM）与你自己的数据连接起来的框架。它专注于对数据
进行**索引**、**检索**和**查询**。

你可以把它想象成一个**"智能图书管理员"**：你把一堆书（你的数据）交给它，它会把书
整理到书架上（索引），当你提问时，它知道该翻到哪一页（检索），然后给你答案（查询）。

---

## When to Use LlamaIndex / 什么时候用 LlamaIndex

**Great for / 适合：**

- Building Q&A systems over your own documents / 基于自有文档构建问答系统
- Enterprise knowledge bases / 企业知识库
- Connecting LLMs to databases, APIs, or file systems / 将 LLM 连接到数据库、API 或文件系统
- Retrieval-Augmented Generation (RAG) pipelines / RAG 检索增强生成管道

**Not ideal for / 不太适合：**

- Simple chatbots that don't need external data / 不需要外部数据的简单聊天机器人
- Agent-heavy tasks with complex tool use (use LangChain/LangGraph instead)
  / 需要大量 Agent 和复杂工具调用的任务（建议用 LangChain/LangGraph）
- General-purpose LLM orchestration without a data focus
  / 不以数据为中心的通用 LLM 编排

---

## Core Concepts / 核心概念

LlamaIndex has 5 key building blocks. Here they are with everyday analogies:

| Concept / 概念 | What it is / 是什么 | Analogy / 类比 |
|---|---|---|
| **Document** | A container for your raw data (a PDF, a web page, a text file). / 原始数据的容器（PDF、网页、文本文件） | A book on your desk / 桌上的一本书 |
| **Node** | A smaller chunk of a Document (a paragraph, a section). / 文档的更小片段（段落、章节） | A page or paragraph in that book / 书中的一页或一段 |
| **Index** | An organized structure built from Nodes for fast lookup. / 由节点构建的有组织结构，用于快速查找 | The library catalog / 图书馆目录 |
| **Retriever** | Finds the most relevant Nodes for a given question. / 为给定问题找到最相关的节点 | The librarian who fetches the right books / 帮你找书的图书管理员 |
| **Query Engine** | Combines the Retriever + LLM to produce a final answer. / 将检索器 + LLM 结合起来生成最终答案 | The librarian reads the book and summarizes it for you / 图书管理员读完书后给你总结 |

---

## How It Works / 工作原理

```
Documents  -->  Nodes  -->  Index  -->  Retriever  -->  Query Engine  -->  Response
 (原始文档)     (切分片段)   (构建索引)   (检索相关片段)   (LLM 生成回答)     (最终答案)
```

**Step by step / 逐步说明:**

1. **Load** -- You feed documents into LlamaIndex (PDF, text, web, DB...).
   / **加载** -- 将文档输入 LlamaIndex。
2. **Parse** -- Documents are split into smaller Nodes (chunks).
   / **解析** -- 文档被切分为更小的节点（片段）。
3. **Index** -- Nodes are embedded (converted to vectors) and stored in an Index.
   / **索引** -- 节点被嵌入（转换为向量）并存储到索引中。
4. **Retrieve** -- When you ask a question, the Retriever finds the top-k most
   relevant Nodes. / **检索** -- 提问时，检索器找到最相关的 top-k 个节点。
5. **Synthesize** -- The Query Engine sends those Nodes + your question to the LLM,
   which generates a response. / **生成** -- 查询引擎将节点和问题发送给 LLM 生成回答。

---

## Quick Start / 快速开始

### Install / 安装

```bash
# Install core package / 安装核心包
pip install llama-index-core

# Install with OpenAI integration (most common) / 安装 OpenAI 集成（最常用）
pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai

# Set your API key / 设置 API 密钥
export OPENAI_API_KEY="sk-..."
```

### Run the Example / 运行示例

```bash
# Run the document Q&A example / 运行文档问答示例
python document_qa.py

# Run the tests (no API key needed) / 运行测试（不需要 API 密钥）
pytest test_llamaindex.py -v
```

---

## LlamaIndex vs LangChain / LlamaIndex 与 LangChain 对比

Both are popular LLM frameworks, but they have different strengths:

两者都是流行的 LLM 框架，但各有所长：

| | LlamaIndex | LangChain |
|---|---|---|
| **Best for / 最擅长** | RAG, data indexing, document Q&A / RAG、数据索引、文档问答 | Agents, chains, tool use / Agent、链、工具调用 |
| **Data focus / 数据聚焦** | Very strong -- built for data / 非常强，为数据而生 | Good but not the primary focus / 不错但非主要关注点 |
| **Agent support / Agent 支持** | Basic / 基础 | Very strong / 非常强 |
| **Learning curve / 学习曲线** | Easier for RAG tasks / RAG 任务更简单 | Steeper, more flexible / 更陡但更灵活 |
| **When to choose / 何时选择** | Your main goal is "ask questions about my data" / 主要目标是"对我的数据提问" | You need complex agents and workflows / 需要复杂 Agent 和工作流 |

**Tip / 提示:** You can use both together! LlamaIndex as the retrieval layer,
LangChain as the agent layer. / 两者可以一起用！LlamaIndex 做检索层，LangChain 做
Agent 层。

---

## Learn More / 了解更多

- [Official Documentation / 官方文档](https://docs.llamaindex.ai/)
- [GitHub Repository / GitHub 仓库](https://github.com/run-llama/llama_index)
- [LlamaIndex Blog / 官方博客](https://www.llamaindex.ai/blog)
- [Discord Community / Discord 社区](https://discord.gg/dGcwcsnxhU)
- [LlamaHub (Data Connectors) / 数据连接器市场](https://llamahub.ai/)

---

## Files in This Example / 本示例文件说明

| File / 文件 | Description / 说明 |
|---|---|
| `README.md` | This guide / 本指南 |
| `document_qa.py` | Build a document Q&A system / 构建文档问答系统 |
| `test_llamaindex.py` | Tests that run without API keys / 无需 API 密钥的测试 |
