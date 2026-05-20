"""
Tests for LlamaIndex basics (no API key needed!)
LlamaIndex 基础测试（不需要 API 密钥！）

Run with / 运行方式:
    pytest test_llamaindex.py -v
"""

from unittest.mock import MagicMock, patch

import pytest

from llama_index.core import Document
from llama_index.core.schema import TextNode


# ---------------------------------------------------------------------------
# Test 1: Document creation / 测试 1：文档创建
# ---------------------------------------------------------------------------
class TestDocument:
    """Test that we can create and inspect Document objects.
    测试我们能否创建和检查 Document 对象。"""

    def test_create_document_with_text(self):
        """A Document should store its text content.
        Document 应该存储其文本内容。"""
        doc = Document(text="Hello, LlamaIndex!")
        assert doc.text == "Hello, LlamaIndex!"

    def test_create_document_with_metadata(self):
        """A Document can carry metadata (source, author, etc.).
        Document 可以携带元数据（来源、作者等）。"""
        doc = Document(
            text="Some content",
            metadata={"source": "test", "author": "Alice"},
        )
        assert doc.metadata["source"] == "test"
        assert doc.metadata["author"] == "Alice"

    def test_document_has_unique_id(self):
        """Each Document gets a unique ID automatically.
        每个 Document 会自动获得一个唯一 ID。"""
        doc_a = Document(text="First")
        doc_b = Document(text="Second")
        assert doc_a.doc_id != doc_b.doc_id


# ---------------------------------------------------------------------------
# Test 2: Node parsing / 测试 2：节点解析
# ---------------------------------------------------------------------------
class TestNodeParsing:
    """Test that documents can be split into smaller nodes (chunks).
    测试文档能否被切分为更小的节点（片段）。"""

    def test_create_text_node(self):
        """A TextNode holds a chunk of text with metadata.
        TextNode 持有一段带元数据的文本片段。"""
        node = TextNode(text="This is a chunk.", metadata={"page": 1})
        assert node.text == "This is a chunk."
        assert node.metadata["page"] == 1

    def test_node_has_unique_id(self):
        """Each Node gets its own unique identifier.
        每个 Node 都有自己的唯一标识符。"""
        node_a = TextNode(text="Chunk A")
        node_b = TextNode(text="Chunk B")
        assert node_a.node_id != node_b.node_id


# ---------------------------------------------------------------------------
# Test 3: Index construction with mock embeddings
# 测试 3：使用模拟嵌入构建索引
# ---------------------------------------------------------------------------
class TestIndexConstruction:
    """Test index building without calling a real embedding API.
    测试在不调用真实嵌入 API 的情况下构建索引。"""

    @patch("llama_index.core.VectorStoreIndex.from_documents")
    def test_index_from_documents(self, mock_from_docs):
        """VectorStoreIndex.from_documents should accept a list of Documents.
        VectorStoreIndex.from_documents 应该接受一个 Document 列表。"""
        mock_index = MagicMock()
        mock_from_docs.return_value = mock_index

        from llama_index.core import VectorStoreIndex

        docs = [
            Document(text="Doc one"),
            Document(text="Doc two"),
        ]
        index = VectorStoreIndex.from_documents(docs)

        # Verify from_documents was called with our docs
        # 验证 from_documents 被调用时传入了我们的文档
        mock_from_docs.assert_called_once_with(docs)
        assert index is mock_index


# ---------------------------------------------------------------------------
# Test 4: Query engine creation / 测试 4：查询引擎创建
# ---------------------------------------------------------------------------
class TestQueryEngine:
    """Test that a query engine can be created from an index.
    测试能否从索引创建查询引擎。"""

    def test_query_engine_from_mock_index(self):
        """Calling index.as_query_engine() should return a query engine.
        调用 index.as_query_engine() 应返回一个查询引擎。"""
        mock_index = MagicMock()
        mock_engine = MagicMock()
        mock_index.as_query_engine.return_value = mock_engine

        engine = mock_index.as_query_engine()

        # The engine should be what the index returned
        # 引擎应该是索引返回的对象
        assert engine is mock_engine
        mock_index.as_query_engine.assert_called_once()

    def test_query_engine_returns_response(self):
        """Querying the engine should return a response object.
        查询引擎应返回一个响应对象。"""
        mock_engine = MagicMock()
        mock_engine.query.return_value = MagicMock(
            response="SkyPet was founded in 2021."
        )

        result = mock_engine.query("When was SkyPet founded?")

        assert result.response == "SkyPet was founded in 2021."
        mock_engine.query.assert_called_once_with("When was SkyPet founded?")
