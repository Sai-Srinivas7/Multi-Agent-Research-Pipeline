"""Smoke tests: verify the crew wires up correctly without calling the LLM.

Run with `pytest`, or directly with `python test_smoke.py`.
These tests do not hit the network or the Groq API.
"""
from agents import researcher, fact_checker, tech_writer
from tasks import build_tasks


def test_agents_have_expected_roles():
    assert researcher.role == 'Senior AI Research Analyst'
    assert fact_checker.role == 'AI Capabilities Verifier'
    assert tech_writer.role == 'Technical Content Strategist'


def test_researcher_and_factchecker_have_search_tool():
    assert len(researcher.tools) == 1
    assert len(fact_checker.tools) == 1
    # The writer synthesizes; it should not need a search tool.
    assert len(tech_writer.tools) == 0


def test_build_tasks_returns_full_pipeline():
    tasks = build_tasks("test topic")
    assert len(tasks) == 3
    # The topic should be threaded into the first task's description.
    assert "test topic" in tasks[0].description


if __name__ == "__main__":
    test_agents_have_expected_roles()
    test_researcher_and_factchecker_have_search_tool()
    test_build_tasks_returns_full_pipeline()
    print("All smoke tests passed.")
