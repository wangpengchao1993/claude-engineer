# DSPy — Automatic Prompt Optimization Framework
# DSPy — 自动提示词优化框架

> ⭐ GitHub Stars: ~23k | Language: Python | License: MIT
>
> 适合人群：希望系统化优化提示词的开发者 / Suitable for: Developers who want to optimize prompts systematically

## What is DSPy? / 什么是 DSPy？

DSPy is a framework that **automatically optimizes prompts and LLM pipelines**. Instead of manually writing and tweaking prompts, you define what you want (input/output signature), provide training examples, and DSPy **learns the best prompt for you**. Think of it as "machine learning for prompts" — you provide data and a metric, and the optimizer finds the best way to instruct the LLM.

DSPy 是一个**自动优化提示词和大模型流水线**的框架。你不需要手动编写和调整提示词，只需定义你想要什么（输入/输出签名），提供训练样本，DSPy 就会**自动学习最佳提示词**。可以把它理解为"提示词的机器学习"——你提供数据和评估指标，优化器会找到指导大模型的最佳方式。

## When to Use / 什么时候用

- ✅ Optimizing prompt quality systematically / 系统化地优化提示词质量
- ✅ Building pipelines that need consistent, reliable outputs / 构建需要稳定可靠输出的流水线
- ✅ Research and evaluation of LLM performance / 大模型性能的研究和评估
- ✅ Multi-step reasoning tasks (QA, classification, summarization) / 多步推理任务（问答、分类、摘要）
- ❌ One-off prompts (just write them directly) / 一次性的提示词（直接手写更快）
- ❌ When you need full control over exact prompt text / 需要完全控制提示词原文时
- ❌ Simple tasks where manual prompts already work well / 手动提示词已经够用的简单任务

## Key Concepts / 核心概念

| Concept / 概念 | What it does / 作用 | Analogy / 类比 |
|----------------|---------------------|----------------|
| **Signature** | Defines input→output spec / 定义输入→输出规格 | Function type hint / 函数类型标注 |
| **Module** | Wraps a prompting strategy / 封装一种提示策略 | `nn.Module` in PyTorch / PyTorch 中的 `nn.Module` |
| **Optimizer** | Learns the best prompts from data / 从数据中学习最佳提示词 | Training loop / 训练循环 |
| **Metric** | Evaluates output quality / 评估输出质量 | Loss function / 损失函数 |

## Quick Start / 快速开始

### Install / 安装
```bash
pip install dspy
```

### Run Examples / 运行示例
```bash
# Set your API key / 设置 API 密钥
export OPENAI_API_KEY=sk-...

# Run classification example / 运行分类示例
python classify_example.py
```

### Run Tests (no API key needed) / 运行测试（无需 API 密钥）
```bash
pip install pytest
pytest test_dspy.py -v
```

## How It Works / 工作原理

```
Step 1: Define Signature    →  "text -> category, confidence"
        定义签名                 （输入文本 → 输出类别和置信度）

Step 2: Build Module        →  Use Predict or ChainOfThought
        构建模块                 （使用 Predict 或 ChainOfThought）

Step 3: Provide Examples    →  Training data with correct outputs
        提供样本                 （带正确输出的训练数据）

Step 4: Optimize            →  DSPy tries different prompts, picks the best
        优化                     （DSPy 尝试不同提示词，选出最佳）

Step 5: Deploy              →  Use the optimized module in production
        部署                     （在生产环境中使用优化后的模块）
```

## DSPy vs Manual Prompt Engineering / DSPy 与手动提示词工程对比

| Aspect / 方面 | Manual / 手动 | DSPy |
|---------------|--------------|------|
| **Prompt writing** / 编写提示词 | You write every word / 你写每一个字 | You define the structure, DSPy writes the prompt / 你定义结构，DSPy 编写提示词 |
| **Iteration** / 迭代 | Trial and error / 反复试错 | Automated optimization / 自动优化 |
| **Reproducibility** / 可复现性 | Hard to track changes / 难以追踪变更 | Version-controlled pipeline / 版本控制的流水线 |
| **Scaling** / 扩展性 | Rewrite for each task / 每个任务重写 | Reuse modules, re-optimize / 复用模块，重新优化 |

## Learn More / 了解更多

- [DSPy GitHub Repository / GitHub 仓库](https://github.com/stanfordnlp/dspy)
- [DSPy Documentation / 官方文档](https://dspy-docs.vercel.app/)
- [DSPy Paper / 论文](https://arxiv.org/abs/2310.03714)
- [Stanford NLP Group / 斯坦福 NLP 组](https://nlp.stanford.edu/)
