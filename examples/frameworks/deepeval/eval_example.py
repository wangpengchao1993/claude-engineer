"""
DeepEval Evaluation Example / DeepEval 评估示例
================================================

This script shows how to evaluate LLM outputs using DeepEval.
本脚本演示如何使用 DeepEval 评估大模型的输出。

Requirements / 依赖:
    pip install deepeval

Note / 注意:
    Metrics like AnswerRelevancy use an LLM judge under the hood,
    so you need OPENAI_API_KEY set in your environment.
    AnswerRelevancy 等指标底层使用 LLM 做裁判，
    所以你需要在环境变量中设置 OPENAI_API_KEY。
"""

from deepeval import assert_test, evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
)
from deepeval.dataset import EvaluationDataset


# =============================================================================
# 1. Create a Test Case / 创建测试用例
# =============================================================================
# A test case is the basic unit: an input question + the LLM's actual output.
# You can also include expected_output (ideal answer) and context (RAG chunks).
# 测试用例是基本单位：一个输入问题 + 大模型的实际输出。
# 你也可以包含 expected_output（理想回答）和 context（RAG 检索片段）。

test_case_simple = LLMTestCase(
    input="What is the capital of France?",          # Question / 问题
    actual_output="The capital of France is Paris.",  # LLM answer / 大模型回答
)

# A more detailed test case with context (for RAG evaluation)
# 一个带上下文的更详细的测试用例（用于 RAG 评估）
test_case_rag = LLMTestCase(
    input="What language is Django written in?",
    actual_output="Django is written in Python. It is a popular web framework.",
    expected_output="Django is written in Python.",
    context=[
        "Django is a high-level Python web framework.",
        "Django was created in 2003 and released publicly in 2005.",
    ],
)


# =============================================================================
# 2. Answer Relevancy / 回答相关性
# =============================================================================
# Checks: does the answer actually address the question?
# 检查：回答是否真正回应了问题？

relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,  # Score must be >= 0.7 to pass / 分数 >= 0.7 才算通过
)


# =============================================================================
# 3. Faithfulness (for RAG) / 忠实度（用于 RAG）
# =============================================================================
# Checks: is the answer faithful to the provided context?
# If the LLM says something not in the context, faithfulness drops.
# 检查：回答是否忠于提供的上下文？
# 如果大模型说了上下文中没有的内容，忠实度就会下降。

faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
)


# =============================================================================
# 4. Hallucination / 幻觉检测
# =============================================================================
# Checks: does the answer contain made-up facts not in the context?
# Lower score = less hallucination = better.
# 检查：回答是否包含上下文中没有的编造事实？
# 分数越低 = 幻觉越少 = 越好。

hallucination_metric = HallucinationMetric(
    threshold=0.5,  # Hallucination score must be <= 0.5 / 幻觉分数须 <= 0.5
)


# =============================================================================
# 5. Run a Single Evaluation / 运行单个评估
# =============================================================================
# assert_test works like pytest's assert -- it raises if the metric fails.
# assert_test 像 pytest 的 assert 一样——如果指标不通过就抛出异常。

def run_single_test():
    """Evaluate one test case with one metric / 用一个指标评估一个测试用例"""
    print("--- Single Test / 单个测试 ---")
    try:
        assert_test(test_case_simple, metrics=[relevancy_metric])
        print("PASSED: Answer is relevant! / 通过：回答是相关的！")
    except AssertionError:
        print("FAILED: Answer is not relevant enough. / 不通过：回答相关性不足。")


# =============================================================================
# 6. Bulk Evaluation with Dataset / 用数据集进行批量评估
# =============================================================================
# When you have many test cases, group them into a dataset and evaluate together.
# 当你有很多测试用例时，把它们组成一个数据集一起评估。

def run_bulk_evaluation():
    """Evaluate multiple test cases at once / 一次评估多个测试用例"""
    print("\n--- Bulk Evaluation / 批量评估 ---")

    # Create more test cases / 创建更多测试用例
    cases = [
        LLMTestCase(
            input="What is Python?",
            actual_output="Python is a high-level programming language.",
            context=["Python is a popular high-level programming language."],
        ),
        LLMTestCase(
            input="Who created Linux?",
            actual_output="Linux was created by Linus Torvalds in 1991.",
            context=["Linus Torvalds created Linux in 1991."],
        ),
        LLMTestCase(
            input="What is machine learning?",
            actual_output="Machine learning is a subset of AI that learns from data.",
            context=["ML is a branch of artificial intelligence."],
        ),
    ]

    # Group into a dataset / 组成数据集
    dataset = EvaluationDataset(test_cases=cases)

    # Evaluate all cases with multiple metrics / 用多个指标评估所有用例
    results = evaluate(
        test_cases=dataset.test_cases,
        metrics=[relevancy_metric, faithfulness_metric],
    )

    # Print summary / 打印摘要
    print(f"Total test cases / 测试用例总数: {len(results.test_results)}")
    for i, result in enumerate(results.test_results):
        print(f"  Case {i+1}: {'PASSED' if result.success else 'FAILED'}"
              f" / {'通过' if result.success else '不通过'}")


# =============================================================================
# Main / 主函数
# =============================================================================
if __name__ == "__main__":
    print("DeepEval Example / DeepEval 示例")
    print("=" * 40)
    print()
    run_single_test()
    run_bulk_evaluation()
    print()
    print("Done! / 完成！")
