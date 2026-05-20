"""
Superpowers Workflow Simulation / Superpowers 工作流模拟

This script simulates the 7-phase Superpowers methodology to help beginners
understand how it works. It does NOT call the Claude API -- it demonstrates
the mental model using plain Python.

这个脚本模拟 Superpowers 的 7 阶段方法论，帮助初学者理解它的工作原理。
它不调用 Claude API -- 它用纯 Python 演示思维模型。

Phases / 阶段:
  1. Brainstorm  头脑风暴  -- Ask questions, refuse to code
  2. Spec        编写规格  -- Document what to build
  3. Plan        编写计划  -- Break into small tasks
  4. TDD         测试驱动  -- Write test first, then code
  5. Subagent    子代理    -- Dispatch each task with fresh context
  6. Review      审查      -- Verify work against spec
  7. Finalize    最终确认  -- Clean up and deliver
"""

from dataclasses import dataclass, field


# -- Phase 1: Brainstorm / 阶段 1：头脑风暴 --
# The key insight: Claude asks YOU questions instead of guessing.
# 关键洞察：Claude 向你提问，而不是猜测。

class Brainstorm:
    """Generate clarifying questions before any code is written.
    在写任何代码之前生成澄清性问题。"""

    def run(self, feature_request: str) -> list[str]:
        """Return a list of questions that must be answered first.
        返回一个必须先回答的问题列表。"""
        # In real Superpowers, Claude generates these dynamically.
        # 在真正的 Superpowers 中，Claude 会动态生成这些问题。
        return [
            f"What problem does '{feature_request}' solve for users? / 这个功能为用户解决什么问题？",
            "What are the edge cases? / 有哪些边界情况？",
            "What existing code does this interact with? / 这与哪些现有代码交互？",
            "What does success look like? / 成功是什么样的？",
        ]


# -- Phase 2: Spec / 阶段 2：编写规格 --
# The spec is shown in digestible chunks for human approval.
# 规格以易消化的片段展示给人类审批。

@dataclass
class Spec:
    """A specification document generated from brainstorm answers.
    从头脑风暴答案生成的规格文档。"""

    title: str = ""
    requirements: list[str] = field(default_factory=list)
    approved: bool = False

    def generate(self, feature: str, answers: list[str]) -> "Spec":
        """Build a spec from the brainstorm phase.
        从头脑风暴阶段构建规格。"""
        self.title = f"Spec: {feature}"
        self.requirements = [
            f"REQ-1: Core functionality for '{feature}' / 核心功能",
            "REQ-2: Input validation and error handling / 输入验证和错误处理",
            "REQ-3: Unit tests with >80% coverage / 单元测试覆盖率>80%",
        ]
        return self

    def approve(self) -> None:
        """Human approves the spec. Code CANNOT proceed without this.
        人类批准规格。没有批准不能继续写代码。"""
        self.approved = True


# -- Phase 3: Plan / 阶段 3：编写计划 --
# Each task should be completable in 2-5 minutes.
# 每个任务应该在 2-5 分钟内完成。

@dataclass
class Task:
    """A single small task from the plan.
    计划中的一个小任务。"""
    name: str
    description: str
    completed: bool = False


class Plan:
    """Break the spec into small, independent tasks.
    将规格分解为小的、独立的任务。"""

    def create_tasks(self, spec: Spec) -> list[Task]:
        """Generate tasks from an approved spec.
        从已批准的规格生成任务。"""
        if not spec.approved:
            # Superpowers REFUSES to plan until spec is approved!
            # Superpowers 在规格被批准之前拒绝制定计划！
            raise ValueError("Spec must be approved before planning / 规格必须在规划前获得批准")
        return [
            Task("write-tests", "Write failing tests first / 先写失败的测试"),
            Task("implement", "Write code to pass tests / 写代码通过测试"),
            Task("refactor", "Clean up while tests stay green / 在测试保持通过的同时清理代码"),
        ]


# -- Phase 4: TDD / 阶段 4：测试驱动开发 --
# Red -> Green -> Refactor. Always test first.
# 红 -> 绿 -> 重构。始终先写测试。

class TDDCycle:
    """Simulate the Test-Driven Development cycle.
    模拟测试驱动开发循环。"""

    def red(self, test_name: str) -> dict:
        """Write a failing test (RED phase). / 写一个失败的测试（红色阶段）。"""
        return {"test": test_name, "status": "FAIL", "phase": "red"}

    def green(self, test_name: str) -> dict:
        """Write minimal code to pass (GREEN phase). / 写最少的代码通过测试（绿色阶段）。"""
        return {"test": test_name, "status": "PASS", "phase": "green"}

    def refactor(self, test_name: str) -> dict:
        """Improve code while keeping tests green (REFACTOR phase).
        在保持测试通过的同时改进代码（重构阶段）。"""
        return {"test": test_name, "status": "PASS", "phase": "refactor"}


# -- Phase 5: Subagent / 阶段 5：子代理开发 --
# Each task gets a FRESH context. This is the secret sauce.
# 每个任务获得全新的上下文。这是秘诀。

class Subagent:
    """Simulate dispatching a task to a subagent with fresh context.
    模拟将任务分派给具有全新上下文的子代理。"""

    def dispatch(self, task: Task, spec: Spec) -> str:
        """Send a task to a fresh subagent with only the relevant spec.
        将任务发送给一个只有相关规格的新子代理。"""
        # In real Superpowers, this spawns a new Claude session.
        # 在真正的 Superpowers 中，这会生成一个新的 Claude 会话。
        task.completed = True
        return f"Subagent completed: {task.name} (fresh context, no rot! / 全新上下文，无腐烂！)"


# -- Phase 6 & 7: Review and Finalize / 阶段 6 和 7：审查与最终确认 --

class Review:
    """Check that all work matches the spec.
    检查所有工作是否符合规格。"""

    def check(self, spec: Spec, tasks: list[Task]) -> dict:
        all_done = all(t.completed for t in tasks)
        return {
            "spec_approved": spec.approved,
            "all_tasks_complete": all_done,
            "passed": spec.approved and all_done,
        }


# -- Run the full workflow / 运行完整工作流 --

def run_superpowers_workflow(feature: str) -> dict:
    """Execute all 7 phases of the Superpowers methodology.
    执行 Superpowers 方法论的全部 7 个阶段。"""

    print(f"=== Superpowers Workflow: {feature} ===\n")

    # Phase 1: Brainstorm / 头脑风暴
    questions = Brainstorm().run(feature)
    print("Phase 1 - Brainstorm / 头脑风暴:")
    for q in questions:
        print(f"  ? {q}")

    # Phase 2: Spec / 编写规格
    spec = Spec().generate(feature, answers=["simulated answers"])
    spec.approve()
    print(f"\nPhase 2 - Spec approved: {spec.title}")

    # Phase 3: Plan / 编写计划
    tasks = Plan().create_tasks(spec)
    print(f"\nPhase 3 - Plan: {len(tasks)} tasks created")

    # Phase 4: TDD / 测试驱动
    tdd = TDDCycle()
    print("\nPhase 4 - TDD:")
    for result in [tdd.red("test_core"), tdd.green("test_core"), tdd.refactor("test_core")]:
        print(f"  [{result['phase'].upper()}] {result['test']} -> {result['status']}")

    # Phase 5: Subagent / 子代理
    agent = Subagent()
    print("\nPhase 5 - Subagent Development / 子代理开发:")
    for task in tasks:
        msg = agent.dispatch(task, spec)
        print(f"  {msg}")

    # Phase 6 & 7: Review & Finalize / 审查与最终确认
    result = Review().check(spec, tasks)
    print(f"\nPhase 6 - Review: {'PASSED' if result['passed'] else 'FAILED'}")
    print("Phase 7 - Finalize: Done! / 完成！\n")

    return result


if __name__ == "__main__":
    # Example: simulate building a URL shortener
    # 示例：模拟构建一个 URL 缩短器
    run_superpowers_workflow("URL Shortener / URL 缩短器")
