import click
from rich.console import Console
from rich.table import Table
from agentinit.generator import generate_project, add_agent

console = Console()

SUPPORTED_FRAMEWORKS = ["langgraph", "crewai", "autogen", "google_adk", "openai_agents", "smolagents"]
SUPPORTED_LLMS = ["openai", "anthropic", "groq", "azure", "bedrock", "gemini"]


@click.group()
def app():
    """agentinit - scaffold LLM agent projects in seconds"""
    pass


@app.command("init")
@click.argument("project_name")
@click.option("--framework", "-f", required=True, help="Agent framework to use")
@click.option("--llm", "-l", required=True, help="LLM provider to use")
def init(project_name, framework, llm):
    """Scaffold a new LLM agent project."""
    if framework not in SUPPORTED_FRAMEWORKS:
        console.print(f"[red]Framework '{framework}' is not supported.[/red]")
        console.print(f"Supported: {', '.join(SUPPORTED_FRAMEWORKS)}")
        raise click.Abort()

    if llm not in SUPPORTED_LLMS:
        console.print(f"[red]LLM provider '{llm}' is not supported.[/red]")
        console.print(f"Supported: {', '.join(SUPPORTED_LLMS)}")
        raise click.Abort()

    console.print(f"\n[bold green]Scaffolding project:[/bold green] {project_name}")
    console.print(f"  Framework : [cyan]{framework}[/cyan]")
    console.print(f"  LLM       : [cyan]{llm}[/cyan]\n")

    success = generate_project(project_name, framework, llm)

    if not success:
        raise click.Abort()

    console.print(f"\n[bold green]Done![/bold green] Your project is ready at [cyan]./{project_name}[/cyan]")
    console.print("\nNext steps:")
    console.print(f"  [yellow]cd {project_name}[/yellow]")
    console.print("  [yellow]cp .env.example .env[/yellow]")
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