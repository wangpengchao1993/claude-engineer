"""
Tests for GSD (Get Shit Done) framework simulation.
GSD（把事做完）框架模拟的测试。

Run with: pytest test_gsd.py -v
运行方式: pytest test_gsd.py -v

No API keys required. / 无需 API 密钥。
"""

import pytest

from example_workflow import (
    SubAgent,
    simulate_accuracy,
    simulate_gsd_session,
    simulate_long_session,
    verify_task,
)


class TestContextRot:
    """Test that context rot simulation behaves correctly.
    测试上下文腐烂模拟的行为是否正确。
    """

    def test_accuracy_high_at_low_tokens(self):
        """Accuracy should be high with small context. / 小上下文时准确率应较高。"""
        acc = simulate_accuracy(0)
        assert acc >= 0.85, f"Expected high accuracy at 0 tokens, got {acc:.2f}"

    def test_accuracy_drops_with_token_count(self):
        """Accuracy should drop as token count grows. / 随着 token 数增长，准确率应下降。"""
        acc_low = simulate_accuracy(1_000)
        acc_high = simulate_accuracy(150_000)
        assert acc_low > acc_high, (
            f"Accuracy should decrease: {acc_low:.2f} at 1k tokens vs "
            f"{acc_high:.2f} at 150k tokens"
        )

    def test_accuracy_never_below_minimum(self):
        """Accuracy has a floor -- never drops below 30%. / 准确率有下限 -- 不低于 30%。"""
        acc = simulate_accuracy(1_000_000)
        assert acc >= 0.30, f"Accuracy floor violated: {acc:.2f}"

    def test_long_session_context_grows(self):
        """Without GSD, total tokens grow with each task. / 没有 GSD，总 token 随任务增长。"""
        results = simulate_long_session(num_tasks=5)
        token_counts = [r["tokens_total"] for r in results]
        assert token_counts == sorted(token_counts), "Token count should monotonically increase"
        assert token_counts[-1] > token_counts[0], "Final token count should exceed initial"


class TestSubAgentContext:
    """Test that GSD sub-agents use focused context, not full history.
    测试 GSD 子代理使用聚焦上下文，而非完整历史。
    """

    def test_subagent_context_is_small(self):
        """Sub-agent context = spec + files, stays small. / 子代理上下文 = 规格 + 文件，保持小。"""
        agent = SubAgent("test-task", spec_tokens=1_000, relevant_file_tokens=3_000)
        assert agent.context_tokens == 4_000
        assert agent.context_tokens < 10_000, "Sub-agent context should be focused, not bloated"

    def test_subagent_context_independent_of_session(self):
        """Each sub-agent starts fresh -- no accumulated context. / 每个子代理从零开始 -- 无累积上下文。"""
        agents = [SubAgent(f"task-{i}", 1_000, 3_000) for i in range(10)]
        contexts = [a.context_tokens for a in agents]
        assert all(c == 4_000 for c in contexts), "All sub-agents should have the same small context"

    def test_gsd_session_contexts_stay_small(self):
        """In a GSD session, no task context exceeds 10k tokens. / GSD 会话中，任务上下文不超过 10k。"""
        results = simulate_gsd_session(num_tasks=8)
        for r in results:
            assert r["context_tokens"] < 10_000, (
                f"{r['task']} context too large: {r['context_tokens']}"
            )


class TestVerification:
    """Test the automatic verification step. / 测试自动验证步骤。"""

    def test_verification_passes_with_valid_spec(self):
        """Verification passes when task passes and spec exists. / 任务通过且规格存在时验证通过。"""
        result = {"passed_verification": True}
        assert verify_task(result, "implement login feature") is True

    def test_verification_fails_on_empty_spec(self):
        """Verification fails with empty spec -- spec is required. / 空规格时验证失败 -- 规格是必需的。"""
        result = {"passed_verification": True}
        assert verify_task(result, "") is False

    def test_verification_fails_when_task_fails(self):
        """Verification fails when the task itself fails. / 任务本身失败时验证失败。"""
        result = {"passed_verification": False}
        assert verify_task(result, "valid spec content") is False


class TestTaskCompletion:
    """Test task completion tracking across sessions. / 测试跨会话的任务完成跟踪。"""

    def test_all_tasks_produce_results(self):
        """Every task produces a result dict. / 每个任务都产生一个结果字典。"""
        n = 6
        results = simulate_gsd_session(num_tasks=n)
        assert len(results) == n

    def test_result_has_required_fields(self):
        """Each result contains the expected fields. / 每个结果包含预期字段。"""
        results = simulate_gsd_session(num_tasks=1)
        r = results[0]
        for field in ("task", "context_tokens", "accuracy", "passed_verification", "verified"):
            assert field in r, f"Missing field: {field}"

    def test_gsd_average_accuracy_above_threshold(self):
        """GSD sessions should maintain high average accuracy. / GSD 会话应保持较高的平均准确率。"""
        results = simulate_gsd_session(num_tasks=10)
        avg = sum(r["accuracy"] for r in results) / len(results)
        assert avg > 0.80, f"GSD average accuracy too low: {avg:.2f}"
