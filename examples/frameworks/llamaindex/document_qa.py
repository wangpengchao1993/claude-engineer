"""
LlamaIndex Document Q&A Example / LlamaIndex 文档问答示例
=========================================================

This script demonstrates how to:
本脚本演示如何：

1. Create documents manually (a small knowledge base)
   手动创建文档（一个小型知识库）
2. Build a VectorStoreIndex from those documents
   从文档构建向量存储索引
3. Create a query engine to ask questions
   创建查询引擎进行提问
4. Customize the query prompt
   自定义查询提示词

Prerequisites / 前置条件:
    pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai
    export OPENAI_API_KEY="sk-..."
"""

from llama_index.core import Document, VectorStoreIndex, Settings

# ---------------------------------------------------------------------------
# Step 1: Create documents -- our fictional company knowledge base
# 第一步：创建文档 -- 我们虚构公司的知识库
# ---------------------------------------------------------------------------
# Each Document is like one page of information the AI can reference.
# 每个 Document 就像 AI 可以参考的一页信息。

documents = [
    Document(
        text=(
            "SkyPet Inc. was founded in 2021 by Alice Zhang and Bob Smith. "
            "The company is headquartered in San Francisco, California. "
            "SkyPet builds AI-powered pet health monitoring devices."
        ),
        metadata={"source": "company_overview", "topic": "general"},
    ),
    Document(
        text=(
            "SkyPet's flagship product is the PetBand, a smart collar that "
            "tracks heart rate, activity level, and sleep patterns for dogs "
            "and cats. It costs $99 and has sold over 500,000 units worldwide."
        ),
        metadata={"source": "product_catalog", "topic": "products"},
    ),
    Document(
        text=(
            "SkyPet raised $15 million in Series A funding in March 2023, "
            "led by TechVentures Capital. The company plans to use the funds "
            "to expand into European and Asian markets in 2024."
        ),
        metadata={"source": "press_release", "topic": "funding"},
    ),
    Document(
        text=(
            "SkyPet currently has 120 employees. The engineering team makes up "
            "about 60% of the workforce. The company offers remote work options "
            "and has offices in San Francisco and Austin, Texas."
        ),
        metadata={"source": "hr_handbook", "topic": "team"},
    ),
]

print("Created %d documents / 已创建 %d 个文档" % (len(documents), len(documents)))

# ---------------------------------------------------------------------------
# Step 2: Build an index from the documents
# 第二步：从文档构建索引
# ---------------------------------------------------------------------------
# VectorStoreIndex converts each document into an embedding (a list of numbers)
# and stores them so we can quickly find relevant documents later.
# VectorStoreIndex 将每个文档转换为嵌入向量（一组数字），并存储起来以便后续快速查找。

# NOTE: This step requires an embedding model. By default it uses OpenAI.
# 注意：此步骤需要嵌入模型，默认使用 OpenAI。
index = VectorStoreIndex.from_documents(documents)

print("Index built successfully! / 索引构建成功！")
print(
    "The index contains %d nodes. / 索引包含 %d 个节点。"
    % (len(index.docstore.docs), len(index.docstore.docs))
)

# ---------------------------------------------------------------------------
# Step 3: Create a query engine and ask questions
# 第三步：创建查询引擎并提问
# ---------------------------------------------------------------------------
# The query engine = Retriever (finds relevant docs) + LLM (generates answer).
# 查询引擎 = 检索器（找到相关文档） + LLM（生成回答）。

query_engine = index.as_query_engine()

# Ask our first question / 提出第一个问题
question_1 = "Who founded SkyPet and where is it located?"
print("\n--- Question 1 / 问题 1 ---")
print("Q:", question_1)
response_1 = query_engine.query(question_1)
print("A:", response_1)

# Ask about the product / 询问产品信息
question_2 = "What is the PetBand and how much does it cost?"
print("\n--- Question 2 / 问题 2 ---")
print("Q:", question_2)
response_2 = query_engine.query(question_2)
print("A:", response_2)

# Ask about funding / 询问融资信息
question_3 = "How much funding has SkyPet raised?"
print("\n--- Question 3 / 问题 3 ---")
print("Q:", question_3)
response_3 = query_engine.query(question_3)
print("A:", response_3)

# ---------------------------------------------------------------------------
# Step 4: Customize the query prompt (optional, but powerful!)
# 第四步：自定义查询提示词（可选，但很强大！）
# ---------------------------------------------------------------------------
# You can tell the LLM *how* to answer by providing a custom prompt template.
# 你可以通过自定义提示词模板来告诉 LLM *如何*回答问题。

from llama_index.core import PromptTemplate

# A custom prompt that asks for concise, bullet-point answers
# 自定义提示词，要求简洁的要点式回答
custom_prompt = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context above, answer the question in 2-3 bullet points.\n"
    "If you don't know, say 'I don't have enough information.'\n"
    "Question: {query_str}\n"
    "Answer: "
)

# Create a new query engine with the custom prompt
# 使用自定义提示词创建新的查询引擎
custom_query_engine = index.as_query_engine(text_qa_template=custom_prompt)

question_4 = "Tell me about SkyPet's team and offices."
print("\n--- Question 4 (Custom Prompt) / 问题 4（自定义提示词） ---")
print("Q:", question_4)
response_4 = custom_query_engine.query(question_4)
print("A:", response_4)

print("\n--- Done! / 完成！---")
print(
    "You just built a document Q&A system with LlamaIndex!\n"
    "你刚刚用 LlamaIndex 构建了一个文档问答系统！"
)
