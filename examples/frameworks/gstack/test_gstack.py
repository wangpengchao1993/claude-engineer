"""
Tests for GStack Workflow / GStack 工作流测试

Validates each role's review logic and the full pipeline.
验证每个角色的审查逻辑和完整流水线。

No API keys needed -- pure unit tests.
无需 API 密钥——纯单元测试。

Run: pytest test_gstack.py -v
"""

import pytest

from example_workflow import (
    Feature,
    ceo_review,
    code_reviewer_review,
    designer_review,
    eng_manager_review,
    release_engineer_ship,
    run_pipeline,
    security_officer_review,
)


# --- CEO Tests / CEO 测试 ---

class TestCEOReview:
    """CEO generates a go/no-go decision / CEO 生成通过/不通过决策"""

    def test_approves_clear_value_proposition(self):
        """Feature with clear value gets approved / 有明确价值的功能被批准"""
        feature = Feature(name="Search", description="Full-text search for user documents")
        result = ceo_review(feature)
        assert result.approved is True
        assert result.role == "CEO"

    def test_rejects_vague_description(self):
        """Vague feature gets rejected / 模糊的功能被拒绝"""
        feature = Feature(name="Thing", description="stuff")
        result = ceo_review(feature)
        assert result.approved is False


# --- Eng Manager Tests / 工程经理测试 ---

class TestEngManagerReview:
    """Eng Manager defines architecture constraints / 工程经理定义架构约束"""

    def test_passes_clean_feature(self):
        """Well-defined feature passes constraints / 定义清晰的功能通过约束"""
        feature = Feature(name="Auth", description="OAuth2 login flow")
        result = eng_manager_review(feature)
        assert result.approved is True

    def test_rejects_hack_workarounds(self):
        """Features described as hacks get flagged / 被描述为 hack 的功能被标记"""
        feature = Feature(name="Fix", description="Quick hack to fix the login")
        result = eng_manager_review(feature)
        assert result.approved is False
        assert "no_conflicts" in result.feedback


# --- Designer Tests / 设计师测试 ---

class TestDesignerReview:
    """Designer catches common AI slop issues / 设计师捕捉常见 AI 水货问题"""

    def test_approves_intentional_design(self):
        """Clean description passes / 干净的描述通过"""
        feature = Feature(name="Profile", description="Personalized user profile with avatar")
        result = designer_review(feature)
        assert result.approved is True

    def test_catches_placeholder_text(self):
        """Placeholder text is AI slop / 占位符文本是 AI 水货"""
        feature = Feature(name="Page", description="Lorem ipsum dolor sit amet")
        result = designer_review(feature)
        assert result.approved is False
        assert "lorem ipsum" in str(result.feedback).lower()

    def test_catches_generic_cta(self):
        """Generic CTAs are caught / 通用行动号召被捕获"""
        feature = Feature(name="Button", description="Click here to continue")
        result = designer_review(feature)
        assert result.approved is False


# --- Security Officer Tests / 安全官测试 ---

class TestSecurityOfficerReview:
    """Security Officer runs OWASP audit checks / 安全官运行 OWASP 审计检查"""

    def test_passes_secure_code(self):
        """Secure code passes audit / 安全的代码通过审计"""
        feature = Feature(name="API", description="REST API", code="def handler(req): return ok()")
        result = security_officer_review(feature)
        assert result.approved is True

    def test_flags_plaintext_password(self):
        """Plaintext passwords flagged (OWASP A02) / 明文密码被标记"""
        feature = Feature(name="Login", description="Login", code="password = input()")
        result = security_officer_review(feature)
        assert result.approved is False
        assert "A02" in result.feedback

    def test_flags_http(self):
        """HTTP flagged as tampering risk / HTTP 被标记为篡改风险"""
        feature = Feature(name="Fetch", description="Fetch data", code='url = "http://api.example.com"')
        result = security_officer_review(feature)
        assert result.approved is False
        assert "HTTPS" in result.feedback


# --- Full Pipeline Test / 完整流水线测试 ---

class TestFullPipeline:
    """Full pipeline passes through all roles / 完整流水线通过所有角色"""

    def test_clean_feature_passes_all_roles(self):
        """A well-crafted feature passes every reviewer / 精心设计的功能通过每个审查者"""
        feature = Feature(
            name="Dashboard",
            description="Real-time analytics dashboard with test coverage",
            code='def get_data(uid):\n    return db.query("SELECT * FROM t WHERE id=?", uid)',
        )
        result = run_pipeline(feature)
        # Should have one review per pipeline step / 每个流水线步骤应有一个审查
        assert len(result.reviews) == 7
        # All roles should approve / 所有角色都应批准
        for review in result.reviews:
            assert review.approved is True, f"{review.role} failed: {review.feedback}"

    def test_bad_feature_gets_blocked(self):
        """A feature with issues gets blocked by release engineer / 有问题的功能被发布工程师拦截"""
        feature = Feature(
            name="Hack",
            description="Quick hack with placeholder text",
            code="password = input(); eval(data)",
        )
        result = run_pipeline(feature)
        # Release engineer should block / 发布工程师应该拦截
        release_review = result.reviews[-1]
        assert release_review.role == "ReleaseEngineer"
        assert release_review.approved is False
