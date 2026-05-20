"""
Tests for BMAD-METHOD Example Workflow / BMAD-METHOD 示例工作流测试
===================================================================

Verifies that each agent produces correct output and that a full
sprint completes all phases successfully.

验证每个智能体产生正确的产出，以及完整冲刺能成功完成所有阶段。

Run with: pytest test_bmad.py -v
运行方式: pytest test_bmad.py -v

No API keys needed. / 无需 API 密钥。
"""

import pytest
from example_workflow import (
    ProductManager,
    Architect,
    Developer,
    QAEngineer,
    run_sprint,
)

SAMPLE_IDEA = "Build a task management dashboard"


# --- Test ProductManager / 测试产品经理 ---

def test_pm_generates_user_stories():
    """PM should produce requirements and user stories from an idea.
    产品经理应从想法中生成需求和用户故事。"""
    pm = ProductManager()
    result = pm.process({"idea": SAMPLE_IDEA})

    assert "requirements" in result, "PM must output requirements / 产品经理必须输出需求"
    assert "user_stories" in result, "PM must output user stories / 产品经理必须输出用户故事"
    assert len(result["user_stories"]) > 0, "Must have at least one story / 至少要有一个用户故事"


# --- Test Architect / 测试架构师 ---

def test_architect_creates_design():
    """Architect should produce architecture and tech stack from requirements.
    架构师应从需求中生成架构设计和技术栈。"""
    pm_output = ProductManager().process({"idea": SAMPLE_IDEA})
    architect = Architect()
    result = architect.process(pm_output)

    assert "architecture" in result, "Architect must output architecture / 架构师必须输出架构"
    assert "tech_stack" in result, "Architect must output tech stack / 架构师必须输出技术栈"
    assert len(result["tech_stack"]) > 0, "Tech stack must not be empty / 技术栈不能为空"
    assert "components" in result, "Architect must define components / 架构师必须定义组件"


# --- Test Developer / 测试开发者 ---

def test_developer_produces_code():
    """Developer should produce code files from architecture.
    开发者应从架构中生成代码文件。"""
    pm_output = ProductManager().process({"idea": SAMPLE_IDEA})
    arch_output = Architect().process(pm_output)
    developer = Developer()
    result = developer.process(arch_output)

    assert "code_files" in result, "Developer must output code files / 开发者必须输出代码文件"
    assert len(result["code_files"]) > 0, "Must produce at least one file / 至少要生成一个文件"
    for filename in result["code_files"]:
        assert filename.endswith(".py"), f"Code file should be .py: {filename} / 代码文件应为 .py"


# --- Test QA Engineer / 测试 QA 工程师 ---

def test_qa_creates_tests():
    """QA should produce test results from code files.
    QA 工程师应从代码文件中生成测试结果。"""
    pm_output = ProductManager().process({"idea": SAMPLE_IDEA})
    arch_output = Architect().process(pm_output)
    dev_output = Developer().process(arch_output)
    qa = QAEngineer()
    result = qa.process(dev_output)

    assert "test_results" in result, "QA must output test results / QA 必须输出测试结果"
    assert "all_passed" in result, "QA must report pass/fail status / QA 必须报告通过/失败状态"
    assert result["all_passed"] is True, "All tests should pass / 所有测试应通过"


# --- Test full sprint / 测试完整冲刺 ---

def test_sprint_completes_all_phases():
    """A full sprint should produce outputs from every agent phase.
    完整冲刺应产出每个智能体阶段的结果。"""
    result = run_sprint(SAMPLE_IDEA)

    # Verify every phase contributed / 验证每个阶段都有贡献
    required_keys = ["user_stories", "architecture", "tech_stack", "code_files", "test_results"]
    for key in required_keys:
        assert key in result, f"Sprint result missing '{key}' / 冲刺结果缺少 '{key}'"

    assert result["all_passed"] is True, "Sprint should end with all tests passing / 冲刺应以所有测试通过结束"
    assert len(result["code_files"]) == len(result["user_stories"]), (
        "Each story should map to a component / 每个用户故事应对应一个组件"
    )
