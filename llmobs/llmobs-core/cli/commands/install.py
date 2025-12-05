import click
from rich.console import Console
from rich.progress import Progress
from cli.utils.docker_manager import DockerManager
from cli.utils.network import check_plugin_availability

console = Console()


@click.command()
@click.argument("plugin_name")
@click.option("--url", help="Plugin repository URL")
@click.option("--version", default="latest", help="Plugin version to install")
def install(plugin_name: str, url: str, version: str):
    """Install a new plugin to the LLMObs platform."""
    console.print(f"[cyan]Installing plugin:[/cyan] {plugin_name} ({version})")
    
    dm = DockerManager()
    
    # Check if plugin is already installed
    if dm.is_plugin_installed(plugin_name):
        console.print(f"[yellow]Warning:[/yellow] Plugin '{plugin_name}' is already installed")
        if not click.confirm("Do you want to reinstall it?"):
            return
    
    with Progress() as progress:
        task = progress.add_task(f"[cyan]Installing {plugin_name}...", total=100)
        
        # Pull plugin image
        progress.update(task, advance=30)
        if url:
            image = url
        else:
            image = f"llmobs/{plugin_name}:{version}"
        
        if not dm.pull_image(image):
            console.print(f"[red]✗[/red] Failed to pull plugin image", err=True)
            return
        
        progress.update(task, advance=30)
        
        # Register plugin
        if dm.register_plugin(plugin_name, image):
            progress.update(task, advance=40)
            console.print(f"[green]✓[/green] Plugin '{plugin_name}' installed successfully")
        else:
            console.print(f"[red]✗[/red] Failed to register plugin", err=True)
