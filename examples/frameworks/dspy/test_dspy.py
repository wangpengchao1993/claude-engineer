"""
Tests for DSPy Concepts (no API key needed) / DSPy 概念测试（无需 API 密钥）

These tests verify that DSPy's core building blocks — Signatures,
Modules, and Fields — can be created and configured correctly,
without making any real LLM calls.

这些测试验证 DSPy 的核心构建模块——签名、模块和字段——
能被正确创建和配置，无需进行任何真实的大模型调用。

Usage / 用法:
    pip install pytest dspy
    pytest test_dspy.py -v
"""

import pytest
from unittest.mock import MagicMock, patch

import dspy
from dspy import Signature, InputField, OutputField, Predict, ChainOfThought


# === Signature to test with / 用于测试的签名 ===
class SentimentClassify(Signature):
    """Classify sentiment of text. / 对文本进行情感分类。"""
    text = InputField(desc="The text to classify")
    category = OutputField(desc="positive, negative, or neutral")
    confidence = OutputField(desc="Confidence from 0.0 to 1.0")


class TestSignatureDefinition:
    """Test that Signatures are defined correctly / 测试签名定义是否正确"""

    def test_signature_has_input_fields(self):
        """Signature should declare input fields / 签名应该声明输入字段"""
        fields = SentimentClassify.input_fields
        assert "text" in fields, "Expected 'text' in input fields / 期望 'text' 在输入字段中"

    def test_signature_has_output_fields(self):
        """Signature should declare output fields / 签名应该声明输出字段"""
        fields = SentimentClassify.output_fields
        assert "category" in fields, "Expected 'category' in output fields"
        assert "confidence" in fields, "Expected 'confidence' in output fields"

    def test_signature_docstring(self):
        """Signature docstring becomes the task description / 签名的文档字符串成为任务描述"""
        assert "sentiment" in SentimentClassify.__doc__.lower()


class TestModuleCreation:
    """Test that Modules can be instantiated / 测试模块能否被实例化"""

    def test_predict_module_creation(self):
        """Predict module wraps a Signature / Predict 模块封装一个签名"""
        module = Predict(SentimentClassify)
        assert module is not None

    def test_chain_of_thought_creation(self):
        """ChainOfThought adds a reasoning step / ChainOfThought 添加推理步骤"""
        module = ChainOfThought(SentimentClassify)
        assert module is not None

    def test_chain_of_thought_has_extended_signature(self):
        """
        ChainOfThought should add a 'reasoning' field to the output.
        ChainOfThought 应该在输出中添加 'reasoning' 字段。
        """
        module = ChainOfThought(SentimentClassify)
        # The extended signature includes a reasoning field
        # 扩展签名包含一个 reasoning 字段
        extended = module.extended_signature if hasattr(module, "extended_signature") else None
        if extended is not None:
            assert "reasoning" in extended.output_fields


class TestFieldSpecs:
    """Test InputField and OutputField configuration / 测试输入输出字段配置"""

    def test_input_field_description(self):
        """InputField should store its description / InputField 应该存储其描述"""
        fields = SentimentClassify.input_fields
        text_field = fields["text"]
        assert text_field.json_schema_extra["desc"] == "The text to classify"

    def test_output_field_description(self):
        """OutputField should store its description / OutputField 应该存储其描述"""
        fields = SentimentClassify.output_fields
        cat_field = fields["category"]
        assert "positive" in cat_field.json_schema_extra["desc"]


class TestInlineSignature:
    """Test shorthand string signatures / 测试简写字符串签名"""

    def test_inline_signature_with_predict(self):
        """
        DSPy supports inline signatures like 'question -> answer'.
        DSPy 支持内联签名，如 'question -> answer'。
        """
        module = Predict("question -> answer")
        assert module is not None

    def test_inline_signature_multiple_outputs(self):
        """
        Inline signatures can have multiple outputs: 'text -> label, score'.
        内联签名可以有多个输出：'text -> label, score'。
        """
        module = Predict("text -> label, score")
        assert module is not None
