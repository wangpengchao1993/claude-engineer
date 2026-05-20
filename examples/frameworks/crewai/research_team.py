"""
CrewAI Research Team Example / CrewAI 研究团队示例
===================================================

This example creates a team of 3 AI agents that collaborate to:
  1. Research a topic  (Researcher / 研究员)
  2. Write an article  (Writer / 作家)
  3. Edit the article  (Editor / 编辑)

本示例创建了一个由3个AI智能体组成的团队，它们协作完成：
  1. 研究一个主题（研究员）
  2. 撰写一篇文章（作家）
  3. 编辑文章（编辑）

Install / 安装:
    pip install crewai

Usage / 使用方法:
    export OPENAI_API_KEY="your-key-here"
    python research_team.py
"""

from crewai import Agent, Task, Crew, Process

# =============================================================================
# Step 1: Define Agents (the "employees" on your team)
# 步骤1：定义智能体（你团队里的"员工"）
#
# Each agent has:
#   - role:      their job title / 职位名称
#   - goal:      what they try to achieve / 他们要达成的目标
#   - backstory: personality & context (this helps the LLM role-play better)
#                性格和背景（这有助于大模型更好地扮演角色）
# =============================================================================

# Agent 1: The Researcher — finds information
# 智能体1：研究员 — 负责查找信息
researcher = Agent(
    role="Senior Research Analyst",           # Job title / 职位
    goal="Find comprehensive and accurate information about the given topic",
    # 目标：找到关于指定主题的全面且准确的信息
    backstory=(
        "You are an experienced research analyst with a keen eye for detail. "
        "You are skilled at finding reliable sources and extracting key insights. "
        "You always verify facts from multiple sources before reporting."
        # 你是一位经验丰富的研究分析师，对细节有敏锐的洞察力。
        # 你擅长寻找可靠的信息来源并提取关键见解。
        # 你总是在报告之前从多个来源验证事实。
    ),
    verbose=True,  # Print what the agent is thinking / 打印智能体的思考过程
)

# Agent 2: The Writer — turns research into an article
# 智能体2：作家 — 将研究转化为文章
writer = Agent(
    role="Content Writer",
    goal="Write a clear, engaging, and well-structured article based on research findings",
    # 目标：基于研究成果撰写一篇清晰、引人入胜、结构良好的文章
    backstory=(
        "You are a talented content writer who excels at making complex topics "
        "accessible to a general audience. You write in a friendly, informative tone "
        "and always structure your articles with clear headings and examples."
        # 你是一位才华横溢的内容作家，擅长将复杂话题
        # 变得通俗易懂。你的写作风格友好、信息丰富，
        # 并且总是使用清晰的标题和示例来组织文章。
    ),
    verbose=True,
)

# Agent 3: The Editor — polishes the final article
# 智能体3：编辑 — 润色最终文章
editor = Agent(
    role="Senior Editor",
    goal="Review and improve the article for clarity, accuracy, and readability",
    # 目标：审查并改进文章的清晰度、准确性和可读性
    backstory=(
        "You are a meticulous editor with years of experience in publishing. "
        "You check for grammar, logical flow, factual accuracy, and overall quality. "
        "You provide constructive feedback and make precise improvements."
        # 你是一位一丝不苟的编辑，拥有多年出版经验。
        # 你检查语法、逻辑流程、事实准确性和整体质量。
        # 你提供建设性的反馈并做出精确的改进。
    ),
    verbose=True,
)

# =============================================================================
# Step 2: Define Tasks (the "assignments" for your employees)
# 步骤2：定义任务（给员工的"工作"）
#
# Each task has:
#   - description:     what to do / 做什么
#   - expected_output: what the result should look like / 结果应该是什么样的
#   - agent:           who does this task / 谁来做这个任务
# =============================================================================

topic = "the current state and future of AI agents in 2025"
# 主题："2025年AI智能体的现状和未来"

# Task 1: Research the topic
# 任务1：研究主题
research_task = Task(
    description=(
        f"Conduct thorough research on: {topic}. "
        "Find key trends, important developments, major players, and future predictions. "
        "Include specific examples and data points where possible."
        # 对指定主题进行深入研究。
        # 找到关键趋势、重要发展、主要参与者和未来预测。
        # 尽可能包含具体的例子和数据。
    ),
    expected_output=(
        "A detailed research report with key findings, organized by subtopic, "
        "including sources and specific data points."
        # 一份详细的研究报告，按子主题组织关键发现，包含来源和具体数据。
    ),
    agent=researcher,
)

# Task 2: Write the article (uses research output)
# 任务2：撰写文章（使用研究成果）
writing_task = Task(
    description=(
        "Using the research findings, write a comprehensive article about "
        f"{topic}. The article should be 800-1000 words, well-structured "
        "with an introduction, main sections, and conclusion."
        # 根据研究成果，撰写一篇关于该主题的综合文章。
        # 文章应为800-1000字，结构清晰，包含引言、主体部分和结论。
    ),
    expected_output=(
        "A polished article of 800-1000 words in markdown format with clear "
        "headings, engaging introduction, and actionable conclusion."
        # 一篇800-1000字的精美文章，使用markdown格式，
        # 有清晰的标题、引人入胜的引言和可操作的结论。
    ),
    agent=writer,
)

# Task 3: Edit the article
# 任务3：编辑文章
editing_task = Task(
    description=(
        "Review the article for grammar, clarity, logical flow, and factual accuracy. "
        "Improve the writing where needed while maintaining the author's voice. "
        "Ensure the article is publication-ready."
        # 审查文章的语法、清晰度、逻辑流程和事实准确性。
        # 在保持作者风格的同时改进需要修改的地方。
        # 确保文章达到可发布状态。
    ),
    expected_output=(
        "The final, publication-ready version of the article with all edits applied."
        # 应用所有编辑后的最终可发布版本。
    ),
    agent=editor,
)

# =============================================================================
# Step 3: Create the Crew (the "team")
# 步骤3：创建团队
#
# Process.sequential means tasks run one after another:
#   research → write → edit
# 顺序执行意味着任务一个接一个地运行：
#   研究 → 写作 → 编辑
# =============================================================================

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # Tasks run in order / 任务按顺序运行
    verbose=True,                # Show progress / 显示进度
)

# =============================================================================
# Step 4: Kick off the crew! / 步骤4：启动团队！
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Starting the Research Team / 启动研究团队")
    print("=" * 60)

    # crew.kickoff() starts the workflow — each agent works on their task in order.
    # crew.kickoff() 启动工作流 — 每个智能体按顺序完成各自的任务。
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("Final Result / 最终结果:")
    print("=" * 60)
    print(result)
