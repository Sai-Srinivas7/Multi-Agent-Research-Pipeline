import groq_patch  # noqa: F401  -- applies the Groq cache_breakpoint fix on import
from crewai import Agent, LLM

from config import GROQ_MODEL
from tools import search_tool

llm = LLM(model=GROQ_MODEL)

researcher = Agent(
    role='Senior AI Research Analyst',
    goal='Uncover the absolute newest AI frameworks, models, and industry improvements.',
    backstory='You are a world-class AI researcher working at a top tech think-tank. Your expertise lies in finding cutting-edge AI advancements before they hit the mainstream media.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

fact_checker = Agent(
    role='AI Capabilities Verifier',
    goal='Verify the use-cases and capabilities of the AI improvements found by the researcher.',
    backstory='You are a meticulous technical auditor. You take bold claims about new AI models and verify what they can actually do, finding concrete real-world use-cases.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

tech_writer = Agent(
    role='Technical Content Strategist',
    goal='Create a comprehensive, easy-to-understand Markdown report on the newest AI improvements, their use-cases, and learning paths.',
    backstory='You are a renowned technical writer who specializes in making complex AI topics accessible to developers and engineers. You excel at creating structured learning paths.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)
