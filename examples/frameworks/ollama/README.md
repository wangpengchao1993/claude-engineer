# Ollama — Run LLMs Locally with One Command
# Ollama — 一行命令本地运行大模型

> Language: Go (Open Source) | License: MIT | GitHub Stars: ~120k
>
> Suitable for: Anyone who wants to run AI models locally / 适合人群：想在本地运行 AI 模型的所有人

## What is Ollama? / 什么是 Ollama？

Ollama is the easiest way to run open-source large language models (Llama, Mistral, Gemma, etc.) on your own computer. No cloud needed, no API keys, no costs. Think of it as **"Docker for AI models"** — one command to download and run any model.

Ollama 是在你自己电脑上运行开源大模型（Llama、Mistral、Gemma 等）最简单的方式。无需云服务、无需 API 密钥、无需花钱。你可以把它想象成 **"AI 模型的 Docker"**——一条命令即可下载并运行任何模型。

## When to Use / 什么时候用

- ✅ Privacy-sensitive data that cannot leave your machine / 隐私敏感数据不能离开本机
- ✅ Offline development without internet / 离线开发，无需联网
- ✅ Learning and experimenting with LLMs for free / 免费学习和体验大模型
- ✅ No API budget — everything runs locally / 没有 API 预算——一切本地运行
- ❌ Need the best quality responses (use Claude or GPT) / 需要最高质量回复（用 Claude 或 GPT）
- ❌ Production at scale with high throughput (use vLLM) / 大规模高吞吐生产环境（用 vLLM）
- ❌ Need to fine-tune models (use Hugging Face or Axolotl) / 需要微调模型（用 Hugging Face 或 Axolotl）

## Core Concepts / 核心概念

| Concept / 概念 | What it does / 作用 | Analogy / 类比 |
|----------------|---------------------|----------------|
| **Model** | The AI brain that generates text / 生成文本的 AI 大脑 | An app / 一个应用 |
| **Modelfile** | Config file defining a custom model / 定义自定义模型的配置文件 | Dockerfile / Dockerfile |
| **ollama serve** | Starts the local API server / 启动本地 API 服务 | Starting Docker daemon / 启动 Docker |
| **ollama run** | Download (if needed) and chat with a model / 下载并对话 | docker run / docker run |
| **ollama pull** | Download a model without running it / 只下载模型不运行 | docker pull / docker pull |
| **ollama list** | Show all downloaded models / 显示所有已下载的模型 | docker images / docker images |

## Supported Models / 支持的模型

| Model / 模型 | Size / 大小 | Best for / 最适合 |
|--------------|------------|-------------------|
| `llama3.1` | 4.7 GB | General chat, reasoning / 通用对话、推理 |
| `mistral` | 4.1 GB | Fast, good quality / 速度快、质量好 |
| `gemma2` | 5.4 GB | Google's open model / 谷歌开源模型 |
| `phi3` | 2.2 GB | Small but capable (Microsoft) / 小巧但强大（微软） |
| `codellama` | 3.8 GB | Code generation / 代码生成 |
| `llama3.2:1b` | 1.3 GB | Tiny, runs on any machine / 超小，任何机器都能跑 |

## Quick Start / 快速开始

### 1. Install Ollama / 安装 Ollama

```bash
# macOS / Linux — one-liner install / 一行安装
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com for Windows/macOS
# 或从 https://ollama.com 下载 Windows/macOS 安装包
```

### 2. Pull and run a model / 下载并运行模型

```bash
# Download and start chatting / 下载并开始对话
ollama run llama3.2

# Pull a model without chatting / 只下载不对话
ollama pull mistral

# List downloaded models / 列出已下载的模型
ollama list
```

### 3. Use with Python / 用 Python 调用

```bash
# Install the Python package / 安装 Python 包
pip install ollama

# Run the example / 运行示例
python local_chat.py
```

### Run Tests / 运行测试

```bash
pip install pytest
pytest test_ollama.py -v
```

## How It Works / 工作原理

```
┌─────────────────────────────────────────────────────────┐
│  Your Computer / 你的电脑                                │
│                                                         │
│  ┌─────────┐    REST API     ┌──────────────────────┐   │
│  │ Python  │ ──────────────> │ ollama serve         │   │
│  │ script  │  localhost:11434│ (manages models,     │   │
│  │ 脚本    │ <────────────── │  runs inference)     │   │
│  └─────────┘    JSON response│ (管理模型、运行推理)   │   │
│                              └──────────────────────┘   │
│                                      │                  │
│                              ┌───────┴──────┐           │
│                              │ Model files  │           │
│                              │ ~/.ollama/   │           │
│                              │ 模型文件      │           │
│                              └──────────────┘           │
└─────────────────────────────────────────────────────────┘
```

1. **`ollama serve`** starts a local REST API server on `localhost:11434` / 在本地 11434 端口启动 REST API 服务
2. **`ollama pull`** downloads model weights to `~/.ollama/models/` / 下载模型权重到本地目录
3. **Your code** sends HTTP requests (or uses the `ollama` Python package) / 你的代码发送 HTTP 请求（或使用 Python 包）
4. **Ollama** loads the model into memory, runs inference, returns the result / Ollama 将模型加载到内存，运行推理，返回结果

## Ollama vs vLLM / Ollama 与 vLLM 对比

| Feature / 特性 | Ollama | vLLM |
|----------------|--------|------|
| **Goal / 目标** | Simple local usage / 简单本地使用 | High-performance serving / 高性能服务 |
| **Setup / 安装** | One command / 一条命令 | Requires GPU setup / 需要 GPU 配置 |
| **Speed / 速度** | Good for single user / 单用户够用 | Optimized for many users / 多用户优化 |
| **Use case / 场景** | Dev, learning, privacy / 开发、学习、隐私 | Production APIs / 生产级 API |
| **GPU required? / 需要 GPU？** | No (CPU works) / 不需要（CPU 可用） | Yes (recommended) / 是（推荐） |

## Learn More / 了解更多

- [Ollama Official Website / 官网](https://ollama.com)
- [Ollama GitHub / GitHub 仓库](https://github.com/ollama/ollama)
- [Ollama Model Library / 模型库](https://ollama.com/library)
- [Ollama Python Package / Python 包](https://github.com/ollama/ollama-python)
- [Ollama API Docs / API 文档](https://github.com/ollama/ollama/blob/main/docs/api.md)
