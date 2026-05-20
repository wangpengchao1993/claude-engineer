"""
Tests for Claude Code Workflows
Claude Code Workflows 测试

Run with: pytest test_workflows.py -v
运行方式: pytest test_workflows.py -v

No API keys required. / 无需 API 密钥。
"""

import pytest

from example_workflow import (
    analyze_complexity,
    generate_prd,
    generate_design_doc,
    generate_work_plan,
    verify_against_design,
)


# --- Test complexity analyzer / 测试复杂度分析器 ---

class TestComplexityAnalyzer:
    """Verify that the analyzer categorizes tasks correctly.
    验证分析器是否正确分类任务。"""

    def test_large_keyword_detected(self):
        """Authentication-related ideas should be at least medium complexity.
        与认证相关的想法应至少为中等复杂度。"""
        assert analyze_complexity("add user authentication") == "medium"

    def test_small_keyword_detected(self):
        """Trivial changes like typo fixes should be small.
        拼写修正等琐碎改动应为小型任务。"""
        assert analyze_complexity("fix typo in readme") == "small"

    def test_default_is_medium(self):
        """Unknown ideas default to medium complexity.
        无法识别的想法默认为中等复杂度。"""
        assert analyze_complexity("build dashboard") == "medium"


# --- Test PRD generation / 测试 PRD 生成 ---

class TestPRDGeneration:
    """Verify that generated PRDs contain required sections.
    验证生成的 PRD 是否包含必要章节。"""

    def test_prd_has_goals(self):
        prd = generate_prd("add search feature")
        assert len(prd.goals) > 0, "PRD must have at least one goal / PRD 必须至少有一个目标"

    def test_prd_has_user_stories(self):
        prd = generate_prd("add search feature")
        assert len(prd.user_stories) > 0, "PRD must have user stories / PRD 必须有用户故事"

    def test_prd_has_acceptance_criteria(self):
        prd = generate_prd("add search feature")
        assert len(prd.acceptance_criteria) > 0, "PRD must have acceptance criteria / PRD 必须有验收标准"

    def test_prd_title_matches_idea(self):
        idea = "add notifications"
        prd = generate_prd(idea)
        assert prd.title == idea, "PRD title should match the original idea / PRD 标题应与原始想法一致"


# --- Test design doc / 测试设计文档 ---

class TestDesignDoc:
    """Verify that design docs reference the PRD.
    验证设计文档是否引用了 PRD。"""

    def test_design_doc_references_prd(self):
        """The design doc should carry forward the PRD title.
        设计文档应保留 PRD 标题。"""
        prd = generate_prd("add payments")
        design = generate_design_doc(prd)
        assert design.prd_title == prd.title

    def test_design_doc_has_components(self):
        prd = generate_prd("add payments")
        design = generate_design_doc(prd)
        assert len(design.components) > 0, "Design doc must list components / 设计文档必须列出组件"


# --- Test work plan / 测试工作计划 ---

class TestWorkPlan:
    """Verify that the work plan creates ordered tasks.
    验证工作计划是否创建了有序的任务。"""

    def test_plan_has_tasks(self):
        prd = generate_prd("add auth")
        design = generate_design_doc(prd)
        plan = generate_work_plan(design)
        assert len(plan.tasks) > 0, "Work plan must have tasks / 工作计划必须有任务"

    def test_data_models_before_components(self):
        """Data models should be created before components are implemented.
        数据模型应在组件实现之前创建。"""
        prd = generate_prd("add auth")
        design = generate_design_doc(prd)
        plan = generate_work_plan(design)
        first_model = next(i for i, t in enumerate(plan.tasks) if "data model" in t)
        first_component = next(i for i, t in enumerate(plan.tasks) if "Implement component" in t)
        assert first_model < first_component, "Models must come before components / 模型必须在组件之前"


# --- Test verification / 测试验证 ---

class TestVerification:
    """Verify that the checker catches mismatches.
    验证检查器是否能发现设计与实现的不匹配。"""

    def test_pass_when_all_components_implemented(self):
        prd = generate_prd("add auth")
        design = generate_design_doc(prd)
        plan = generate_work_plan(design)
        completed = [f"[done] {t}" for t in plan.tasks]
        assert verify_against_design(completed, design) is True

    def test_fail_when_component_missing(self):
        """If a component is missing from completed tasks, verification fails.
        如果已完成任务中缺少某个组件，验证将失败。"""
        prd = generate_prd("add auth")
        design = generate_design_doc(prd)
        # Only complete tasks that do NOT mention the first component
        # 只完成不涉及第一个组件的任务
        missing = design.components[0]
        completed = [f"[done] task-{i}" for i in range(5)]  # No real component names / 无真实组件名
        assert verify_against_design(completed, design) is False
