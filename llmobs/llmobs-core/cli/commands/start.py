import click
from rich.console import Console
from rich.progress import Progress
from cli.utils.docker_manager import DockerManager
import time

console = Console()


@click.command()
@click.option("--detach", "-d", is_flag=True, help="Run services in detached mode")
def start(detach: bool):
    """Start the LLMObs platform and all services."""
    console.print("[cyan]Starting LLMObs platform...[/cyan]\n")
    
    dm = DockerManager()
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Starting services...", total=100)
        
        # Start core services
        progress.update(task, description="[cyan]Starting database...")
        if not dm.start_service("postgres"):
            console.print("[red]✗[/red] Failed to start database", err=True)
            return
        progress.update(task, advance=20)
        
        # Wait for database to be ready
        time.sleep(2)
        
        progress.update(task, description="[cyan]Starting Redis...")
        if not dm.start_service("redis"):
            console.print("[red]✗[/red] Failed to start Redis", err=True)
            return
        progress.update(task, advance=20)
        
        progress.update(task, description="[cyan]Starting backend...")
        if not dm.start_service("backend"):
            console.print("[red]✗[/red] Failed to start backend", err=True)
            return
        progress.update(task, advance=30)
        
        progress.update(task, description="[cyan]Starting frontend...")
        if not dm.start_service("frontend"):
            console.print("[red]✗[/red] Failed to start frontend", err=True)
            return
        progress.update(task, advance=30)
    
    console.print("\n[green]✓[/green] LLMObs platform started successfully!\n")
    console.print("[bold]Access the platform at:[/bold]")
    console.print("  • Frontend: http://localhost:3000")
    console.print("  • Backend API: http://localhost:8000")
    console.print("  • API Docs: http://localhost:8000/docs\n")
    
    if not detach:
        console.print("[yellow]Press Ctrl+C to stop the services[/yellow]")
        try:
            dm.follow_logs()
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping services...[/yellow]")
            dm.stop_services()
