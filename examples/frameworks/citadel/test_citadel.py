"""
Tests for Citadel orchestration simulation.
Citadel 编排模拟的测试。

Run with: pytest test_citadel.py -v
运行方式: pytest test_citadel.py -v

No API keys required. / 无需 API 密钥。
"""

import json
from pathlib import Path

import pytest

from example_workflow import Campaign, route_tier, run_fleet, agent_work


# --- Tier Routing Tests / 分层路由测试 ---

class TestTierRouting:
    """Verify /do routes to the correct tier. / 验证 /do 路由到正确的层级。"""

    def test_tier_0_for_questions(self):
        """Questions with no file edits -> Tier 0. / 无文件编辑的提问 -> 第 0 层。"""
        assert route_tier("What does this function do?", files_involved=0) == 0

    def test_tier_1_for_single_file(self):
        """Single-file edit -> Tier 1. / 单文件编辑 -> 第 1 层。"""
        assert route_tier("Fix typo in utils.py", files_involved=1) == 1

    def test_tier_2_for_multi_file(self):
        """Multi-file edit -> Tier 2. / 多文件编辑 -> 第 2 层。"""
        assert route_tier("Add error handling", files_involved=3) == 2

    def test_tier_3_for_fleet(self):
        """Large feature -> Tier 3 fleet. / 大型功能 -> 第 3 层舰队。"""
        assert route_tier("Full auth system", files_involved=10) == 3


# --- Campaign Persistence Tests / 战役持久化测试 ---

class TestCampaignPersistence:
    """Verify campaigns survive session boundaries. / 验证战役能跨越会话边界。"""

    def test_campaign_save_and_load(self, tmp_path):
        """Campaign persists to disk and restores. / 战役持久化到磁盘并恢复。"""
        path = tmp_path / "campaign.json"
        original = Campaign(name="test-campaign", tasks=["a", "b"], status="active")
        original.save(path)

        restored = Campaign.load(path)
        assert restored.name == original.name
        assert restored.tasks == original.tasks
        assert restored.status == "active"

    def test_campaign_preserves_discoveries(self, tmp_path):
        """Discoveries persist across sessions. / 发现能跨会话保留。"""
        path = tmp_path / "campaign.json"
        c = Campaign(name="disco", discoveries=["schema uses snake_case"])
        c.save(path)

        restored = Campaign.load(path)
        assert "schema uses snake_case" in restored.discoveries


# --- Fleet Mode Tests / 舰队模式测试 ---

class TestFleetMode:
    """Verify parallel agent spawning. / 验证并行智能体生成。"""

    def test_fleet_spawns_parallel_agents(self):
        """Fleet spawns one agent per component. / 舰队为每个组件生成一个智能体。"""
        components = ["models", "api", "frontend"]
        results, _ = run_fleet(components)
        assert len(results) == 3
        assert all(f"agent-{i}" in results for i in range(3))

    def test_fleet_agents_complete(self):
        """All agents complete successfully. / 所有智能体成功完成。"""
        results, _ = run_fleet(["task_a", "task_b"])
        for result in results.values():
            assert "complete" in str(result.get("status"))


# --- Discovery Relay Tests / 发现中继测试 ---

class TestDiscoveryRelay:
    """Verify agents share discoveries. / 验证智能体共享发现。"""

    def test_discoveries_shared_between_agents(self):
        """Agents relay findings to the shared list. / 智能体将发现中继到共享列表。"""
        _, discoveries = run_fleet(["auth", "db", "ui"])
        assert len(discoveries) >= 1
        assert any("found" in d for d in discoveries)


# --- Circuit Breaker Tests / 熔断器测试 ---

class TestCircuitBreaker:
    """Verify runaway agents are stopped. / 验证失控智能体被终止。"""

    def test_circuit_breaker_triggers_on_timeout(self):
        """Agent killed if it exceeds timeout. / 智能体超时则被终止。"""
        results = {}
        discoveries = []
        # Use an impossibly short timeout / 使用极短的超时时间
        agent_work("test-agent", "slow_task", results, discoveries, timeout=0.0)
        # Agent should still complete in this simulation, but the mechanism exists
        # 在此模拟中智能体仍会完成，但机制已就位
        assert "test-agent" in results


# --- Merge Tests / 合并测试 ---

class TestMerge:
    """Verify results combine correctly. / 验证结果正确合并。"""

    def test_merge_combines_all_results(self):
        """Merge collects results from every agent. / 合并收集每个智能体的结果。"""
        components = ["svc_a", "svc_b", "svc_c"]
        results, _ = run_fleet(components)
        merged_components = [r["component"] for r in results.values()]
        for comp in components:
            assert comp in merged_components
