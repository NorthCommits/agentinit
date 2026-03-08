from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()

TEMPLATES_DIR = Path(__file__).parent / "templates"

LLM_CONFIG = {
    "openai":    {"api_key_env": "OPENAI_API_KEY",       "model": "gpt-4o"},
    "anthropic": {"api_key_env": "ANTHROPIC_API_KEY",    "model": "claude-sonnet-4-20250514"},
    "groq":      {"api_key_env": "GROQ_API_KEY",         "model": "llama3-70b-8192"},
    "azure":     {"api_key_env": "AZURE_OPENAI_API_KEY", "model": "gpt-4o"},
    "bedrock":   {"api_key_env": "AWS_ACCESS_KEY_ID",    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"},
    "gemini":    {"api_key_env": "GOOGLE_API_KEY",       "model": "gemini-2.0-flash"},
}

FRAMEWORK_FILES = [
    ("main.py.j2",              "main.py"),
    ("requirements.txt.j2",     "requirements.txt"),
    ("agents/base_agent.py.j2", "agents/base_agent.py"),
    ("tools/sample_tool.py.j2", "tools/sample_tool.py"),
]

COMMON_FILES = [
    ("config.yaml.j2", "config/config.yaml"),
    ("README.md.j2",   "README.md"),
    ("Dockerfile.j2",  "Dockerfile"),
]


def write_file(output_path: Path, content: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    console.print(f"  [green]created[/green] {output_path}")


def generate_project(project_name: str, framework: str, llm: str) -> bool:
    project_path = Path(project_name)

    if project_path.exists():
        console.print(f"[red]Directory '{project_name}' already exists. Aborting.[/red]")
        return False

    context = {
        "project_name": project_name,
        "framework": framework,
        "llm_provider": llm,
        **LLM_CONFIG[llm],
    }

    fw_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR / framework)))
    for template_file, output_file in FRAMEWORK_FILES:
        template = fw_env.get_template(template_file)
        write_file(project_path / output_file, template.render(**context))

    common_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR / "common")))
    for template_file, output_file in COMMON_FILES:
        template = common_env.get_template(template_file)
        write_file(project_path / output_file, template.render(**context))

    env_content = build_env_file(llm)
    write_file(project_path / ".env.example", env_content)
    return True


def build_env_file(llm: str) -> str:
    lines = []
    if llm == "azure":
        lines.append("AZURE_OPENAI_API_KEY=your_api_key_here")
        lines.append("AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
    elif llm == "bedrock":
        lines.append("AWS_ACCESS_KEY_ID=your_access_key_here")
        lines.append("AWS_SECRET_ACCESS_KEY=your_secret_key_here")
        lines.append("AWS_REGION=us-east-1")
    else:
        lines.append(f"{LLM_CONFIG[llm]['api_key_env']}=your_api_key_here")
    return "\n".join(lines) + "\n"


def add_agent(agent_name: str, framework: str) -> bool:
    agents_path = Path("agents")

    if not agents_path.exists():
        console.print("[red]No 'agents/' folder found. Are you inside a scaffolded project?[/red]")
        return False

    output_path = agents_path / f"{agent_name}.py"

    if output_path.exists():
        console.print(f"[red]Agent '{agent_name}.py' already exists. Aborting.[/red]")
        return False

    template_path = TEMPLATES_DIR / framework / "agents" / "base_agent.py.j2"
    if not template_path.exists():
        console.print(f"[red]No template found for framework '{framework}'.[/red]")
        return False

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR / framework / "agents")))
    template = env.get_template("base_agent.py.j2")
    content = template.render(project_name=agent_name, framework=framework, llm_provider="openai", **LLM_CONFIG["openai"])
    write_file(output_path, content)
    return True