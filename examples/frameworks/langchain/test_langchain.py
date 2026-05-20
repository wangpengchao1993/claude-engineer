"""
Tests for LangChain Examples / LangChain 示例测试

All tests run WITHOUT a real API key — we use unittest.mock to avoid real API calls.
所有测试无需真实 API 密钥运行——使用 unittest.mock 避免真实 API 调用。

Usage / 用法:
    pip install pytest langchain langchain-openai
    pytest test_langchain.py -v
"""

from unittest.mock import patch, MagicMock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def test_prompt_template_formatting():
    """Test that prompt templates correctly fill in variables / 测试提示词模板能正确填充变量"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a translator."),
        ("human", "Translate to {language}: {text}"),
    ])
    # Format the prompt with concrete values / 用具体值格式化提示词
    messages = prompt.format_messages(language="Chinese", text="Hello")
    assert len(messages) == 2
    assert "Chinese" in messages[1].content
    assert "Hello" in messages[1].content


def test_chain_is_runnable():
    """Test that LCEL chain creates a valid Runnable / 测试 LCEL 链创建有效的 Runnable"""
    from langchain_core.runnables import Runnable
    prompt = ChatPromptTemplate.from_template("Say {word}")
    parser = StrOutputParser()
    # Create a mock model that behaves like a Runnable / 创建一个模拟模型
    mock_model = MagicMock(spec=Runnable)
    mock_model.__or__ = MagicMock(return_value=MagicMock(spec=Runnable))
    chain = prompt | mock_model
    # The chain should be a Runnable / 链应该是一个 Runnable
    assert isinstance(chain, Runnable)


def test_output_parser():
    """Test StrOutputParser extracts text content / 测试 StrOutputParser 提取文本内容"""
    parser = StrOutputParser()
    # Simulate an AIMessage-like object / 模拟 AIMessage 对象
    from langchain_core.messages import AIMessage
    message = AIMessage(content="Hello World")
    result = parser.invoke(message)
    assert result == "Hello World"


def test_document_splitting():
    """Test that text splitter correctly chunks documents / 测试文本分割器能正确分块"""
    doc = Document(
        page_content="A" * 100 + " " + "B" * 100,  # ~201 chars with space / 约 201 个字符
        metadata={"source": "test"},
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=10)
    chunks = splitter.split_documents([doc])
    # Should split into at least 2 chunks / 应该分成至少 2 个块
    assert len(chunks) >= 2
    # Each chunk should preserve metadata / 每个块应保留元数据
    for chunk in chunks:
        assert chunk.metadata["source"] == "test"


def test_rag_chain_assembly():
    """Test that RAG chain can be assembled without API key / 测试 RAG 链能在无 API 密钥下组装"""
    from rag_example import simple_retriever, format_docs, chunks

    # Test retriever finds relevant docs / 测试检索器能找到相关文档
    results = simple_retriever("What is RAG?", chunks, top_k=2)
    assert len(results) <= 2
    assert all(isinstance(d, Document) for d in results)

    # Test format_docs joins content / 测试 format_docs 合并内容
    formatted = format_docs(results)
    assert isinstance(formatted, str)
    assert len(formatted) > 0


def test_simple_retriever_ranking():
    """Test retriever returns most relevant docs first / 测试检索器优先返回最相关文档"""
    from rag_example import simple_retriever
    docs = [
        Document(page_content="cats and dogs are pets"),
        Document(page_content="Python is a programming language"),
        Document(page_content="cats like to sleep all day"),
    ]
    results = simple_retriever("cats pets", docs, top_k=2)
    # The "cats and dogs" doc should rank highest (2 word overlap)
    # "cats and dogs" 文档应排名最高（2 个词重叠）
    assert "cats" in results[0].page_content
