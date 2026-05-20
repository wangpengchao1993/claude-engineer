# LangChain — The Most Popular LLM Application Framework
# LangChain — 最流行的大模型应用开发框架

> ⭐ GitHub Stars: ~85k | Language: Python / TypeScript | License: MIT
>
> 适合人群：AI 应用开发初学者 / Suitable for: Beginners in AI app development

## What is LangChain? / 什么是 LangChain？

LangChain is an open-source framework for building applications powered by large language models (LLMs). Think of it as "LEGO blocks for AI" — you can snap together different components (models, tools, data sources, memory) to build complex AI applications without writing everything from scratch.

LangChain 是一个用于构建大模型应用的开源框架。你可以把它想象成"AI 的乐高积木"——将不同的组件（模型、工具、数据源、记忆）拼接在一起，无需从零开始就能构建复杂的 AI 应用。

## When to Use / 什么时候用

- ✅ Building chatbots with memory / 构建带记忆的聊天机器人
- ✅ Creating RAG (Retrieval-Augmented Generation) apps / 创建 RAG 检索增强生成应用
- ✅ Connecting LLMs to external tools and APIs / 将大模型连接到外部工具和 API
- ✅ Prototyping AI features quickly / 快速原型开发 AI 功能
- ❌ Simple one-shot API calls (use the API directly) / 简单的单次 API 调用（直接用 API 更好）
- ❌ Fine-tuning models (use Hugging Face instead) / 微调模型（用 Hugging Face）

## Key Concepts / 核心概念

| Concept / 概念 | What it does / 作用 | Analogy / 类比 |
|----------------|---------------------|----------------|
| **Model** | The AI brain (GPT, Claude, etc.) / AI 大脑 | The chef / 厨师 |
| **Prompt Template** | Reusable instruction format / 可复用的指令模板 | The recipe / 菜谱 |
| **Chain** | Multiple steps linked together / 多步骤串联 | Assembly line / 流水线 |
| **Tool** | External capability (search, calculator) / 外部能力 | Kitchen appliances / 厨房工具 |
| **Memory** | Conversation history / 对话历史 | Notebook / 笔记本 |
| **Retriever** | Fetches relevant documents / 获取相关文档 | Librarian / 图书管理员 |

## Quick Start / 快速开始

### Install / 安装
```bash
pip install langchain langchain-openai
```

### Run Examples / 运行示例
```bash
# Set your API key / 设置 API 密钥
export OPENAI_API_KEY=sk-...

# Run basic chain / 运行基础链
python basic_chain.py

# Run RAG example / 运行 RAG 示例
python rag_example.py
```

### Run Tests / 运行测试
```bash
pip install pytest
pytest test_langchain.py -v
```

## How It Works / 工作原理

```
User Input / 用户输入
      │
      ▼
┌─────────────┐
│ Prompt       │  ← Template formats the input / 模板格式化输入
│ Template     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ LLM /        │  ← Model processes the prompt / 模型处理提示词
│ Chat Model   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Output       │  ← Parser structures the response / 解析器结构化输出
│ Parser       │
└──────┬──────┘
       │
       ▼
  Final Result / 最终结果
```

## Comparison with Other Frameworks / 与其他框架对比

| Feature / 特性 | LangChain | LlamaIndex | Direct API / 直接 API |
|----------------|-----------|------------|----------------------|
| Learning curve / 学习曲线 | Medium / 中等 | Medium / 中等 | Easy / 简单 |
| RAG support / RAG 支持 | Good / 好 | Best / 最好 | Manual / 手动 |
| Agent support / Agent 支持 | Great / 很好 | Basic / 基础 | Manual / 手动 |
| Community / 社区 | Largest / 最大 | Large / 大 | N/A |
| Flexibility / 灵活性 | High / 高 | Medium / 中等 | Highest / 最高 |

## Learn More / 延伸阅读

- [Official Docs / 官方文档](https://python.langchain.com/docs/get_started/introduction)
- [GitHub](https://github.com/langchain-ai/langchain)
- [LangChain Cookbook / 食谱](https://github.com/langchain-ai/langchain/tree/master/cookbook)
