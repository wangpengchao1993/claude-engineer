# AI Frameworks Guide — Your First Step into the AI Ecosystem
# AI 框架指南 — 进入 AI 生态的第一步

> A beginner-friendly, bilingual guide to the most popular AI/LLM frameworks in 2025-2026.
>
> 面向小白的双语 AI/LLM 框架指南（2025-2026 主流框架）。

---

## How to Use This Guide / 如何使用本指南

Each framework directory contains:
每个框架目录包含：

| File / 文件 | Purpose / 用途 |
|-------------|---------------|
| `README.md` | Framework introduction, concepts, and comparisons / 框架介绍、核心概念和对比 |
| `*.py` | Runnable example code with bilingual comments / 可运行的示例代码（双语注释） |
| `test_*.py` | Tests that work without API keys / 无需 API 密钥即可运行的测试 |

```bash
# Run any example / 运行任意示例
cd examples/frameworks/<framework>
pip install <dependencies>
python <example>.py

# Run tests / 运行测试
pytest test_*.py -v
```

---

## Framework Overview / 框架总览

### 1. LLM Application Frameworks / 大模型应用框架

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [LangChain](langchain/) | ~85k | Connect LLMs with tools, data, and memory / 将大模型与工具、数据、记忆连接 | Medium / 中等 |
| [LlamaIndex](llamaindex/) | ~35k | Build RAG apps over your data / 在你的数据上构建 RAG 应用 | Medium / 中等 |

### 2. Agent Frameworks / 智能体框架

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [CrewAI](crewai/) | ~25k | Create teams of AI agents / 创建 AI 智能体团队 | Easy / 简单 |
| [LangGraph](langgraph/) | — | Production-grade agent workflows as graphs / 生产级图结构 Agent 工作流 | Hard / 较难 |
| [OpenAI Agents SDK](openai-agents/) | — | OpenAI's official agent framework / OpenAI 官方 Agent 框架 | Medium / 中等 |

### 3. Prompt Optimization / 提示词优化

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [DSPy](dspy/) | ~23k | Automatically optimize prompts / 自动优化提示词 | Hard / 较难 |

### 4. Model Serving / 模型部署

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [Ollama](ollama/) | — | Run LLMs locally with one command / 一行命令本地运行大模型 | Easy / 简单 |
| [LiteLLM](litellm/) | — | One API for 100+ LLM providers / 一套接口调用 100+ 大模型 | Easy / 简单 |

### 5. Evaluation & Testing / 评估与测试

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [DeepEval](deepeval/) | — | Pytest for LLMs — test AI outputs / 大模型的 Pytest 测试框架 | Medium / 中等 |

### 6. Models & Fine-tuning / 模型与微调

| Framework / 框架 | Stars | What It Does / 用途 | Difficulty / 难度 |
|------------------|-------|--------------------|--------------------|
| [Hugging Face](huggingface/) | ~140k | The GitHub of AI — find and use any model / AI 界的 GitHub | Medium / 中等 |

---

## Learning Path for Beginners / 小白学习路径

```
Stage 1: Get Started / 入门阶段
├── Ollama         → Run your first local model / 跑起你的第一个本地模型
├── Hugging Face   → Understand models & tokenizers / 理解模型和分词器
└── LiteLLM        → Call different models with one API / 用一套 API 调用不同模型

Stage 2: Build Apps / 应用开发阶段
├── LangChain      → Build your first AI app / 构建你的第一个 AI 应用
├── LlamaIndex     → Add your own data (RAG) / 让 AI 读懂你的数据
└── DeepEval       → Test your AI outputs / 测试 AI 的输出质量

Stage 3: Build Agents / 智能体阶段
├── CrewAI          → Create a team of AI agents / 创建 AI 智能体团队
├── OpenAI Agents   → Use OpenAI's official agent SDK / 使用 OpenAI 官方 Agent SDK
└── LangGraph       → Production-grade agent workflows / 生产级 Agent 工作流

Stage 4: Advanced / 进阶阶段
└── DSPy            → Automatic prompt optimization / 自动提示词优化
```

---

## Quick Comparison / 快速对比

### "I want to..." / "我想要..."

| Goal / 目标 | Best Framework / 推荐框架 | Why / 原因 |
|-------------|--------------------------|-----------|
| Build a chatbot / 做聊天机器人 | LangChain | Best chain & memory support / 最好的链和记忆支持 |
| Q&A over documents / 文档问答 | LlamaIndex | RAG specialist / RAG 专家 |
| Multi-agent teamwork / 多 Agent 协作 | CrewAI | Easiest to start / 最容易上手 |
| Complex agent workflows / 复杂 Agent 流程 | LangGraph | Fine-grained control / 精细控制 |
| Run models locally / 本地跑模型 | Ollama | One command setup / 一行命令搞定 |
| Switch between models / 切换不同模型 | LiteLLM | Universal interface / 统一接口 |
| Test AI quality / 测试 AI 质量 | DeepEval | Pytest-like experience / 类似 Pytest 的体验 |
| Use open-source models / 用开源模型 | Hugging Face | Largest model hub / 最大的模型仓库 |
| Optimize prompts / 优化提示词 | DSPy | Automatic optimization / 自动优化 |

---

## Prerequisites / 环境要求

```bash
# Python 3.10+ recommended / 推荐 Python 3.10+
python --version

# Install frameworks as needed / 按需安装框架
pip install langchain langchain-openai    # LangChain
pip install llama-index                    # LlamaIndex
pip install crewai                         # CrewAI
pip install langgraph                      # LangGraph
pip install openai-agents                  # OpenAI Agents SDK
pip install dspy                           # DSPy
pip install ollama                         # Ollama Python client
pip install litellm                        # LiteLLM
pip install deepeval                       # DeepEval
pip install transformers torch             # Hugging Face

# Run tests (no API keys needed) / 运行测试（无需 API 密钥）
pip install pytest
pytest examples/frameworks/ -v
```

---

<p align="center">
  <sub>Part of <a href="../../README.md">claude-engineer</a> — contributions welcome! / 欢迎贡献！</sub>
</p>
