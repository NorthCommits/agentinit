import click
import questionary
import requests
import urllib3
from rich.console import Console
from rich.table import Table
from agentinit.generator import generate_project, add_agent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

SUPPORTED_FRAMEWORKS = ["langgraph", "crewai", "autogen", "google_adk", "openai_agents", "smolagents"]
SUPPORTED_LLMS = ["openai", "anthropic", "groq", "azure", "bedrock", "gemini"]
PACKAGE_MANAGERS = ["pip", "uv"]
API_URL = "https://agentinit-api.onrender.com/analyze"


def get_smart_structure(description: str, framework: str, llm: str) -> dict | None:
    try:
        console.print("  [dim]Waking up the API, this may take up to 60 seconds on first run...[/dim]")
        response = requests.post(
            API_URL,
            json={"description": description, "framework": framework, "llm": llm},
            timeout=90,
            verify=False,
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


@click.group()
def app():
    """agentinit - scaffold LLM agent projects in seconds"""
    pass


@app.command("create")
@click.argument("project_name")
def create(project_name):
    """Scaffold a new LLM agent project interactively."""

    console.print(f"\n[bold green]Creating project:[/bold green] [cyan]{project_name}[/cyan]\n")

    framework = questionary.select(
        "Select a framework:",
        choices=SUPPORTED_FRAMEWORKS,
    ).ask()

    if not framework:
        raise click.Abort()

    llm = questionary.select(
        "Select an LLM provider:",
        choices=SUPPORTED_LLMS,
    ).ask()

    if not llm:
        raise click.Abort()

    package_manager = questionary.select(
        "Select a package manager:",
        choices=PACKAGE_MANAGERS,
    ).ask()

    if not package_manager:
        raise click.Abort()

    description = questionary.text(
        "Describe your project in one line (press Enter to skip):",
    ).ask()

    smart_structure = None
    if description and description.strip():
        console.print("\n  [dim]Analyzing project description...[/dim]")
        smart_structure = get_smart_structure(description.strip(), framework, llm)
        if smart_structure:
            console.print("  [green]Smart structure generated![/green]")
        else:
            console.print("  [yellow]Could not reach API, using default structure.[/yellow]")

    console.print(f"\n  Framework       : [cyan]{framework}[/cyan]")
    console.print(f"  LLM Provider    : [cyan]{llm}[/cyan]")
    console.print(f"  Package Manager : [cyan]{package_manager}[/cyan]\n")

    success = generate_project(project_name, framework, llm, package_manager, smart_structure)

    if not success:
        raise click.Abort()

    console.print(f"\n[bold green]Done![/bold green] Your project is ready at [cyan]./{project_name}[/cyan]")
    console.print("\nNext steps:")
    console.print(f"  [yellow]cd {project_name}[/yellow]")
    console.print("  [yellow]cp .env.example .env[/yellow]")

    if package_manager == "uv":
        console.print("  [yellow]uv sync[/yellow]")
        console.print("  [yellow]uv run python main.py[/yellow]\n")
    else:
        console.print("  [yellow]pip install -r requirements.txt[/yellow]")
        console.print("  [yellow]python main.py[/yellow]\n")


@app.command("add-agent")
@click.argument("agent_name")
@click.option("--framework", "-f", required=True, help="Framework of the existing project")
def add_agent_cmd(agent_name, framework):
    """Add a new agent to an existing scaffolded project."""
    if framework not in SUPPORTED_FRAMEWORKS:
        console.print(f"[red]Framework '{framework}' is not supported.[/red]")
        console.print(f"Supported: {', '.join(SUPPORTED_FRAMEWORKS)}")
        raise click.Abort()

    console.print(f"\n[bold green]Adding agent:[/bold green] {agent_name}")
    console.print(f"  Framework : [cyan]{framework}[/cyan]\n")

    success = add_agent(agent_name, framework)

    if not success:
        raise click.Abort()

    console.print(f"\n[bold green]Done![/bold green] Agent [cyan]agents/{agent_name}.py[/cyan] created.\n")


@app.command("list-frameworks")
def list_frameworks():
    """List all supported frameworks and LLM providers."""
    table = Table(title="Supported Frameworks & LLM Providers")
    table.add_column("Frameworks", style="cyan")
    table.add_column("LLM Providers", style="green")

    rows = list(zip(SUPPORTED_FRAMEWORKS, SUPPORTED_LLMS))
    for fw, llm in rows:
        table.add_row(fw, llm)

    console.print(table)