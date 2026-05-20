"""
Tests for Hermes Agent self-improvement simulation.
Hermes Agent 自改进模拟测试。

Run with: pytest test_hermes.py -v
运行方式: pytest test_hermes.py -v

No API keys required. / 无需 API 密钥。
"""

import pytest
from example_workflow import Skill, Memory, evaluate_result


# --- Test: Skill improves after learning / 测试：技能在学习后改进 ---
def test_skill_improves_after_learning():
    """After learning patterns, skill score should increase. / 学习模式后，技能分数应提高。"""
    skill = Skill(name="test_skill")
    before = skill.apply("some task")["score"]

    skill.learn("pattern_a")
    skill.learn("pattern_b")
    after = skill.apply("some task")["score"]

    assert after > before, "Skill should improve after learning / 学习后技能应改进"
    assert skill.version == 3, "Version should increment per pattern / 每学一个模式版本应递增"


# --- Test: Memory persists across sessions / 测试：记忆跨会话保留 ---
def test_memory_persists_across_sessions():
    """Memory should retain values, simulating cross-session persistence. / 记忆应保留值，模拟跨会话持久性。"""
    memory = Memory()

    # Session 1: store facts / 会话 1：存储事实
    memory.remember("user_preference", "dark_mode")
    memory.remember("last_project", "hermes-agent")

    # Session 2: recall facts / 会话 2：回忆事实
    assert memory.recall("user_preference") == "dark_mode"
    assert memory.recall("last_project") == "hermes-agent"
    assert memory.recall("nonexistent") is None


# --- Test: Learning loop extracts patterns / 测试：学习循环提取模式 ---
def test_learning_loop_extracts_patterns():
    """evaluate_result should extract relevant patterns from task results. / evaluate_result 应从任务结果中提取相关模式。"""
    high_score_result = {"task": "Write tests for module", "score": 0.8}
    patterns = evaluate_result(high_score_result)

    assert "high_confidence_approach" in patterns, "Should detect high confidence / 应检测到高置信度"
    assert "test_driven_pattern" in patterns, "Should detect test keyword / 应检测到测试关键词"

    low_score_result = {"task": "Refactor the code", "score": 0.5}
    patterns = evaluate_result(low_score_result)

    assert "needs_more_context" in patterns, "Should flag low score / 应标记低分"
    assert "code_structure_awareness" in patterns, "Should detect refactor keyword / 应检测到重构关键词"


# --- Test: Performance improves over iterations / 测试：性能随迭代改进 ---
def test_performance_improves_over_iterations():
    """Simulating multiple tasks should show increasing scores. / 模拟多个任务应显示分数递增。"""
    skill = Skill(name="iteration_skill")
    scores = []

    tasks = [
        ("Parse config file", ["config_parsing"]),
        ("Refactor config parser", ["code_structure_awareness", "error_handling"]),
        ("Write tests for parser", ["test_driven_pattern"]),
    ]

    for task_name, patterns in tasks:
        result = skill.apply(task_name)
        scores.append(result["score"])
        for p in patterns:
            skill.learn(p)

    # Each score should be >= the previous one / 每个分数应 >= 前一个
    for i in range(1, len(scores)):
        assert scores[i] >= scores[i - 1], (
            f"Score should not decrease: {scores[i]} < {scores[i-1]} "
            f"/ 分数不应下降: {scores[i]} < {scores[i-1]}"
        )

    # Final should be clearly better than initial / 最终分数应明显优于初始分数
    assert scores[-1] > scores[0], "Final score must beat initial / 最终分数必须超过初始分数"
