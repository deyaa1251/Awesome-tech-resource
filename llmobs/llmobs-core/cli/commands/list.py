import click
from rich.console import Console
from rich.table import Table
from cli.utils.docker_manager import DockerManager

console = Console()


@click.command()
@click.option("--all", "-a", is_flag=True, help="Show all plugins including inactive")
def list_plugins(all: bool):
    """List all installed plugins."""
    dm = DockerManager()
    plugins = dm.list_plugins(include_inactive=all)
    
    if not plugins:
        console.print("[yellow]No plugins installed[/yellow]")
        return
    
    table = Table(title="Installed Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version")
    table.add_column("Image")
    
    for plugin in plugins:
        status = "Active" if plugin.get("active") else "Inactive"
        status_color = "green" if plugin.get("active") else "yellow"
        
        table.add_row(
            plugin["name"],
            f"[{status_color}]{status}[/{status_color}]",
            plugin.get("version", "latest"),
            plugin.get("image", "N/A"),
        )
    
    console.print(table)
