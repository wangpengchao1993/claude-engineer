"""
RAG (Retrieval-Augmented Generation) Example / RAG 检索增强生成示例

RAG = Retrieve relevant documents + feed them to the LLM as context.
This lets the model answer questions about YOUR data, not just its training data.

RAG = 检索相关文档 + 将其作为上下文传给大模型。
这样模型就能回答关于"你的数据"的问题，而不仅仅依赖训练数据。

Usage / 用法:
    export OPENAI_API_KEY=sk-...
    python rag_example.py
"""

# === Imports / 导入 ===
from langchain_core.documents import Document                  # Document container / 文档容器
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Text splitter / 文本分割器
from langchain_core.prompts import ChatPromptTemplate          # Prompt template / 提示词模板
from langchain_core.output_parsers import StrOutputParser      # Output parser / 输出解析器
from langchain_core.runnables import RunnablePassthrough        # Passthrough helper / 透传辅助
from langchain_openai import ChatOpenAI                        # Chat model / 聊天模型


# === Step 1: Create sample documents / 第一步：创建示例文档 ===
# In real apps, you'd load these from files, databases, or URLs.
# 在实际应用中，你会从文件、数据库或 URL 加载这些内容。
documents = [
    Document(page_content=(
        "Python was created by Guido van Rossum and first released in 1991. "
        "It emphasizes code readability and supports multiple programming paradigms."
        # Python 由 Guido van Rossum 创建，1991 年首次发布。
    ), metadata={"source": "python_intro"}),
    Document(page_content=(
        "LangChain is a framework for building LLM-powered applications. "
        "It was created by Harrison Chase in October 2022. "
        "Key features include chains, agents, and retrieval capabilities."
        # LangChain 是构建大模型应用的框架，由 Harrison Chase 于 2022 年 10 月创建。
    ), metadata={"source": "langchain_intro"}),
    Document(page_content=(
        "RAG stands for Retrieval-Augmented Generation. It combines a retriever "
        "that fetches relevant documents with a generator (LLM) that produces answers. "
        "This reduces hallucination and keeps answers grounded in real data."
        # RAG 即检索增强生成，结合检索器获取相关文档和生成器（大模型）产出答案。
    ), metadata={"source": "rag_explanation"}),
]


# === Step 2: Split documents into chunks / 第二步：将文档分割成小块 ===
# Smaller chunks help the retriever find more precise matches.
# 更小的块帮助检索器找到更精确的匹配。
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,        # Max characters per chunk / 每块最大字符数
    chunk_overlap=30,      # Overlap between chunks to preserve context / 块之间的重叠以保留上下文
)
chunks = splitter.split_documents(documents)


# === Step 3: Build a simple keyword retriever / 第三步：构建简单的关键词检索器 ===
# This is a minimal retriever that searches by keyword overlap.
# No vector DB or embeddings needed — perfect for learning!
# 这是一个按关键词重叠搜索的最小检索器，无需向量数据库或嵌入模型，非常适合学习！

def simple_retriever(query: str, docs: list[Document] = chunks, top_k: int = 2) -> list[Document]:
    """
    Retrieve documents by keyword overlap / 通过关键词重叠检索文档

    For production, use a vector store (FAISS, Chroma, Pinecone, etc.)
    生产环境请使用向量数据库（FAISS、Chroma、Pinecone 等）
    """
    query_words = set(query.lower().split())
    scored = []
    for doc in docs:
        doc_words = set(doc.page_content.lower().split())
        # Count how many query words appear in the document / 计算查询词在文档中出现的数量
        overlap = len(query_words & doc_words)
        scored.append((overlap, doc))
    # Sort by score (descending) and return top results / 按分数降序排序，返回前几个结果
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def format_docs(docs: list[Document]) -> str:
    """Join document contents into a single string / 将文档内容合并为一个字符串"""
    return "\n\n".join(doc.page_content for doc in docs)


# === Step 4: Build the RAG chain / 第四步：构建 RAG 链 ===
def build_rag_chain():
    """
    Build the full RAG pipeline / 构建完整的 RAG 管道

    Flow / 流程:
        question → retriever → format docs ─┐
        question ─────────────────────────────┤→ prompt → model → parser
                                              │
        (context + question fed to prompt)
        (上下文 + 问题一起传入提示词模板)
    """
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # The prompt tells the model to answer ONLY from the provided context
    # 提示词要求模型只根据提供的上下文来回答
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based only on the following context. "
        "If you cannot find the answer, say 'I don't know'.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
        # 仅根据以下上下文回答问题。如果找不到答案，请说"我不知道"。
    )

    # Build the chain using LCEL / 使用 LCEL 构建链
    chain = (
        {
            # Retrieve and format relevant docs / 检索并格式化相关文档
            "context": lambda x: format_docs(simple_retriever(x["question"])),
            # Pass the question through unchanged / 将问题原样传递
            "question": RunnablePassthrough() | (lambda x: x["question"]),
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain


if __name__ == "__main__":
    print("=== RAG Example / RAG 示例 ===\n")
    print(f"Total chunks after splitting / 分割后总块数: {len(chunks)}\n")

    # Demo: Ask a question / 演示：提问
    rag_chain = build_rag_chain()
    question = "What is RAG and why is it useful?"
    print(f"Question / 问题: {question}")
    answer = rag_chain.invoke({"question": question})
    print(f"Answer / 回答: {answer}")
