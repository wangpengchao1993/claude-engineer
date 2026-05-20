"""
Spec-Kit Workflow Simulation / Spec-Kit 工作流模拟

Demonstrates the 6-phase Spec-Driven Development process.
演示 6 阶段规格驱动开发流程。

Each phase is a function that takes the previous phase's output,
enforcing the sequential discipline that Spec-Kit requires.
每个阶段是一个函数，接收上一阶段的输出，强制执行 Spec-Kit 要求的顺序纪律。
"""

from dataclasses import dataclass, field


# --- Data models for each phase / 每个阶段的数据模型 ---

@dataclass
class Constitution:
    """Non-negotiable project rules / 不可违背的项目规则"""
    technologies: dict  # Language, framework, DB / 语言、框架、数据库
    testing: dict       # Testing requirements / 测试要求
    style: dict         # Code style rules / 代码风格规则
    constraints: list   # Hard constraints / 硬约束条件


@dataclass
class Specification:
    """Project requirements / 项目需求"""
    features: list          # Feature descriptions / 功能描述
    non_functional: list    # Performance, security, etc. / 性能、安全等
    ambiguities: list       # Unresolved questions / 未解决的问题


@dataclass
class Plan:
    """Implementation plan / 实施计划"""
    steps: list             # Ordered implementation steps / 有序的实施步骤
    dependencies: dict      # Step dependencies / 步骤依赖关系


@dataclass
class Task:
    """A single work item / 单个工作项"""
    name: str
    description: str
    status: str = "pending"  # pending, in_progress, done / 待处理、进行中、完成


# --- Phase functions / 阶段函数 ---

def phase1_constitution(project_idea: str) -> Constitution:
    """Phase 1: Define non-negotiable rules / 阶段 1: 定义不可违背的规则"""
    print(f"\n[Phase 1: Constitution] Project: {project_idea}")
    print("[阶段 1: 宪法] 定义项目原则和约束...")
    return Constitution(
        technologies={"language": "Python 3.12", "framework": "FastAPI", "database": "SQLite"},
        testing={"required": True, "min_coverage": 80, "framework": "pytest"},
        style={"formatter": "black", "linter": "ruff"},
        constraints=["All endpoints need auth", "Type hints required", "No global state"],
    )


def phase2_specify(constitution: Constitution) -> Specification:
    """Phase 2: Outline requirements based on constitution / 阶段 2: 基于宪法概述需求"""
    print("\n[Phase 2: Specify] Creating requirements within constitution bounds...")
    print("[阶段 2: 规格说明] 在宪法约束内创建需求...")
    lang = constitution.technologies["language"]
    return Specification(
        features=[
            f"REST API built with {lang}",
            "User registration and login",
            "Task CRUD operations",
        ],
        non_functional=["Response time < 200ms", "99.9% uptime"],
        ambiguities=["Should tasks support attachments?", "What auth method: JWT or session?"],
    )


def phase3_clarify(spec: Specification) -> Specification:
    """Phase 3: Resolve ambiguities / 阶段 3: 解决歧义"""
    print("\n[Phase 3: Clarify] Resolving ambiguous requirements...")
    print("[阶段 3: 澄清] 解决模糊的需求...")
    resolutions = {
        "Should tasks support attachments?": "No, text-only for v1 / 否, v1 仅文本",
        "What auth method: JWT or session?": "JWT tokens / JWT 令牌",
    }
    for question, answer in resolutions.items():
        print(f"  Q: {question}")
        print(f"  A: {answer}")
    # Return updated spec with ambiguities resolved / 返回已解决歧义的更新规格
    spec.ambiguities = []
    spec.features.append("JWT-based authentication")
    return spec


def phase4_plan(spec: Specification, constitution: Constitution) -> Plan:
    """Phase 4: Create implementation plan / 阶段 4: 创建实施计划"""
    print("\n[Phase 4: Plan] Building implementation plan from spec...")
    print("[阶段 4: 规划] 从规格构建实施计划...")
    db = constitution.technologies["database"]
    return Plan(
        steps=[
            f"Set up {db} schema",
            "Implement auth module (JWT)",
            "Build task CRUD endpoints",
            "Add input validation",
            "Write tests (min coverage: {0}%)".format(constitution.testing["min_coverage"]),
        ],
        dependencies={"Implement auth module (JWT)": [f"Set up {db} schema"]},
    )


def phase5_tasks(plan: Plan) -> list[Task]:
    """Phase 5: Break plan into tasks / 阶段 5: 将计划拆分为任务"""
    print("\n[Phase 5: Tasks] Breaking plan into work items...")
    print("[阶段 5: 任务拆分] 将计划拆分为具体工作项...")
    tasks = [Task(name=f"task-{i+1}", description=step) for i, step in enumerate(plan.steps)]
    for t in tasks:
        print(f"  [{t.status}] {t.name}: {t.description}")
    return tasks


def phase6_implement(tasks: list[Task]) -> list[Task]:
    """Phase 6: Execute each task / 阶段 6: 执行每个任务"""
    print("\n[Phase 6: Implement] Executing tasks in order...")
    print("[阶段 6: 执行实现] 按顺序执行任务...")
    for task in tasks:
        task.status = "done"
        print(f"  [DONE / 完成] {task.name}: {task.description}")
    return tasks


# --- Run the full workflow / 运行完整工作流 ---

def run_speckit_workflow():
    """Run all 6 phases in sequence / 按顺序运行全部 6 个阶段"""
    project = "Task Management API / 任务管理 API"
    print("=" * 60)
    print("Spec-Kit Workflow Simulation / Spec-Kit 工作流模拟")
    print("=" * 60)

    constitution = phase1_constitution(project)
    spec = phase2_specify(constitution)
    clarified_spec = phase3_clarify(spec)
    plan = phase4_plan(clarified_spec, constitution)
    tasks = phase5_tasks(plan)
    completed = phase6_implement(tasks)

    done = sum(1 for t in completed if t.status == "done")
    print(f"\n{'=' * 60}")
    print(f"Result: {done}/{len(completed)} tasks completed / 结果: {done}/{len(completed)} 个任务完成")
    print("Spec-Kit workflow finished successfully! / Spec-Kit 工作流成功完成!")
    return completed


if __name__ == "__main__":
    run_speckit_workflow()
