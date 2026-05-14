from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def show_header(domain, mode):
    title = Text("HEXSCAN", style="bold cyan")

    subtitle = Text(
        f"AI-Powered Recon Framework\nTarget: {domain}\nMode: {mode}",
        style="white"
    )

    panel = Panel.fit(
        subtitle,
        title=title,
        border_style="cyan"
    )

    console.print(panel)


def section(title):
    console.print(f"\n[bold cyan]━━━━━━━━ {title} ━━━━━━━━[/bold cyan]\n")


def task(name, status):
    icon = {
        "running": "[yellow]⏳[/yellow]",
        "done": "[green]✔[/green]",
        "failed": "[red]✘[/red]"
    }.get(status, "[white]-[/white]")

    console.print(f"{icon} {name}")