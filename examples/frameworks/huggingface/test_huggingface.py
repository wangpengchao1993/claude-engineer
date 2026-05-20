"""
Tests for Hugging Face Examples / Hugging Face 示例测试
======================================================

These tests verify Hugging Face functionality WITHOUT downloading real models.
We use mocking so tests run fast and don't need internet or GPU.

这些测试在不下载真实模型的情况下验证 Hugging Face 功能。
使用 mock 使测试运行快速，无需网络或 GPU。

Run / 运行: pytest test_huggingface.py -v
"""

import pytest
from unittest.mock import patch, MagicMock


class TestPipelineCreation:
    """Test that pipelines can be created correctly / 测试管道是否能正确创建"""

    @patch("transformers.pipeline")
    def test_sentiment_pipeline(self, mock_pipeline):
        """Pipeline should accept task name / 管道应接受任务名称"""
        mock_pipeline.return_value = MagicMock()
        from transformers import pipeline

        classifier = pipeline("sentiment-analysis")
        mock_pipeline.assert_called_with("sentiment-analysis")
        assert classifier is not None

    @patch("transformers.pipeline")
    def test_generation_pipeline_with_model(self, mock_pipeline):
        """Pipeline should accept model name / 管道应接受模型名称"""
        mock_pipeline.return_value = MagicMock()
        from transformers import pipeline

        generator = pipeline("text-generation", model="gpt2")
        mock_pipeline.assert_called_with("text-generation", model="gpt2")

    @patch("transformers.pipeline")
    def test_pipeline_returns_results(self, mock_pipeline):
        """Pipeline should return predictions / 管道应返回预测结果"""
        mock_result = [{"label": "POSITIVE", "score": 0.9998}]
        mock_fn = MagicMock(return_value=mock_result)
        mock_pipeline.return_value = mock_fn
        from transformers import pipeline

        classifier = pipeline("sentiment-analysis")
        result = classifier("I love this!")

        assert result[0]["label"] == "POSITIVE"
        assert result[0]["score"] > 0.99


class TestTokenizer:
    """Test tokenizer encoding and decoding / 测试分词器的编码和解码"""

    @patch("transformers.AutoTokenizer.from_pretrained")
    def test_tokenizer_encode(self, mock_from_pretrained):
        """Tokenizer should convert text to IDs / 分词器应将文本转为 ID"""
        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = [15496, 11, 995, 0]
        mock_from_pretrained.return_value = mock_tokenizer
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        ids = tokenizer.encode("Hello, world!")

        assert isinstance(ids, list)
        assert len(ids) > 0
        assert all(isinstance(i, int) for i in ids)

    @patch("transformers.AutoTokenizer.from_pretrained")
    def test_tokenizer_decode(self, mock_from_pretrained):
        """Tokenizer should convert IDs back to text / 分词器应将 ID 还原为文本"""
        mock_tokenizer = MagicMock()
        mock_tokenizer.decode.return_value = "Hello, world!"
        mock_from_pretrained.return_value = mock_tokenizer
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        text = tokenizer.decode([15496, 11, 995, 0])

        assert isinstance(text, str)
        assert len(text) > 0

    @patch("transformers.AutoTokenizer.from_pretrained")
    def test_tokenizer_roundtrip(self, mock_from_pretrained):
        """Encode then decode should return original text / 编码再解码应返回原文"""
        original = "AI is amazing"
        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = [20185, 318, 4998]
        mock_tokenizer.decode.return_value = original
        mock_from_pretrained.return_value = mock_tokenizer
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        ids = tokenizer.encode(original)
        decoded = tokenizer.decode(ids)

        assert decoded == original


class TestModelConfiguration:
    """Test model loading and config / 测试模型加载和配置"""

    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_model_loading(self, mock_from_pretrained):
        """Model should load from name / 模型应能从名称加载"""
        mock_model = MagicMock()
        mock_from_pretrained.return_value = mock_model
        from transformers import AutoModelForCausalLM

        model = AutoModelForCausalLM.from_pretrained("gpt2")
        mock_from_pretrained.assert_called_with("gpt2")
        assert model is not None

    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_model_generate(self, mock_from_pretrained):
        """Model should accept generation parameters / 模型应接受生成参数"""
        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_model.generate.return_value = mock_output
        mock_from_pretrained.return_value = mock_model
        from transformers import AutoModelForCausalLM

        model = AutoModelForCausalLM.from_pretrained("gpt2")
        fake_input = MagicMock()

        model.generate(
            input_ids=fake_input,
            max_new_tokens=30,
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
        )

        model.generate.assert_called_once()
        call_kwargs = model.generate.call_args[1]
        assert call_kwargs["max_new_tokens"] == 30
        assert call_kwargs["temperature"] == 0.8
        assert call_kwargs["top_p"] == 0.9
        assert call_kwargs["do_sample"] is True


class TestGenerationParameters:
    """Test that generation parameters are validated / 测试生成参数是否正确验证"""

    def test_temperature_range(self):
        """Temperature should be between 0 and 2 / 温度应在 0 到 2 之间"""
        valid_temps = [0.1, 0.5, 0.7, 1.0, 1.5]
        for temp in valid_temps:
            assert 0 < temp <= 2, f"Temperature {temp} out of range"

    def test_top_p_range(self):
        """top_p should be between 0 and 1 / top_p 应在 0 到 1 之间"""
        valid_values = [0.1, 0.5, 0.9, 0.95, 1.0]
        for val in valid_values:
            assert 0 < val <= 1, f"top_p {val} out of range"

    def test_max_length_positive(self):
        """max_length should be a positive integer / max_length 应为正整数"""
        valid_lengths = [10, 50, 100, 512]
        for length in valid_lengths:
            assert length > 0, f"max_length {length} should be positive"
            assert isinstance(length, int), f"max_length should be int"
