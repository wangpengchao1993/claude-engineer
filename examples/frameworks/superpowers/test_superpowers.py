"""
Tests for the Superpowers Workflow Simulation
Superpowers 工作流模拟的测试

These tests validate each phase of the 7-phase methodology.
No API keys needed -- everything runs locally.

这些测试验证 7 阶段方法论的每个阶段。
不需要 API 密钥 -- 一切在本地运行。

Run with: pytest test_superpowers.py -v
运行方式: pytest test_superpowers.py -v
"""

import pytest
from example_workflow import (
    Brainstorm, Spec, Plan, Task, TDDCycle, Subagent, Review,
    run_superpowers_workflow,
)


class TestBrainstorm:
    """Test Phase 1: Brainstorm must produce clarifying questions.
    测试阶段 1：头脑风暴必须产生澄清性问题。"""

    def test_generates_questions(self):
        """Brainstorm should return multiple questions for any feature.
        头脑风暴应该为任何功能返回多个问题。"""
        questions = Brainstorm().run("user login")
        assert len(questions) >= 2
        assert all(isinstance(q, str) for q in questions)

    def test_questions_reference_feature(self):
        """Questions should mention the requested feature.
        问题应该提到请求的功能。"""
        questions = Brainstorm().run("search bar")
        assert any("search bar" in q for q in questions)


class TestSpec:
    """Test Phase 2: Spec generation and approval gate.
    测试阶段 2：规格生成和审批门控。"""

    def test_spec_generated_after_brainstorm(self):
        """A spec should have a title and requirements.
        规格应该有标题和需求。"""
        spec = Spec().generate("caching layer", answers=["ans1"])
        assert spec.title == "Spec: caching layer"
        assert len(spec.requirements) >= 1

    def test_spec_not_approved_by_default(self):
        """Specs start unapproved -- human must approve.
        规格默认未批准 -- 人类必须批准。"""
        spec = Spec().generate("feature", answers=[])
        assert spec.approved is False

    def test_spec_approval(self):
        """After approval, spec.approved is True.
        批准后，spec.approved 为 True。"""
        spec = Spec().generate("feature", answers=[])
        spec.approve()
        assert spec.approved is True


class TestPlan:
    """Test Phase 3: Plan refuses to proceed without approved spec.
    测试阶段 3：计划在规格未批准时拒绝继续。"""

    def test_creates_tasks_from_approved_spec(self):
        """Plan should create multiple tasks from an approved spec.
        计划应该从已批准的规格创建多个任务。"""
        spec = Spec().generate("api endpoint", answers=[])
        spec.approve()
        tasks = Plan().create_tasks(spec)
        assert len(tasks) >= 2
        assert all(isinstance(t, Task) for t in tasks)

    def test_refuses_unapproved_spec(self):
        """Plan must raise an error if spec is not approved.
        如果规格未批准，计划必须抛出错误。"""
        spec = Spec().generate("feature", answers=[])
        with pytest.raises(ValueError, match="approved"):
            Plan().create_tasks(spec)


class TestTDD:
    """Test Phase 4: TDD cycle goes red -> green -> refactor.
    测试阶段 4：TDD 循环经过 红 -> 绿 -> 重构。"""

    def test_red_phase_fails(self):
        """RED: test should fail before implementation.
        红色：测试在实现前应该失败。"""
        result = TDDCycle().red("test_add")
        assert result["status"] == "FAIL"
        assert result["phase"] == "red"

    def test_green_phase_passes(self):
        """GREEN: test passes after minimal implementation.
        绿色：最小实现后测试通过。"""
        result = TDDCycle().green("test_add")
        assert result["status"] == "PASS"
        assert result["phase"] == "green"

    def test_refactor_stays_green(self):
        """REFACTOR: tests still pass after cleanup.
        重构：清理后测试仍然通过。"""
        result = TDDCycle().refactor("test_add")
        assert result["status"] == "PASS"
        assert result["phase"] == "refactor"


class TestReview:
    """Test Phase 6: Review checks all phases are complete.
    测试阶段 6：审查检查所有阶段是否完成。"""

    def test_review_passes_when_all_complete(self):
        """Review passes when spec is approved and all tasks done.
        当规格已批准且所有任务完成时，审查通过。"""
        spec = Spec().generate("f", answers=[])
        spec.approve()
        tasks = [Task("t1", "desc", completed=True), Task("t2", "desc", completed=True)]
        result = Review().check(spec, tasks)
        assert result["passed"] is True

    def test_review_fails_with_incomplete_tasks(self):
        """Review fails if any task is not completed.
        如果有任何任务未完成，审查失败。"""
        spec = Spec().generate("f", answers=[])
        spec.approve()
        tasks = [Task("t1", "desc", completed=True), Task("t2", "desc", completed=False)]
        result = Review().check(spec, tasks)
        assert result["passed"] is False

    def test_review_fails_without_spec_approval(self):
        """Review fails if spec was never approved.
        如果规格从未被批准，审查失败。"""
        spec = Spec().generate("f", answers=[])
        tasks = [Task("t1", "desc", completed=True)]
        result = Review().check(spec, tasks)
        assert result["passed"] is False


class TestFullWorkflow:
    """Test the end-to-end workflow simulation.
    测试端到端工作流模拟。"""

    def test_workflow_completes_successfully(self):
        """The full 7-phase workflow should pass.
        完整的 7 阶段工作流应该通过。"""
        result = run_superpowers_workflow("test feature")
        assert result["passed"] is True
        assert result["spec_approved"] is True
        assert result["all_tasks_complete"] is True
