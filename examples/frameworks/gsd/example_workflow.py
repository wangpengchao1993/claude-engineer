"""
GSD (Get Shit Done) Framework -- Context Rot Simulation
GSD（把事做完）框架 -- 上下文腐烂模拟

Demonstrates how context rot degrades AI coding sessions and how GSD's
sub-agent architecture solves it.

演示上下文腐烂如何降低 AI 编程会话质量，以及 GSD 的子代理架构如何解决它。

No API keys required -- pure simulation.
无需 API 密钥 -- 纯模拟。
"""

import random

random.seed(42)


# --- Context rot model / 上下文腐烂模型 ---

def simulate_accuracy(token_count: int) -> float:
    """Simulate accuracy dropping as context grows.
    模拟随着上下文增长，准确率下降。

    At 0 tokens: ~98% accuracy. At 100k tokens: ~55% accuracy.
    0 token 时约 98% 准确率。100k token 时约 55% 准确率。
    """
    base = 0.98
    decay = token_count / 200_000  # gradual decay / 逐渐衰减
    noise = random.uniform(-0.03, 0.03)
    return max(0.30, min(1.0, base - decay + noise))


def simulate_long_session(num_tasks: int = 8) -> list[dict]:
    """Simulate a long coding session WITHOUT GSD -- context grows continuously.
    模拟没有 GSD 的长编程会话 -- 上下文持续增长。
    """
    results = []
    token_count = 0

    for i in range(num_tasks):
        # Each task adds tokens to the session / 每个任务向会话添加 token
        tokens_added = random.randint(8_000, 15_000)
        token_count += tokens_added

        accuracy = simulate_accuracy(token_count)
        passed = random.random() < accuracy

        results.append({
            "task": f"Task-{i + 1}",
            "tokens_total": token_count,
            "accuracy": accuracy,
            "passed_verification": passed,
        })

    return results


# --- GSD sub-agent model / GSD 子代理模型 ---

class SubAgent:
    """A GSD sub-agent: spawned with fresh context for one focused task.
    GSD 子代理：为一个聚焦任务以全新上下文生成。
    """

    def __init__(self, task_name: str, spec_tokens: int, relevant_file_tokens: int):
        # Sub-agent context = spec + relevant files only (NOT full history)
        # 子代理上下文 = 仅规格 + 相关文件（不是完整历史）
        self.task_name = task_name
        self.context_tokens = spec_tokens + relevant_file_tokens
        self.accuracy = simulate_accuracy(self.context_tokens)

    def execute(self) -> dict:
        """Run the task and return result. / 执行任务并返回结果。"""
        passed = random.random() < self.accuracy
        return {
            "task": self.task_name,
            "context_tokens": self.context_tokens,
            "accuracy": self.accuracy,
            "passed_verification": passed,
        }


def verify_task(result: dict, spec: str) -> bool:
    """Automatic verification step -- checks output against spec.
    自动验证步骤 -- 检查输出是否符合规格。

    In real GSD this runs tests, linters, and spec conformance checks.
    在真正的 GSD 中，这会运行测试、linter 和规格符合性检查。
    """
    return result["passed_verification"] and len(spec) > 0


def simulate_gsd_session(num_tasks: int = 8) -> list[dict]:
    """Simulate a session WITH GSD -- each task gets a fresh sub-agent.
    模拟使用 GSD 的会话 -- 每个任务获得一个全新子代理。
    """
    results = []

    for i in range(num_tasks):
        spec_tokens = random.randint(500, 1_500)        # task spec / 任务规格
        file_tokens = random.randint(2_000, 5_000)       # relevant files / 相关文件

        # Fresh sub-agent with focused context / 全新子代理，聚焦上下文
        agent = SubAgent(f"Task-{i + 1}", spec_tokens, file_tokens)
        result = agent.execute()

        # Automatic verification / 自动验证
        spec = f"Spec for task {i + 1}: implement feature and pass tests"
        result["verified"] = verify_task(result, spec)

        results.append(result)

    return results


# --- Run comparison / 运行对比 ---

if __name__ == "__main__":
    print("=" * 65)
    print("WITHOUT GSD -- Long session, growing context")
    print("没有 GSD -- 长会话，上下文持续增长")
    print("=" * 65)

    no_gsd = simulate_long_session()
    for r in no_gsd:
        status = "PASS / 通过" if r["passed_verification"] else "FAIL / 失败"
        print(
            f"  {r['task']:>8}  |  tokens: {r['tokens_total']:>6,}  |  "
            f"accuracy: {r['accuracy']:.0%}  |  {status}"
        )

    avg_no_gsd = sum(r["accuracy"] for r in no_gsd) / len(no_gsd)
    print(f"\n  Average accuracy / 平均准确率: {avg_no_gsd:.0%}")

    print()
    print("=" * 65)
    print("WITH GSD -- Fresh sub-agent per task, focused context")
    print("使用 GSD -- 每个任务全新子代理，聚焦上下文")
    print("=" * 65)

    with_gsd = simulate_gsd_session()
    for r in with_gsd:
        status = "PASS / 通过" if r["verified"] else "FAIL / 失败"
        print(
            f"  {r['task']:>8}  |  tokens: {r['context_tokens']:>6,}  |  "
            f"accuracy: {r['accuracy']:.0%}  |  {status}"
        )

    avg_gsd = sum(r["accuracy"] for r in with_gsd) / len(with_gsd)
    print(f"\n  Average accuracy / 平均准确率: {avg_gsd:.0%}")

    print()
    print("-" * 65)
    improvement = avg_gsd - avg_no_gsd
    print(f"GSD improvement / GSD 提升: +{improvement:.0%} average accuracy")
    print(
        "Key insight: fresh sub-agents never accumulate context rot."
    )
    print(
        "关键洞察：全新子代理永远不会累积上下文腐烂。"
    )
