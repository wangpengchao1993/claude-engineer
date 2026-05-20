"""
DeepEval Unit Tests (No API Key Required) / DeepEval 单元测试（无需 API 密钥）
=============================================================================

These tests verify DeepEval components work correctly WITHOUT calling any LLM.
We use unittest.mock to avoid real API calls.
这些测试验证 DeepEval 组件能正确工作，且不调用任何大模型。
我们使用 unittest.mock 来避免真实的 API 调用。

Run with / 运行方式:
    pytest test_deepeval.py -v
"""

import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Test 1: LLMTestCase creation / 测试1：创建 LLMTestCase
# ---------------------------------------------------------------------------
def test_create_test_case():
    """Verify LLMTestCase stores fields correctly.
    验证 LLMTestCase 能正确存储各字段。"""
    from deepeval.test_case import LLMTestCase

    case = LLMTestCase(
        input="What is Python?",
        actual_output="Python is a programming language.",
        expected_output="Python is a high-level programming language.",
        context=["Python is a popular high-level language."],
    )

    assert case.input == "What is Python?"
    assert case.actual_output == "Python is a programming language."
    assert case.expected_output == "Python is a high-level programming language."
    assert len(case.context) == 1


# ---------------------------------------------------------------------------
# Test 2: Metric initialization / 测试2：指标初始化
# ---------------------------------------------------------------------------
def test_metric_initialization():
    """Verify metrics can be created with custom thresholds.
    验证指标能使用自定义阈值创建。"""
    from deepeval.metrics import AnswerRelevancyMetric

    metric = AnswerRelevancyMetric(threshold=0.8)
    assert metric.threshold == 0.8


def test_faithfulness_metric_initialization():
    """Verify FaithfulnessMetric initializes properly.
    验证 FaithfulnessMetric 能正确初始化。"""
    from deepeval.metrics import FaithfulnessMetric

    metric = FaithfulnessMetric(threshold=0.6)
    assert metric.threshold == 0.6


def test_hallucination_metric_initialization():
    """Verify HallucinationMetric initializes properly.
    验证 HallucinationMetric 能正确初始化。"""
    from deepeval.metrics import HallucinationMetric

    metric = HallucinationMetric(threshold=0.5)
    assert metric.threshold == 0.5


# ---------------------------------------------------------------------------
# Test 3: Dataset creation / 测试3：数据集创建
# ---------------------------------------------------------------------------
def test_dataset_creation():
    """Verify EvaluationDataset holds multiple test cases.
    验证 EvaluationDataset 能容纳多个测试用例。"""
    from deepeval.test_case import LLMTestCase
    from deepeval.dataset import EvaluationDataset

    cases = [
        LLMTestCase(input="Q1", actual_output="A1"),
        LLMTestCase(input="Q2", actual_output="A2"),
        LLMTestCase(input="Q3", actual_output="A3"),
    ]
    dataset = EvaluationDataset(test_cases=cases)

    assert len(dataset.test_cases) == 3
    assert dataset.test_cases[0].input == "Q1"
    assert dataset.test_cases[2].actual_output == "A3"


# ---------------------------------------------------------------------------
# Test 4: Threshold configuration / 测试4：阈值配置
# ---------------------------------------------------------------------------
def test_threshold_boundary():
    """Verify different threshold values are accepted.
    验证不同的阈值设置能被接受。"""
    from deepeval.metrics import AnswerRelevancyMetric

    # Low threshold -- more lenient / 低阈值——更宽松
    lenient = AnswerRelevancyMetric(threshold=0.3)
    assert lenient.threshold == 0.3

    # High threshold -- more strict / 高阈值——更严格
    strict = AnswerRelevancyMetric(threshold=0.95)
    assert strict.threshold == 0.95


# ---------------------------------------------------------------------------
# Test 5: Mock metric measure / 测试5：模拟指标评估
# ---------------------------------------------------------------------------
def test_metric_measure_mocked():
    """Verify metric.measure() can be called (mocked, no real API).
    验证 metric.measure() 可以被调用（已模拟，无需真实 API）。"""
    from deepeval.test_case import LLMTestCase
    from deepeval.metrics import AnswerRelevancyMetric

    case = LLMTestCase(
        input="What is 2+2?",
        actual_output="2+2 equals 4.",
    )
    metric = AnswerRelevancyMetric(threshold=0.7)

    # Mock the measure method to avoid real API calls
    # 模拟 measure 方法以避免真实的 API 调用
    with patch.object(metric, "measure", return_value=0.95) as mock_measure:
        score = metric.measure(case)
        mock_measure.assert_called_once_with(case)
        assert score == 0.95
