"""
Claude Code Harness — Example Workflow
Claude Code Harness -- 示例工作流

Simulates the full Harness delivery loop:
模拟完整的 Harness 交付循环：
    Setup -> Plan -> Work -> Guardrail Check -> Review -> Release
    设置 -> 计划 -> 开发 -> 护栏检查 -> 审查 -> 发布

No API keys needed. This is a local simulation.
无需 API 密钥。这是本地模拟。
"""

import time
from dataclasses import dataclass, field


# --- Data models / 数据模型 ---

@dataclass
class GuardrailRule:
    """A single guardrail rule. / 单条护栏规则。"""
    name: str
    forbidden_pattern: str  # pattern to block / 要阻止的模式
    message: str


@dataclass
class ProjectConfig:
    """Project configuration created by 'harness setup'. / 由 'harness setup' 创建的项目配置。"""
    language: str
    guardrail_rules: list = field(default_factory=list)


@dataclass
class Task:
    """A single task in the plan. / 计划中的单个任务。"""
    description: str
    file_path: str
    status: str = "pending"  # pending -> done / 待处理 -> 完成


# --- 1. Setup: configure project / 设置：配置项目 ---

def setup(language: str) -> ProjectConfig:
    """Initialize project with guardrails. / 使用护栏初始化项目。"""
    rules = [
        GuardrailRule(
            name="no-direct-db-migration",
            forbidden_pattern="ALTER TABLE",
            message="Direct DB migration forbidden. Use migration tool. / 禁止直接数据库迁移，请使用迁移工具。",
        ),
        GuardrailRule(
            name="no-hardcoded-secrets",
            forbidden_pattern="SECRET_KEY=",
            message="Hardcoded secrets forbidden. Use env vars. / 禁止硬编码密钥，请使用环境变量。",
        ),
    ]
    config = ProjectConfig(language=language, guardrail_rules=rules)
    print(f"[setup] Project configured for {language} with {len(rules)} guardrail rules.")
    print(f"[setup] 项目已配置：语言={language}，护栏规则={len(rules)}条")
    return config


# --- 2. Plan: create tasks / 计划：创建任务 ---

def plan(requirements: str) -> list[Task]:
    """Generate tasks from requirements. / 根据需求生成任务。"""
    tasks = [
        Task(description="Create user model / 创建用户模型", file_path="models/user.py"),
        Task(description="Add auth routes / 添加认证路由", file_path="routes/auth.py"),
        Task(description="Write auth tests / 编写认证测试", file_path="tests/test_auth.py"),
    ]
    print(f"[plan] Created {len(tasks)} tasks for: {requirements}")
    print(f"[plan] 为 '{requirements}' 创建了 {len(tasks)} 个任务")
    return tasks


# --- 3. Work: implement via worker agents / 开发：通过工作代理实现 ---

def work(tasks: list[Task]) -> dict[str, str]:
    """Simulate parallel implementation by worker agents. / 模拟工作代理的并行实现。"""
    changes = {}
    for task in tasks:
        # Simulate worker generating code / 模拟工作代理生成代码
        changes[task.file_path] = f"# Implementation for: {task.description}\nclass UserAuth:\n    pass\n"
        task.status = "done"
        print(f"  [worker] Completed: {task.description}")
    print(f"[work] All {len(tasks)} tasks implemented in parallel.")
    print(f"[work] 所有 {len(tasks)} 个任务已并行实现。")
    return changes


# --- 4. Guardrail check: validate changes / 护栏检查：验证变更 ---

def guardrail_check(config: ProjectConfig, file_path: str, content: str) -> tuple[bool, str]:
    """
    Validate a change against guardrail rules. Simulates sub-10ms Go engine.
    对照护栏规则验证变更。模拟亚10ms的 Go 引擎。
    """
    start = time.perf_counter_ns()
    for rule in config.guardrail_rules:
        if rule.forbidden_pattern in content:
            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
            print(f"  [guardrail] BLOCKED {file_path} in {elapsed_ms:.2f}ms — {rule.message}")
            return False, rule.message
    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
    print(f"  [guardrail] PASSED {file_path} in {elapsed_ms:.2f}ms")
    return True, "OK"


# --- 5. Review: check quality / 审查：检查质量 ---

def review(tasks: list[Task], changes: dict[str, str]) -> bool:
    """Reviewer agent checks implementation matches plan. / 审查代理检查实现是否匹配计划。"""
    all_done = all(t.status == "done" for t in tasks)
    all_files = all(t.file_path in changes for t in tasks)
    passed = all_done and all_files
    status = "PASSED / 通过" if passed else "FAILED / 失败"
    print(f"[review] {status} — {len(tasks)} tasks checked.")
    return passed


# --- 6. Release: ship it / 发布：交付 ---

def release(review_passed: bool) -> bool:
    """Create PR only if review passed. / 仅在审查通过后创建 PR。"""
    if not review_passed:
        print("[release] BLOCKED — review did not pass. / 阻止 -- 审查未通过。")
        return False
    print("[release] PR created and ready for merge. / PR 已创建，准备合并。")
    return True


# --- Main: run the full cycle / 主流程：运行完整循环 ---

if __name__ == "__main__":
    print("=" * 60)
    print("Claude Code Harness — Delivery Loop Simulation")
    print("Claude Code Harness -- 交付循环模拟")
    print("=" * 60)

    # Step 1: Setup / 步骤1：设置
    config = setup("python")

    # Step 2: Plan / 步骤2：计划
    tasks = plan("add user authentication")

    # Step 3: Work / 步骤3：开发
    changes = work(tasks)

    # Step 4: Guardrail checks on valid changes / 步骤4：对有效变更进行护栏检查
    print("\n[guardrail] Checking valid changes... / 检查有效变更...")
    for path, content in changes.items():
        guardrail_check(config, path, content)

    # Step 5: Show guardrail blocking a bad change / 步骤5：展示护栏阻止不良变更
    print("\n[guardrail] Checking a BAD change... / 检查一个不良变更...")
    bad_content = "ALTER TABLE users DROP COLUMN email;"
    guardrail_check(config, "migrations/002.sql", bad_content)

    # Step 6: Review / 步骤6：审查
    passed = review(tasks, changes)

    # Step 7: Release / 步骤7：发布
    release(passed)

    print("\n" + "=" * 60)
    print("Cycle complete! / 循环完成！")
    print("=" * 60)
