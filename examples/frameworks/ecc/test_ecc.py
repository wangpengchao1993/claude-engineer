"""
Tests for the ECC example workflow.
ECC 示例工作流的测试。

Run with: pytest test_ecc.py -v
运行方式：pytest test_ecc.py -v

No API keys needed / 无需 API 密钥。
"""

import pytest
from example_workflow import (
    select_agent,
    research_phase,
    planning_phase,
    tdd_phase,
    security_scan,
    code_review,
    AGENTS,
)


# --- Test agent selection / 测试 Agent 选择 ---

@pytest.mark.parametrize("task_type,expected_key", [
    ("research", "research"),
    ("plan", "planning"),
    ("test", "tdd"),
    ("security", "security"),
    ("build", "build"),
    ("review_python", "review_py"),
    ("review_typescript", "review_ts"),
])
def test_select_agent_by_task_type(task_type: str, expected_key: str):
    """Correct agent is chosen for each task type. / 每种任务类型都能选到正确的 Agent。"""
    agent = select_agent(task_type)
    assert agent is AGENTS[expected_key]


def test_select_agent_unknown_raises():
    """Unknown task type raises ValueError. / 未知任务类型抛出 ValueError。"""
    with pytest.raises(ValueError):
        select_agent("nonexistent")


# --- Test research phase / 测试研究阶段 ---

def test_research_phase_returns_findings():
    """Research phase produces a non-empty list of findings. / 研究阶段产生非空的发现列表。"""
    findings = research_phase("authentication")
    assert len(findings) >= 1
    assert all(isinstance(f, str) for f in findings)


# --- Test planning phase / 测试规划阶段 ---

def test_planning_creates_steps():
    """Planning agent creates multiple implementation steps. / 规划 Agent 创建多个实施步骤。"""
    steps = planning_phase("build login page")
    assert len(steps) >= 2
    # Each step should mention the task or be a concrete action
    # 每个步骤都应提及任务或是一个具体动作
    assert any("login" in s.lower() for s in steps)


# --- Test TDD phase / 测试 TDD 阶段 ---

def test_tdd_generates_tests_for_each_step():
    """TDD agent generates one test per plan step. / TDD Agent 为每个计划步骤生成一个测试。"""
    plan = ["step A", "step B", "step C"]
    tests = tdd_phase(plan)
    assert len(tests) == len(plan)


# --- Test security scan / 测试安全扫描 ---

def test_security_scan_detects_issues():
    """Security scan finds at least one issue. / 安全扫描至少发现一个问题。"""
    issues = security_scan("user input handler")
    assert len(issues) >= 1
    # Each issue has required fields / 每个问题都有必需字段
    for issue in issues:
        assert "severity" in issue
        assert "issue" in issue


# --- Test code review / 测试代码审查 ---

@pytest.mark.parametrize("language", ["python", "typescript", "go", "rust"])
def test_code_review_per_language(language: str):
    """Code review works for each supported language. / 代码审查适用于每种支持的语言。"""
    result = code_review(language, "sample code")
    assert result["language"] == language
    assert isinstance(result["suggestions"], list)
    assert len(result["suggestions"]) >= 1
    assert "approved" in result
