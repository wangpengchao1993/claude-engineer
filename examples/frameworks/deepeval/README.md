# DeepEval -- Pytest for LLMs / 大模型的 Pytest 测试框架

**Language / 语言:** Python
**License / 许可证:** MIT
**GitHub:** [confident-ai/deepeval](https://github.com/confident-ai/deepeval)

---

## What is DeepEval? / 什么是 DeepEval？

DeepEval is an evaluation framework that lets you **test LLM outputs like you test code with pytest**.
Think of it as "unit testing for AI" -- you define what good output looks like,
and DeepEval checks if your LLM meets the bar.

DeepEval 是一个评估框架，让你能够**像用 pytest 测试代码一样测试大模型的输出**。
你可以把它理解为"AI 的单元测试"——你定义什么算好的输出，DeepEval 帮你检查大模型是否达标。

```
Your LLM output  -->  DeepEval metrics  -->  Pass / Fail
你的大模型输出   -->  DeepEval 指标      -->  通过 / 不通过
```

---

## When to Use / 适用场景

| Use Case / 场景 | Example / 例子 |
|---|---|
| Testing RAG quality / 测试 RAG 质量 | Check if retrieved context is actually used in the answer / 检查检索到的上下文是否真正用在了回答中 |
| Detecting hallucinations / 检测幻觉 | Verify the model doesn't make things up / 验证模型没有编造内容 |
| Measuring answer relevance / 衡量回答相关性 | Ensure the answer addresses the question / 确保回答切题 |
| CI/CD for AI / AI 的持续集成 | Run evaluations automatically on every code change / 每次代码变更自动运行评估 |

## When NOT to Use / 不适用场景

| Scenario / 场景 | Use Instead / 应该用 |
|---|---|
| Testing traditional code / 测试传统代码 | pytest, unittest |
| Model training evaluation / 模型训练评估 | MLflow, Weights & Biases |
| Real-time monitoring / 实时监控 | LangSmith, Arize, Helicone |

---

## Core Concepts / 核心概念

DeepEval has four building blocks. Master these and you understand the whole framework.

DeepEval 有四个基本构件。掌握它们，你就理解了整个框架。

### 1. Test Case / 测试用例

A single input-output pair to evaluate. Like a unit test for your LLM.

一个用于评估的输入-输出对。就像大模型的一个单元测试。

```python
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is Python?",              # The question / 问题
    actual_output="Python is a snake.",    # What the LLM said / 大模型的回答
    expected_output="Python is a programming language.",  # Ideal answer / 理想回答
    context=["Python is a high-level programming language."],  # RAG context / 检索上下文
)
```

### 2. Metric / 评估指标

An evaluation criterion with a threshold. If the score >= threshold, the test passes.

一个带阈值的评估标准。如果得分 >= 阈值，测试就通过。

```python
from deepeval.metrics import AnswerRelevancyMetric

metric = AnswerRelevancyMetric(threshold=0.7)  # Must score >= 0.7 to pass
```

### 3. Dataset / 数据集

A collection of test cases. Useful for bulk evaluation.

测试用例的集合。用于批量评估。

```python
from deepeval.dataset import EvaluationDataset

dataset = EvaluationDataset(test_cases=[case1, case2, case3])
```

### 4. Assert / 断言

The pass/fail check -- just like `assert` in pytest.

通过/不通过的检查——就像 pytest 里的 `assert`。

```python
from deepeval import assert_test

assert_test(test_case, metrics=[metric])  # Raises if metric fails / 如果指标不通过就抛异常
```

---

## Built-in Metrics / 内置指标

DeepEval ships with many metrics out of the box. Here are the most commonly used ones.

DeepEval 自带许多开箱即用的指标。以下是最常用的。

| Metric / 指标 | What it Measures / 衡量什么 | Needs Context? / 需要上下文？ |
|---|---|---|
| **AnswerRelevancy** | Is the answer relevant to the question? / 回答是否与问题相关？ | No / 否 |
| **Faithfulness** | Is the answer faithful to the given context? / 回答是否忠于给定的上下文？ | Yes / 是 |
| **Hallucination** | Does the answer contain made-up information? / 回答是否包含编造的信息？ | Yes / 是 |
| **Bias** | Does the answer show unfair bias? / 回答是否存在不公平的偏见？ | No / 否 |
| **Toxicity** | Does the answer contain toxic content? / 回答是否包含有害内容？ | No / 否 |
| **ContextualRelevancy** | Is the retrieved context relevant? / 检索到的上下文是否相关？ | Yes / 是 |
| **ContextualPrecision** | How precise is the retrieved context? / 检索上下文的精确度如何？ | Yes / 是 |
| **ContextualRecall** | Does the context cover the expected answer? / 上下文是否覆盖了预期回答？ | Yes / 是 |
| **Summarization** | Is the summary accurate and complete? / 摘要是否准确完整？ | No / 否 |
| **GEval** | Custom criteria (you define them) / 自定义标准（你来定义） | Optional / 可选 |

---

## Quick Start / 快速开始

```bash
# Install / 安装
pip install deepeval

# (Optional) Log in to Confident AI dashboard / （可选）登录 Confident AI 仪表板
deepeval login

# Run tests with pytest / 用 pytest 运行测试
deepeval test run test_example.py

# Or just use pytest directly / 或者直接用 pytest
pytest test_example.py
```

---

## How It Works / 工作流程

```
Step 1: Define test cases     -->  What inputs/outputs to evaluate
步骤1：定义测试用例            -->  要评估哪些输入/输出

Step 2: Choose metrics         -->  What criteria to check
步骤2：选择指标                -->  要检查哪些标准

Step 3: Run evaluation         -->  DeepEval scores each case
步骤3：运行评估                -->  DeepEval 为每个用例打分

Step 4: Get results            -->  Pass/Fail + detailed scores
步骤4：获取结果                -->  通过/不通过 + 详细分数
```

A minimal working example / 一个最小的可运行示例：

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def test_my_llm():
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="The capital of France is Paris.",
    )
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, metrics=[metric])
```

---

## DeepEval vs RAGAS / DeepEval 与 RAGAS 对比

Both are popular LLM evaluation tools. Here is how they compare.

两者都是流行的大模型评估工具。以下是它们的对比。

| Aspect / 方面 | DeepEval | RAGAS |
|---|---|---|
| **Interface / 接口** | pytest-native (feels like writing tests) / 原生 pytest（像写测试一样） | Standalone library / 独立库 |
| **CI/CD integration / CI/CD 集成** | First-class (just run pytest) / 一等支持（直接跑 pytest） | Requires extra setup / 需要额外配置 |
| **Metrics / 指标** | 10+ built-in, custom via GEval / 10+ 内置，可用 GEval 自定义 | Focus on RAG metrics / 聚焦 RAG 指标 |
| **Dashboard / 仪表板** | Confident AI (cloud) / Confident AI（云端） | No official dashboard / 无官方仪表板 |
| **RAG focus / RAG 聚焦** | General LLM + RAG / 通用大模型 + RAG | Primarily RAG / 主要面向 RAG |
| **Learning curve / 学习曲线** | Low (if you know pytest) / 低（如果你会 pytest） | Low / 低 |

**Rule of thumb / 经验法则：**
- Need pytest-style CI/CD testing? --> DeepEval / 需要 pytest 风格的 CI/CD 测试？--> DeepEval
- Only evaluating RAG pipelines in notebooks? --> RAGAS / 只在 notebook 中评估 RAG 管道？--> RAGAS

---

## Learn More / 了解更多

- [DeepEval Documentation / 官方文档](https://docs.confident-ai.com/)
- [GitHub Repository / GitHub 仓库](https://github.com/confident-ai/deepeval)
- [Confident AI Dashboard / Confident AI 仪表板](https://app.confident-ai.com/)
- [DeepEval Metrics Guide / 指标指南](https://docs.confident-ai.com/docs/metrics-introduction)
- [Getting Started Tutorial / 入门教程](https://docs.confident-ai.com/docs/getting-started)
