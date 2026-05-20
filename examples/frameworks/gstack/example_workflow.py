"""
GStack Workflow Simulation / GStack 工作流模拟

Simulates GStack's role-based engineering team pipeline.
模拟 GStack 的基于角色的工程团队流水线。

Each role reviews a feature with strong, opinionated feedback.
每个角色以有主见的方式审查功能。

No API keys needed -- this is a local simulation.
无需 API 密钥——这是本地模拟。
"""

from dataclasses import dataclass, field


# --- Data Model / 数据模型 ---

@dataclass
class ReviewResult:
    """Result from a role's review / 角色审查的结果"""
    role: str           # Role name / 角色名称
    approved: bool      # Pass or fail / 通过或拒绝
    feedback: str       # Opinionated feedback / 有主见的反馈


@dataclass
class Feature:
    """A feature moving through the GStack pipeline / 通过 GStack 流水线的功能"""
    name: str
    description: str
    code: str = ""
    reviews: list = field(default_factory=list)


# --- Role Reviewers / 角色审查者 ---
# Each role has strong opinions about what "good" looks like.
# 每个角色对"什么是好的"都有坚定的看法。

def ceo_review(feature: Feature) -> ReviewResult:
    """CEO: Is this worth building? / CEO：这值得做吗？"""
    has_user_value = len(feature.description) > 10
    return ReviewResult(
        role="CEO",
        approved=has_user_value,
        feedback="Ships user value -- build it."
        if has_user_value
        else "Too vague. What problem does this solve for users?",
    )


def eng_manager_review(feature: Feature) -> ReviewResult:
    """Eng Manager: Does this fit the architecture? / 工程经理：这符合架构吗？"""
    constraints = {
        "has_name": bool(feature.name),
        "has_description": bool(feature.description),
        "no_conflicts": "hack" not in feature.description.lower(),
    }
    all_pass = all(constraints.values())
    failed = [k for k, v in constraints.items() if not v]
    return ReviewResult(
        role="EngManager",
        approved=all_pass,
        feedback="Architecture constraints satisfied."
        if all_pass
        else f"Constraint violations: {', '.join(failed)}. Fix before proceeding.",
    )


def designer_review(feature: Feature) -> ReviewResult:
    """Designer: Catch AI slop / 设计师：捕捉 AI 水货"""
    # AI slop indicators: generic words that signal template-driven UI
    # AI 水货指标：暗示模板化 UI 的通用词汇
    slop_words = ["lorem ipsum", "click here", "placeholder", "untitled"]
    desc_lower = feature.description.lower()
    found_slop = [w for w in slop_words if w in desc_lower]
    clean = len(found_slop) == 0
    return ReviewResult(
        role="Designer",
        approved=clean,
        feedback="Design looks intentional -- no AI slop detected."
        if clean
        else f"AI slop detected: {found_slop}. Give it personality.",
    )


def code_reviewer_review(feature: Feature) -> ReviewResult:
    """Code Reviewer: Find the 3 AM bug / 代码审查员：找到凌晨三点的 Bug"""
    issues = []
    if "eval(" in feature.code:
        issues.append("eval() is a production incident waiting to happen")
    if "except:" in feature.code:
        issues.append("Bare except catches KeyboardInterrupt -- be specific")
    if "TODO" in feature.code:
        issues.append("TODOs in production code are broken promises")
    return ReviewResult(
        role="CodeReviewer",
        approved=len(issues) == 0,
        feedback="Code looks solid for production."
        if not issues
        else f"Issues found: {'; '.join(issues)}",
    )


def qa_lead_review(feature: Feature) -> ReviewResult:
    """QA Lead: Would this survive real browser testing? / QA：这能通过真实浏览器测试吗？"""
    has_test_plan = "test" in feature.description.lower() or len(feature.code) > 0
    return ReviewResult(
        role="QALead",
        approved=has_test_plan,
        feedback="Test scenarios covered -- ready for browser testing."
        if has_test_plan
        else "No test plan. I need scenarios before I open the browser.",
    )


def security_officer_review(feature: Feature) -> ReviewResult:
    """Security Officer: OWASP + STRIDE audit / 安全官：OWASP + STRIDE 审计"""
    # Check for common OWASP issues / 检查常见的 OWASP 问题
    threats = []
    code = feature.code
    if "password" in code and "hash" not in code:
        threats.append("OWASP A02: Plaintext password detected")
    if "SELECT" in code and "parameterize" not in code and "?" not in code:
        threats.append("OWASP A03: Possible SQL injection")
    if "http://" in code:
        threats.append("STRIDE-Tampering: Use HTTPS, not HTTP")
    return ReviewResult(
        role="SecurityOfficer",
        approved=len(threats) == 0,
        feedback="Zero-trust audit passed. No threats found."
        if not threats
        else f"Threats: {'; '.join(threats)}",
    )


def release_engineer_ship(feature: Feature) -> ReviewResult:
    """Release Engineer: Ship it / 发布工程师：发布"""
    all_approved = all(r.approved for r in feature.reviews)
    return ReviewResult(
        role="ReleaseEngineer",
        approved=all_approved,
        feedback="All reviews passed -- PR shipped!"
        if all_approved
        else "Blocked: not all reviews passed. Fix issues first.",
    )


# --- Pipeline / 流水线 ---

# The full GStack pipeline, in order / 完整的 GStack 流水线（按顺序）
PIPELINE = [
    ceo_review,
    eng_manager_review,
    designer_review,
    code_reviewer_review,
    qa_lead_review,
    security_officer_review,
    release_engineer_ship,
]


def run_pipeline(feature: Feature) -> Feature:
    """Run a feature through the full GStack team / 让功能通过完整的 GStack 团队审查"""
    for reviewer in PIPELINE:
        result = reviewer(feature)
        feature.reviews.append(result)
        print(f"  [{result.role}] {'PASS' if result.approved else 'FAIL'}: {result.feedback}")
    return feature


# --- Demo / 演示 ---

if __name__ == "__main__":
    print("=== GStack Pipeline Demo / GStack 流水线演示 ===\n")

    # Define a feature / 定义一个功能
    feature = Feature(
        name="User Dashboard",
        description="Real-time analytics dashboard with test coverage for key metrics",
        code='def get_metrics(user_id):\n    return db.query("SELECT * FROM metrics WHERE uid=?", user_id)',
    )
    print(f"Feature: {feature.name}")
    print(f"Description: {feature.description}\n")

    # Run through the team / 通过团队审查
    result = run_pipeline(feature)

    # Summary / 总结
    passed = sum(1 for r in result.reviews if r.approved)
    total = len(result.reviews)
    print(f"\nResult: {passed}/{total} roles approved.")
    print("shipped!" if passed == total else "Blocked -- fix issues above.")
