import click
from cli.commands.install import install
from cli.commands.start import start
from cli.commands.list import list_plugins
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """LLMObs CLI - Manage your LLM observability platform."""
    pass


# Register commands
cli.add_command(install)
cli.add_command(start)
cli.add_command(list_plugins, name="list")


@cli.command()
def stop():
    """Stop all LLMObs services."""
    from cli.utils.docker_manager import DockerManager
    
    console.print("[yellow]Stopping LLMObs services...[/yellow]")
    dm = DockerManager()
    if dm.stop_services():
        console.print("[green]✓[/green] Services stopped successfully")
    else:
        console.print("[red]✗[/red] Failed to stop services", err=True)


@cli.command()
def status():
    """Check the status of LLMObs services."""
    from cli.utils.docker_manager import DockerManager
    
    dm = DockerManager()
    status = dm.get_status()
    
    console.print("\n[bold]LLMObs Service Status:[/bold]\n")
    for service, running in status.items():
        icon = "✓" if running else "✗"
        color = "green" if running else "red"
        console.print(f"[{color}]{icon}[/{color}] {service}: {'Running' if running else 'Stopped'}")


if __name__ == "__main__":
    cli()
