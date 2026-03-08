import os
import pytest
from pathlib import Path
from agentinit.generator import generate_project, add_agent


@pytest.mark.parametrize("framework,llm", [
    ("langgraph",     "openai"),
    ("crewai",        "anthropic"),
    ("autogen",       "groq"),
    ("google_adk",    "openai"),
    ("openai_agents", "openai"),
    ("smolagents",    "gemini"),
    ("langgraph",     "azure"),
    ("langgraph",     "bedrock"),
    ("smolagents",    "gemini"),
])
def test_generate_project(tmp_path, framework, llm):
    project_name = f"test_{framework}_{llm}"
    os.chdir(tmp_path)
    generate_project(project_name, framework, llm)

    project_path = tmp_path / project_name
    assert (project_path / "main.py").exists()
    assert (project_path / "requirements.txt").exists()
    assert (project_path / "agents" / "base_agent.py").exists()
    assert (project_path / "tools" / "sample_tool.py").exists()
    assert (project_path / "config" / "config.yaml").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / "Dockerfile").exists()


def test_duplicate_project(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai")
    result = generate_project("my-project", "langgraph", "openai")
    assert result is False


def test_add_agent(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai")
    os.chdir(tmp_path / "my-project")
    result = add_agent("researcher", "langgraph")
    assert result is True
    assert (Path("agents") / "researcher.py").exists()


def test_add_agent_duplicate(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai")
    os.chdir(tmp_path / "my-project")
    add_agent("researcher", "langgraph")
    result = add_agent("researcher", "langgraph")
    assert result is False