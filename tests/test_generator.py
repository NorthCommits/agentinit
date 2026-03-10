import os
import pytest
from pathlib import Path
from agentinit.generator import generate_project, add_agent


@pytest.mark.parametrize("framework,llm,pm", [
    ("langgraph",     "openai",    "pip"),
    ("crewai",        "anthropic", "pip"),
    ("autogen",       "groq",      "pip"),
    ("google_adk",    "openai",    "pip"),
    ("openai_agents", "openai",    "pip"),
    ("smolagents",    "gemini",    "pip"),
    ("langgraph",     "azure",     "pip"),
    ("langgraph",     "bedrock",   "pip"),
    ("langgraph",     "openai",    "uv"),
    ("crewai",        "anthropic", "uv"),
    ("smolagents",    "gemini",    "uv"),
])
def test_generate_project(tmp_path, framework, llm, pm):
    project_name = f"test_{framework}_{llm}_{pm}"
    os.chdir(tmp_path)
    generate_project(project_name, framework, llm, pm)

    project_path = tmp_path / project_name
    assert (project_path / "main.py").exists()
    assert (project_path / "agents" / "base_agent.py").exists()
    assert (project_path / "tools" / "sample_tool.py").exists()
    assert (project_path / "config" / "config.yaml").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / "Dockerfile").exists()

    if pm == "pip":
        assert (project_path / "requirements.txt").exists()
    else:
        assert (project_path / "pyproject.toml").exists()


def test_duplicate_project(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai", "pip")
    result = generate_project("my-project", "langgraph", "openai", "pip")
    assert result is False


def test_add_agent(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai", "pip")
    os.chdir(tmp_path / "my-project")
    result = add_agent("researcher", "langgraph")
    assert result is True
    assert (Path("agents") / "researcher.py").exists()


def test_add_agent_duplicate(tmp_path):
    os.chdir(tmp_path)
    generate_project("my-project", "langgraph", "openai", "pip")
    os.chdir(tmp_path / "my-project")
    add_agent("researcher", "langgraph")
    result = add_agent("researcher", "langgraph")
    assert result is False