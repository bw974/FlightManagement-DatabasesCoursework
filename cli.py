from rich.console import Console
from rich.table import Table
from rich.panel import Panel


# Print the options menu in cyan colour format from Rich library
def print_options(options: list[str]) -> None:
    console = Console()
    table = Table(show_header=False, box=None)
    table.add_column("Option", style="cyan")
    for option in options:
        table.add_row(option)
    console.print(table)


# Print the BathAirways banner including the logo and title of Flight management system
def print_banner(logo: str, title: str, subtitle: str) -> None:
    console = Console()
    console.print()
    console.print(Panel.fit(
        renderable=f"[bold blue]{logo}[/bold blue]",
        title=title,
        subtitle=subtitle,
    ))
    console.print()


# Print a table's data in a nice format with cyan colour for text and bold white headings
def print_table(data: list[tuple], columns: list[str], title: str) -> None:
    console = Console()
    if not data:
        console.print(f"[bold red]No {title} found[/bold red]")
        return

    table = Table(title=title, show_lines=True)

    # Skip first column of table which is the ID primary key but not relevant to user
    for col in columns[1:]:
        table.add_column(col, style="cyan", no_wrap=True)
    # For any null values such as dep/arr time for cancelled flight or pilot/airplane yet to be assigned, mark cell with a dash (-)
    for row in data:
        table.add_row(*(str(item) if item not in [None, " "] else "-" for item in row[1:]))
    console.print()
    console.print(table)
