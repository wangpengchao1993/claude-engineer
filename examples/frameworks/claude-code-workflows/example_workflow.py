"""
Claude Code Workflows -- Example: Full Lifecycle Simulation
Claude Code Workflows -- 示例：完整生命周期模拟

This script walks through every stage of the workflow pipeline
for a single feature idea. No API keys required -- all steps
are simulated locally so you can see the shape of the process.

本脚本模拟单个功能想法的完整工作流流水线。
无需 API 密钥 -- 所有步骤在本地模拟，让你了解整个流程的全貌。
"""

from dataclasses import dataclass, field
from typing import List


# --- Data models / 数据模型 ---

@dataclass
class PRD:
    """Product Requirements Document / 产品需求文档"""
    title: str
    goals: List[str]
    user_stories: List[str]
    acceptance_criteria: List[str]


@dataclass
class DesignDoc:
    """Architecture design document / 架构设计文档"""
    prd_title: str
    components: List[str]
    api_endpoints: List[str]
    data_models: List[str]


@dataclass
class WorkPlan:
    """Ordered implementation tasks / 有序实现任务"""
    tasks: List[str] = field(default_factory=list)


# --- Step 1: Complexity analysis / 第一步：复杂度分析 ---

def analyze_complexity(idea: str) -> str:
    """Determine task complexity from the idea description.
    根据想法描述判断任务复杂度。"""
    keywords_large = ["authentication", "payment", "migration", "认证", "支付"]
    keywords_small = ["typo", "rename", "color", "拼写", "重命名"]
    idea_lower = idea.lower()
    if any(k in idea_lower for k in keywords_large):
        return "medium"  # Could be large; simplified for demo / 简化演示
    if any(k in idea_lower for k in keywords_small):
        return "small"
    return "medium"


# --- Step 2: Generate PRD / 第二步：生成 PRD ---

def generate_prd(idea: str) -> PRD:
    """Create a product requirements document from the idea.
    根据想法创建产品需求文档。"""
    return PRD(
        title=idea,
        goals=[f"Implement {idea} securely", f"Provide clear UX for {idea}"],
        user_stories=[f"As a user, I can {idea} so that my account is protected"],
        acceptance_criteria=["All endpoints require valid tokens", "Tests pass at >90% coverage"],
    )


# --- Step 3: Generate UI Spec / 第三步：生成 UI 规格说明 ---

def generate_ui_spec(prd: PRD) -> dict:
    """Produce a UI specification from the PRD (for frontend features).
    根据 PRD 生成 UI 规格说明（适用于前端功能）。"""
    return {"screens": ["Login Page", "Registration Page"], "components": ["AuthForm", "TokenRefreshBanner"]}


# --- Step 4: Generate Design Doc / 第四步：生成设计文档 ---

def generate_design_doc(prd: PRD) -> DesignDoc:
    """Create an architecture design document referencing the PRD.
    创建引用 PRD 的架构设计文档。"""
    return DesignDoc(
        prd_title=prd.title,
        components=["AuthService", "TokenManager", "UserRepository"],
        api_endpoints=["POST /auth/login", "POST /auth/register", "POST /auth/refresh"],
        data_models=["User", "Session", "RefreshToken"],
    )


# --- Step 5: Generate Work Plan / 第五步：生成工作计划 ---

def generate_work_plan(design: DesignDoc) -> WorkPlan:
    """Break the design into ordered tasks.
    将设计拆分为有序的任务。"""
    plan = WorkPlan()
    for model in design.data_models:
        plan.tasks.append(f"Create data model: {model}")
    for component in design.components:
        plan.tasks.append(f"Implement component: {component}")
    for endpoint in design.api_endpoints:
        plan.tasks.append(f"Wire up endpoint: {endpoint}")
    plan.tasks.append("Write unit and integration tests")
    return plan


# --- Step 6: Implement / 第六步：实现 ---

def implement_tasks(plan: WorkPlan) -> List[str]:
    """Simulate implementing each task in order.
    模拟按顺序实现每个任务。"""
    completed = []
    for task in plan.tasks:
        completed.append(f"[done] {task}")  # Simulated / 模拟完成
    return completed


# --- Step 7: Run tests / 第七步：运行测试 ---

def run_tests(completed_tasks: List[str]) -> bool:
    """Simulate running tests -- pass if all tasks are done.
    模拟运行测试 -- 所有任务完成则通过。"""
    return all(t.startswith("[done]") for t in completed_tasks)


# --- Step 8: Verify against design doc / 第八步：对照设计文档验证 ---

def verify_against_design(completed_tasks: List[str], design: DesignDoc) -> bool:
    """Check that every design component was implemented.
    检查每个设计组件是否都已实现。"""
    for component in design.components:
        if not any(component in t for t in completed_tasks):
            return False
    return True


# --- Main: run the full pipeline / 主流程：运行完整流水线 ---

if __name__ == "__main__":
    idea = "add user authentication"  # Feature idea / 功能想法
    print(f"Feature idea / 功能想法: {idea}\n")

    complexity = analyze_complexity(idea)
    print(f"1. Complexity / 复杂度: {complexity}")

    prd = generate_prd(idea)
    print(f"2. PRD generated / PRD 已生成: {prd.title}  ({len(prd.goals)} goals)")

    ui_spec = generate_ui_spec(prd)
    print(f"3. UI Spec / UI 规格: {len(ui_spec['screens'])} screens, {len(ui_spec['components'])} components")

    design = generate_design_doc(prd)
    print(f"4. Design Doc / 设计文档: {len(design.components)} components, {len(design.api_endpoints)} endpoints")

    plan = generate_work_plan(design)
    print(f"5. Work Plan / 工作计划: {len(plan.tasks)} tasks")

    completed = implement_tasks(plan)
    print(f"6. Implementation / 实现: {len(completed)} tasks completed")

    tests_pass = run_tests(completed)
    print(f"7. Tests / 测试: {'PASS / 通过' if tests_pass else 'FAIL / 失败'}")

    verified = verify_against_design(completed, design)
    print(f"8. Verification / 验证: {'PASS / 通过' if verified else 'FAIL / 失败'}")

    print("\nPipeline complete! / 流水线完成！")
