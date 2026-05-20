"""
Tests for Spec-Kit Workflow / Spec-Kit 工作流测试

Validates each phase produces correct output.
验证每个阶段产生正确的输出。

Run: pytest test_spec_kit.py -v
"""

import pytest
from example_workflow import (
    Constitution, Specification, Plan, Task,
    phase1_constitution, phase2_specify, phase3_clarify,
    phase4_plan, phase5_tasks, phase6_implement,
)


# --- Fixtures / 测试夹具 ---

@pytest.fixture
def constitution():
    """Create a constitution for testing / 创建用于测试的宪法"""
    return phase1_constitution("Test Project / 测试项目")


@pytest.fixture
def spec(constitution):
    """Create a specification for testing / 创建用于测试的规格"""
    return phase2_specify(constitution)


@pytest.fixture
def clarified_spec(spec):
    """Create a clarified spec for testing / 创建用于测试的已澄清规格"""
    return phase3_clarify(spec)


@pytest.fixture
def plan(clarified_spec, constitution):
    """Create a plan for testing / 创建用于测试的计划"""
    return phase4_plan(clarified_spec, constitution)


@pytest.fixture
def tasks(plan):
    """Create tasks for testing / 创建用于测试的任务"""
    return phase5_tasks(plan)


# --- Tests / 测试 ---

def test_constitution_has_required_fields(constitution):
    """Constitution must define technologies, testing, style, and constraints.
    宪法必须定义技术栈、测试、风格和约束条件。"""
    assert "language" in constitution.technologies
    assert "framework" in constitution.technologies
    assert constitution.testing["required"] is True
    assert constitution.testing["min_coverage"] > 0
    assert len(constitution.constraints) > 0
    assert isinstance(constitution.style, dict)


def test_specify_creates_requirements_from_constitution(spec, constitution):
    """Specify must produce features that reference the constitution.
    规格说明必须产生引用宪法的功能。"""
    assert len(spec.features) > 0
    assert len(spec.non_functional) > 0
    # Features should reference the chosen language / 功能应引用所选语言
    lang = constitution.technologies["language"]
    assert any(lang in f for f in spec.features)


def test_clarify_resolves_ambiguities(clarified_spec):
    """Clarify must resolve all ambiguities from the spec.
    澄清必须解决规格中的所有歧义。"""
    assert len(clarified_spec.ambiguities) == 0
    # Clarified decisions become features / 澄清的决定变成功能
    assert any("JWT" in f for f in clarified_spec.features)


def test_plan_references_requirements(plan, clarified_spec):
    """Plan steps must cover the specified requirements.
    计划步骤必须覆盖指定的需求。"""
    assert len(plan.steps) > 0
    # Plan should include auth (from clarified spec) / 计划应包含认证（来自已澄清的规格）
    step_text = " ".join(plan.steps)
    assert "auth" in step_text.lower()
    assert isinstance(plan.dependencies, dict)


def test_tasks_generated_from_plan(tasks, plan):
    """Each plan step must become a task / 每个计划步骤必须变成一个任务"""
    assert len(tasks) == len(plan.steps)
    for task in tasks:
        assert isinstance(task, Task)
        assert task.status == "pending"  # Not yet executed / 尚未执行
        assert task.description in plan.steps


def test_implement_tracks_task_completion(tasks):
    """Implement must mark all tasks as done / 执行必须将所有任务标记为完成"""
    completed = phase6_implement(tasks)
    assert all(t.status == "done" for t in completed)
    assert len(completed) == len(tasks)
