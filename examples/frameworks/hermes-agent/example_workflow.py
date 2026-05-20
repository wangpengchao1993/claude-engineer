"""
Hermes Agent — Self-Improvement Loop Simulation
Hermes Agent — 自改进循环模拟

This script demonstrates how Hermes learns from each task,
improves its skills, and remembers context across sessions.

本脚本演示 Hermes 如何从每个任务中学习、改进技能并跨会话记忆上下文。
"""


# === Skill: starts at v1, evolves as it learns / 技能：从 v1 开始，随学习进化 ===
class Skill:
    """A self-improving skill. / 一个自改进技能。"""

    def __init__(self, name: str):
        self.name = name
        self.version = 1
        self.patterns: list[str] = []  # Learned patterns / 已学模式
        self.success_rate = 0.5  # Baseline performance / 基线性能

    def apply(self, task: str) -> dict:
        """Execute the skill on a task. / 在任务上执行技能。"""
        # More learned patterns → better performance / 学到的模式越多 → 性能越好
        bonus = len(self.patterns) * 0.1
        score = min(self.success_rate + bonus, 1.0)
        return {
            "task": task,
            "score": round(score, 2),
            "skill_version": f"v{self.version}",
            "patterns_used": len(self.patterns),
        }

    def learn(self, pattern: str):
        """Learn a new pattern and evolve. / 学习新模式并进化。"""
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            self.version += 1  # Skill evolves! / 技能进化！
            print(f"  [LEARN/学习] Skill '{self.name}' learned: '{pattern}' → now v{self.version}")


# === Persistent Memory: survives across sessions / 持久记忆：跨会话保留 ===
class Memory:
    """Persistent memory store. / 持久记忆存储。"""

    def __init__(self):
        self.store: dict[str, str] = {}

    def remember(self, key: str, value: str):
        """Save a fact. / 保存一条事实。"""
        self.store[key] = value

    def recall(self, key: str) -> str | None:
        """Retrieve a fact. / 检索一条事实。"""
        return self.store.get(key)


# === Learning Loop: do → evaluate → learn → improve / 学习循环：执行→评估→学习→改进 ===
def evaluate_result(result: dict) -> list[str]:
    """Evaluate a task result and extract patterns. / 评估任务结果并提取模式。"""
    patterns = []
    if result["score"] >= 0.7:
        patterns.append("high_confidence_approach")
    if result["score"] < 0.7:
        patterns.append("needs_more_context")
    if "refactor" in result["task"].lower():
        patterns.append("code_structure_awareness")
    if "test" in result["task"].lower():
        patterns.append("test_driven_pattern")
    return patterns


def run_learning_loop():
    """Main demo: run the full self-improvement loop. / 主演示：运行完整的自改进循环。"""

    print("=" * 60)
    print("Hermes Agent — Self-Improvement Loop Demo")
    print("Hermes Agent — 自改进循环演示")
    print("=" * 60)

    # Initialize agent components / 初始化智能体组件
    skill = Skill(name="code_assistant")
    memory = Memory()

    # Tasks the agent will process / 智能体将处理的任务
    tasks = [
        "Write a Python function to parse JSON",       # Task 1 / 任务 1
        "Refactor the parser for edge cases",           # Task 2 / 任务 2
        "Write tests for the refactored parser",        # Task 3 / 任务 3
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} / 任务 {i}: {task} ---")

        # Step 1: Execute / 步骤 1：执行
        result = skill.apply(task)
        print(f"  [EXEC/执行] Score: {result['score']} | Skill: {result['skill_version']}")

        # Step 2: Evaluate / 步骤 2：评估
        new_patterns = evaluate_result(result)

        # Step 3: Learn / 步骤 3：学习
        for pattern in new_patterns:
            skill.learn(pattern)

        # Step 4: Remember / 步骤 4：记忆
        memory.remember(f"task_{i}_score", str(result["score"]))
        memory.remember(f"task_{i}_version", result["skill_version"])

    # Show evolution summary / 显示进化摘要
    print(f"\n{'=' * 60}")
    print("Evolution Summary / 进化摘要")
    print(f"{'=' * 60}")
    print(f"  Skill version / 技能版本: v1 → v{skill.version}")
    print(f"  Patterns learned / 已学模式: {skill.patterns}")
    print(f"  Final score / 最终分数: {skill.apply('any task')['score']}")

    # Show persistent memory / 显示持久记忆
    print(f"\nPersistent Memory / 持久记忆:")
    for key, value in memory.store.items():
        print(f"  {key} = {value}")

    # Simulate "new session" — memory persists / 模拟"新会话" — 记忆保留
    print(f"\n--- New Session (memory persists) / 新会话（记忆保留） ---")
    recalled = memory.recall("task_1_score")
    print(f"  Recalled task_1_score from previous session: {recalled}")
    print(f"  从上一会话回忆 task_1_score: {recalled}")


if __name__ == "__main__":
    run_learning_loop()
