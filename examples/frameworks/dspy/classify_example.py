"""
DSPy Sentiment Classification Example / DSPy 情感分类示例

This script shows how to use DSPy to classify text sentiment.
Instead of writing a prompt manually, we define a Signature
(what we want) and let DSPy handle the prompting.

本脚本演示如何使用 DSPy 对文本进行情感分类。
我们不手动编写提示词，而是定义一个签名（Signature）
来描述我们想要什么，让 DSPy 处理提示词生成。

Usage / 用法:
    export OPENAI_API_KEY=sk-...
    python classify_example.py
"""

import dspy
from dspy import Signature, InputField, OutputField, Predict, ChainOfThought


# === Step 1: Define the Signature / 第一步：定义签名 ===
# A Signature tells DSPy the input and output fields.
# Think of it like a function type hint: text -> (category, confidence)
# 签名告诉 DSPy 输入和输出字段。
# 可以把它想象成函数的类型标注：text -> (category, confidence)

class SentimentClassify(Signature):
    """Classify the sentiment of a given text. / 对给定文本进行情感分类。"""

    # Input field: the text to classify / 输入字段：要分类的文本
    text = InputField(desc="The text to classify / 要分类的文本")

    # Output fields: category and confidence / 输出字段：类别和置信度
    category = OutputField(desc="One of: positive, negative, neutral / 三选一：positive, negative, neutral")
    confidence = OutputField(desc="Confidence score from 0.0 to 1.0 / 置信度评分，0.0 到 1.0")


# === Step 2: Build Modules / 第二步：构建模块 ===
# Predict = simple one-shot prediction / 简单的一次性预测
# ChainOfThought = adds reasoning steps before answering (usually better)
# ChainOfThought = 先推理再回答（通常效果更好）

simple_classifier = Predict(SentimentClassify)
cot_classifier = ChainOfThought(SentimentClassify)


# === Step 3: Configure the LLM / 第三步：配置大模型 ===
def setup_lm():
    """
    Configure which LLM to use / 配置使用哪个大模型

    DSPy supports many providers: OpenAI, Anthropic, local models, etc.
    DSPy 支持多种供应商：OpenAI、Anthropic、本地模型等。
    """
    lm = dspy.LM("openai/gpt-4o-mini", temperature=0.0)
    dspy.configure(lm=lm)


# === Step 4: Run classification / 第四步：运行分类 ===
def classify_texts():
    """
    Classify example texts using both Predict and ChainOfThought.
    用 Predict 和 ChainOfThought 两种方式分类示例文本。
    """
    # Example texts to classify / 要分类的示例文本
    examples = [
        "This product is absolutely amazing! Best purchase I've ever made.",
        "The service was terrible and the food was cold.",
        "The package arrived on Tuesday as scheduled.",
    ]

    print("=" * 60)
    print("Simple Predict / 简单预测")
    print("=" * 60)

    for text in examples:
        result = simple_classifier(text=text)
        print(f"\nText / 文本: {text[:50]}...")
        print(f"  Category / 类别: {result.category}")
        print(f"  Confidence / 置信度: {result.confidence}")

    print("\n" + "=" * 60)
    print("ChainOfThought (with reasoning) / 思维链（带推理过程）")
    print("=" * 60)

    for text in examples:
        result = cot_classifier(text=text)
        print(f"\nText / 文本: {text[:50]}...")
        print(f"  Reasoning / 推理: {result.reasoning[:80]}...")
        print(f"  Category / 类别: {result.category}")
        print(f"  Confidence / 置信度: {result.confidence}")


if __name__ == "__main__":
    setup_lm()
    classify_texts()

    # Show what DSPy generated behind the scenes / 展示 DSPy 在幕后生成的内容
    print("\n" + "=" * 60)
    print("Inspecting the prompt DSPy built / 查看 DSPy 构建的提示词")
    print("=" * 60)
    # The LM history shows the actual prompts sent / LM 历史记录显示实际发送的提示词
    print(dspy.inspect_history(n=1))
