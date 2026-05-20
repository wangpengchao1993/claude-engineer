"""
BMAD-METHOD Example Workflow / BMAD-METHOD 示例工作流
=====================================================

Simulates a full agile sprint using the BMAD multi-agent team.
Each agent (PM, Architect, Developer, QA) processes its phase and
passes output to the next agent -- just like a real sprint.

模拟使用 BMAD 多智能体团队的完整敏捷冲刺。
每个智能体（产品经理、架构师、开发者、QA）处理各自阶段，
并将产出传递给下一个智能体——就像真正的冲刺一样。

No API keys needed -- this is a local simulation.
无需 API 密钥——这是本地模拟。
"""

from dataclasses import dataclass, field


# --- Agent base class / 智能体基类 ---

@dataclass
class Agent:
    """Base class for all BMAD agents. / 所有 BMAD 智能体的基类。"""

    role: str  # e.g. "Product Manager" / 例如 "产品经理"
    goal: str  # What this agent aims to produce / 该智能体的目标产出

    def process(self, input_data: dict) -> dict:
        """Process input and return output. Override in subclasses.
        处理输入并返回产出。子类需重写此方法。"""
        raise NotImplementedError


# --- Concrete agents / 具体智能体 ---

class ProductManager(Agent):
    """Gathers requirements and writes user stories from an idea.
    从想法中收集需求并编写用户故事。"""

    def __init__(self):
        super().__init__(role="Product Manager", goal="Define requirements")

    def process(self, input_data: dict) -> dict:
        idea = input_data.get("idea", "")
        # Simulate generating user stories / 模拟生成用户故事
        stories = [
            f"As a user, I want to {idea.lower()} so that I can be more productive",
            f"As an admin, I want to manage {idea.lower()} settings",
            f"As a user, I want notifications about {idea.lower()} updates",
        ]
        return {"requirements": f"PRD for: {idea}", "user_stories": stories}


class Architect(Agent):
    """Designs system architecture and picks a tech stack.
    设计系统架构并选择技术栈。"""

    def __init__(self):
        super().__init__(role="Architect", goal="Design architecture")

    def process(self, input_data: dict) -> dict:
        requirements = input_data.get("requirements", "")
        stories = input_data.get("user_stories", [])
        return {
            "architecture": f"Microservices design for: {requirements}",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Redis"],
            "components": [f"service_{i}" for i in range(len(stories))],
        }


class Developer(Agent):
    """Implements features based on the architecture.
    根据架构实现功能。"""

    def __init__(self):
        super().__init__(role="Developer", goal="Implement features")

    def process(self, input_data: dict) -> dict:
        components = input_data.get("components", [])
        tech_stack = input_data.get("tech_stack", [])
        # Simulate code generation / 模拟代码生成
        code_files = {f"{comp}.py": f"# Implementation of {comp}" for comp in components}
        return {"code_files": code_files, "tech_used": tech_stack}


class QAEngineer(Agent):
    """Writes and runs tests to verify quality.
    编写并运行测试以验证质量。"""

    def __init__(self):
        super().__init__(role="QA Engineer", goal="Verify quality")

    def process(self, input_data: dict) -> dict:
        code_files = input_data.get("code_files", {})
        test_results = {f"test_{name}": "PASSED" for name in code_files}
        return {"test_results": test_results, "all_passed": True}


# --- Sprint runner / 冲刺运行器 ---

def run_sprint(idea: str) -> dict:
    """Run a full BMAD agile sprint from idea to tested software.
    执行一次完整的 BMAD 敏捷冲刺，从想法到已测试的软件。"""

    agents = [ProductManager(), Architect(), Developer(), QAEngineer()]
    context = {"idea": idea}  # Start with just the idea / 从想法开始

    for agent in agents:
        print(f"[{agent.role}] Processing... / 处理中...")
        output = agent.process(context)
        context.update(output)  # Pass output to next agent / 将产出传递给下一个智能体
        print(f"[{agent.role}] Done. Output keys: {list(output.keys())}")

    return context


# --- Main / 主程序 ---

if __name__ == "__main__":
    # Define a product idea / 定义一个产品想法
    idea = "Build a task management dashboard"

    print("=" * 60)
    print("BMAD Sprint Simulation / BMAD 冲刺模拟")
    print("=" * 60)
    print(f"Idea / 想法: {idea}\n")

    result = run_sprint(idea)

    print("\n" + "=" * 60)
    print("Sprint Complete! / 冲刺完成！")
    print("=" * 60)
    print(f"User stories / 用户故事: {len(result['user_stories'])}")
    print(f"Architecture / 架构: {result['architecture']}")
    print(f"Code files / 代码文件: {list(result['code_files'].keys())}")
    print(f"Tests passed / 测试通过: {result['all_passed']}")
