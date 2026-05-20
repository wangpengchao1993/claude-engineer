"""
Basic LangChain Chain Example / LangChain 基础链示例

This script shows how to build simple chains using LangChain's
LCEL (LangChain Expression Language) — the pipe (|) syntax.

本脚本演示如何使用 LangChain 的 LCEL（LangChain 表达式语言）
——即管道符（|）语法——构建简单的链。

Usage / 用法:
    export OPENAI_API_KEY=sk-...
    python basic_chain.py
"""

# === Import required modules / 导入所需模块 ===
from langchain_openai import ChatOpenAI               # OpenAI chat model wrapper / OpenAI 聊天模型封装
from langchain_core.prompts import ChatPromptTemplate  # Prompt template / 提示词模板
from langchain_core.output_parsers import StrOutputParser  # String output parser / 字符串输出解析器


def build_translation_chain():
    """
    Build a simple translation chain / 构建一个简单的翻译链

    Chain structure / 链结构:
        prompt → model → parser
        (template formats input → LLM generates response → parser extracts text)
        (模板格式化输入 → 大模型生成回复 → 解析器提取文本)
    """
    # Step 1: Create the model / 第一步：创建模型
    # temperature=0 makes output deterministic / temperature=0 使输出更确定
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Step 2: Create a prompt template / 第二步：创建提示词模板
    # Variables in {curly braces} will be filled in later / {花括号}中的变量稍后填充
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional translator. / 你是一位专业翻译。"),
        ("human", "Translate the following text to {language}:\n\n{text}"),
    ])

    # Step 3: Create an output parser / 第三步：创建输出解析器
    # StrOutputParser extracts the string content from the model response
    # StrOutputParser 从模型回复中提取字符串内容
    parser = StrOutputParser()

    # Step 4: Chain them together with LCEL pipe syntax / 第四步：用 LCEL 管道语法串联
    # This reads as: prompt → model → parser (left to right)
    # 读作：提示词 → 模型 → 解析器（从左到右）
    chain = prompt | model | parser

    return chain


def build_summarize_then_translate_chain():
    """
    Build a multi-step chain: summarize, then translate / 构建多步链：先总结，再翻译

    This shows how to compose chains — the output of one feeds into the next.
    这展示了如何组合链——一个链的输出作为下一个链的输入。
    """
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    parser = StrOutputParser()

    # Chain 1: Summarize / 链 1：总结
    summarize_prompt = ChatPromptTemplate.from_template(
        "Summarize the following text in 1-2 sentences:\n\n{text}"
        # 用 1-2 句话总结以下文本
    )
    summarize_chain = summarize_prompt | model | parser

    # Chain 2: Translate the summary / 链 2：翻译总结内容
    translate_prompt = ChatPromptTemplate.from_template(
        "Translate the following English text to Chinese:\n\n{text}"
        # 将以下英文翻译成中文
    )
    translate_chain = translate_prompt | model | parser

    return summarize_chain, translate_chain


if __name__ == "__main__":
    # --- Demo 1: Simple translation / 演示 1：简单翻译 ---
    print("=== Translation Chain / 翻译链 ===\n")
    chain = build_translation_chain()
    result = chain.invoke({"language": "Chinese", "text": "Hello, how are you today?"})
    print(f"Result / 结果: {result}\n")

    # --- Demo 2: Summarize then translate / 演示 2：先总结后翻译 ---
    print("=== Summarize + Translate Chain / 总结+翻译链 ===\n")
    summarize_chain, translate_chain = build_summarize_then_translate_chain()
    article = (
        "LangChain is a framework for developing applications powered by "
        "large language models. It provides tools for prompt management, "
        "chain composition, data retrieval, and agent creation."
    )
    summary = summarize_chain.invoke({"text": article})
    print(f"Summary / 总结: {summary}")
    translation = translate_chain.invoke({"text": summary})
    print(f"Translation / 翻译: {translation}")
