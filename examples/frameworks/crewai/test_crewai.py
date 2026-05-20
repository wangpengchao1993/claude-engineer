"""
Tests for CrewAI Research Team / CrewAI 研究团队测试
=====================================================

These tests verify agent, task, and crew setup WITHOUT calling any LLM API.
No API keys needed — we use unittest.mock to avoid real API calls.

这些测试验证智能体、任务和团队的设置，不会调用任何大模型API。
不需要API密钥 — 我们使用 unittest.mock 来避免真实的API调用。

Run / 运行:
    pytest test_crewai.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

from crewai import Agent, Task, Crew, Process


# ---------------------------------------------------------------------------
# Test Agent creation / 测试智能体创建
# ---------------------------------------------------------------------------

class TestAgentCreation:
    """Test that agents are created with correct attributes.
    测试智能体是否以正确的属性被创建。"""

    def test_agent_has_role(self):
        """Agent should store its role. / 智能体应保存其角色。"""
        agent = Agent(
            role="Researcher",
            goal="Find information",
            backstory="An experienced researcher.",
        )
        assert agent.role == "Researcher"

    def test_agent_has_goal(self):
        """Agent should store its goal. / 智能体应保存其目标。"""
        agent = Agent(
            role="Writer",
            goal="Write clear articles",
            backstory="A talented writer.",
        )
        assert agent.goal == "Write clear articles"

    def test_agent_has_backstory(self):
        """Agent should store its backstory. / 智能体应保存其背景故事。"""
        agent = Agent(
            role="Editor",
            goal="Improve articles",
            backstory="A meticulous editor with 10 years of experience.",
        )
        assert "meticulous editor" in agent.backstory


# ---------------------------------------------------------------------------
# Test Task creation / 测试任务创建
# ---------------------------------------------------------------------------

class TestTaskCreation:
    """Test that tasks are created and assigned correctly.
    测试任务是否被正确创建和分配。"""

    def test_task_has_description(self):
        """Task should store its description. / 任务应保存其描述。"""
        agent = Agent(role="Researcher", goal="Research", backstory="Expert.")
        task = Task(
            description="Research AI trends",
            expected_output="A report on AI trends.",
            agent=agent,
        )
        assert "AI trends" in task.description

    def test_task_has_expected_output(self):
        """Task should store the expected output. / 任务应保存预期输出。"""
        agent = Agent(role="Writer", goal="Write", backstory="Writer.")
        task = Task(
            description="Write an article",
            expected_output="A 1000-word article in markdown.",
            agent=agent,
        )
        assert "1000-word" in task.expected_output

    def test_task_assigned_to_agent(self):
        """Task should be linked to its agent. / 任务应与其智能体关联。"""
        agent = Agent(role="Editor", goal="Edit", backstory="Editor.")
        task = Task(
            description="Edit the article",
            expected_output="Polished article.",
            agent=agent,
        )
        assert task.agent == agent


# ---------------------------------------------------------------------------
# Test Crew assembly / 测试团队组建
# ---------------------------------------------------------------------------

class TestCrewAssembly:
    """Test that a crew is assembled correctly.
    测试团队是否被正确组建。"""

    def _make_crew(self):
        """Helper: build a small crew. / 辅助方法：构建一个小团队。"""
        r = Agent(role="Researcher", goal="Research", backstory="Researcher.")
        w = Agent(role="Writer", goal="Write", backstory="Writer.")
        t1 = Task(description="Do research", expected_output="Report.", agent=r)
        t2 = Task(description="Write article", expected_output="Article.", agent=w)
        crew = Crew(
            agents=[r, w],
            tasks=[t1, t2],
            process=Process.sequential,
        )
        return crew, [r, w], [t1, t2]

    def test_crew_has_all_agents(self):
        """Crew should contain all assigned agents. / 团队应包含所有指定的智能体。"""
        crew, agents, _ = self._make_crew()
        assert len(crew.agents) == 2

    def test_crew_has_all_tasks(self):
        """Crew should contain all assigned tasks. / 团队应包含所有指定的任务。"""
        crew, _, tasks = self._make_crew()
        assert len(crew.tasks) == 2

    def test_crew_process_is_sequential(self):
        """Crew should use the sequential process. / 团队应使用顺序执行流程。"""
        crew, _, _ = self._make_crew()
        assert crew.process == Process.sequential
