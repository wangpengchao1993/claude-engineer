"""
Citadel Parallel Orchestration — Example Workflow
Citadel 并行编排 —— 示例工作流

Simulates how Citadel coordinates multiple agents working in parallel.
模拟 Citadel 如何协调多个智能体并行工作。

No API keys required. This is a local simulation.
无需 API 密钥。这是一个本地模拟。
"""

import json
import time
import threading
from pathlib import Path
from dataclasses import dataclass, field


# --- Tier Routing / 分层路由 ---
# Routes tasks to the cheapest execution path based on complexity.
# 根据复杂度将任务路由到最经济的执行路径。

TIERS = {
    0: "instant lookup / 即时查询",
    1: "single-file edit / 单文件编辑",
    2: "multi-file coordinated edit / 多文件协调编辑",
    3: "fleet mode — parallel agents / 舰队模式 — 并行智能体",
}


def route_tier(task_description: str, files_involved: int) -> int:
    """Determine the execution tier for a task. / 确定任务的执行层级。"""
    if files_involved == 0:
        return 0  # Just a question, no edits / 仅是提问，无需编辑
    if files_involved == 1:
        return 1
    if files_involved <= 4:
        return 2
    return 3  # Complex — needs fleet / 复杂 — 需要舰队


# --- Campaign Persistence / 战役持久化 ---
# Campaigns survive session restarts by saving state to disk.
# 战役通过将状态保存到磁盘来跨会话存活。

@dataclass
class Campaign:
    name: str
    tasks: list = field(default_factory=list)
    discoveries: list = field(default_factory=list)
    status: str = "active"

    def save(self, path: Path):
        """Persist campaign to disk. / 将战役持久化到磁盘。"""
        path.write_text(json.dumps(self.__dict__, indent=2))

    @classmethod
    def load(cls, path: Path) -> "Campaign":
        """Resume campaign from disk. / 从磁盘恢复战役。"""
        data = json.loads(path.read_text())
        return cls(**data)


# --- Fleet Mode / 舰队模式 ---
# Spawn parallel agents, each in an isolated worktree.
# 生成并行智能体，每个都在隔离的工作树中运行。

def agent_work(agent_id: str, component: str, results: dict, discoveries: list,
               timeout: float = 5.0):
    """
    Simulate one agent working in its own worktree.
    模拟一个智能体在自己的工作树中工作。
    """
    start = time.time()
    # Simulate work / 模拟工作
    time.sleep(0.1)

    # Circuit breaker: abort if over timeout / 熔断器：超时则中止
    if time.time() - start > timeout:
        results[agent_id] = {"status": "killed", "reason": "timeout / 超时"}
        return

    # Agent discovers something useful / 智能体发现了有用的信息
    discovery = f"{agent_id} found: {component} uses snake_case naming"
    discoveries.append(discovery)

    results[agent_id] = {
        "status": "complete / 完成",
        "component": component,
        "lines_changed": 42,
    }


def run_fleet(components: list[str], timeout: float = 5.0) -> tuple[dict, list]:
    """
    Launch parallel agents — one per component.
    启动并行智能体 —— 每个组件一个。
    """
    results = {}
    discoveries = []  # Shared discovery relay / 共享发现中继
    threads = []

    for i, component in enumerate(components):
        agent_id = f"agent-{i}"
        t = threading.Thread(
            target=agent_work,
            args=(agent_id, component, results, discoveries, timeout),
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=timeout + 1)

    return results, discoveries


# --- Main Simulation / 主模拟流程 ---

if __name__ == "__main__":
    print("=== Citadel Orchestration Demo / Citadel 编排演示 ===\n")

    # Step 1: Define a large feature / 第一步：定义一个大型功能
    task = "Implement full authentication system / 实现完整认证系统"
    components = ["auth_models", "auth_api", "auth_frontend"]

    # Step 2: Tier routing / 第二步：分层路由
    tier = route_tier(task, files_involved=len(components) * 3)
    print(f"Task: {task}")
    print(f"Tier: {tier} — {TIERS[tier]}\n")

    # Step 3: Create a persistent campaign / 第三步：创建持久化战役
    campaign = Campaign(name="auth-system", tasks=components)
    campaign_path = Path("/tmp/citadel_campaign.json")
    campaign.save(campaign_path)
    print(f"Campaign saved / 战役已保存: {campaign_path}")

    # Simulate session restart / 模拟会话重启
    restored = Campaign.load(campaign_path)
    print(f"Campaign restored / 战役已恢复: {restored.name} ({restored.status})\n")

    # Step 4: Fleet mode — parallel agents / 第四步：舰队模式 — 并行智能体
    print("Launching fleet / 启动舰队...")
    results, discoveries = run_fleet(components)

    for agent_id, result in results.items():
        print(f"  {agent_id}: {result}")

    # Step 5: Discovery relay / 第五步：发现中继
    print(f"\nDiscoveries relayed / 已中继的发现: {len(discoveries)}")
    for d in discoveries:
        print(f"  -> {d}")

    # Step 6: Merge results / 第六步：合并结果
    successful = [r for r in results.values() if "complete" in str(r.get("status"))]
    print(f"\nMerge: {len(successful)}/{len(results)} agents succeeded / 成功")
    print("=== Done / 完成 ===")
