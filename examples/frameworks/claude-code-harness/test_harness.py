"""
Tests for Claude Code Harness workflow simulation.
Claude Code Harness 工作流模拟的测试。

Run with: pytest test_harness.py -v
运行方式: pytest test_harness.py -v

No API keys needed. / 无需 API 密钥。
"""

import pytest
from example_workflow import (
    setup,
    plan,
    work,
    guardrail_check,
    review,
    release,
)


# --- Test setup / 测试设置 ---

def test_setup_creates_valid_config():
    """Setup should return a config with language and guardrail rules.
    设置应返回包含语言和护栏规则的配置。"""
    config = setup("python")
    assert config.language == "python"
    assert len(config.guardrail_rules) >= 1
    assert all(r.name and r.forbidden_pattern for r in config.guardrail_rules)


# --- Test plan / 测试计划 ---

def test_plan_generates_tasks():
    """Plan should generate tasks from requirements.
    计划应根据需求生成任务。"""
    tasks = plan("add user authentication")
    assert len(tasks) >= 1
    for task in tasks:
        assert task.description  # each task has a description / 每个任务有描述
        assert task.file_path    # each task has a file path / 每个任务有文件路径
        assert task.status == "pending"  # starts pending / 初始状态为待处理


# --- Test guardrail / 测试护栏 ---

def test_guardrail_blocks_forbidden_changes():
    """Guardrail should block content matching forbidden patterns.
    护栏应阻止匹配禁止模式的内容。"""
    config = setup("python")
    # Try a direct DB migration (forbidden) / 尝试直接数据库迁移（被禁止）
    passed, message = guardrail_check(config, "bad.sql", "ALTER TABLE users DROP COLUMN email;")
    assert passed is False
    assert "migration" in message.lower() or "迁移" in message


def test_guardrail_blocks_hardcoded_secrets():
    """Guardrail should block hardcoded secrets.
    护栏应阻止硬编码密钥。"""
    config = setup("python")
    passed, message = guardrail_check(config, "config.py", 'SECRET_KEY="abc123"')
    assert passed is False
    assert "secret" in message.lower() or "密钥" in message


def test_guardrail_allows_valid_changes():
    """Guardrail should allow content that does not match any forbidden pattern.
    护栏应允许不匹配任何禁止模式的内容。"""
    config = setup("python")
    passed, message = guardrail_check(config, "models/user.py", "class User:\n    pass\n")
    assert passed is True
    assert message == "OK"


# --- Test review / 测试审查 ---

def test_review_passes_when_all_tasks_done():
    """Review should pass when all tasks are done and all files exist.
    当所有任务完成且所有文件存在时，审查应通过。"""
    tasks = plan("add feature")
    changes = work(tasks)
    assert review(tasks, changes) is True


def test_review_fails_when_tasks_incomplete():
    """Review should fail when tasks are still pending.
    当任务仍在待处理时，审查应失败。"""
    tasks = plan("add feature")
    # Do not call work() — tasks stay pending / 不调用 work() -- 任务保持待处理
    assert review(tasks, {}) is False


# --- Test release / 测试发布 ---

def test_release_succeeds_after_review_passes():
    """Release should succeed when review passed.
    审查通过后，发布应成功。"""
    assert release(review_passed=True) is True


def test_release_blocked_when_review_fails():
    """Release should be blocked when review did not pass.
    审查未通过时，发布应被阻止。"""
    assert release(review_passed=False) is False
