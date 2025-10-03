from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def show_menu():
    console = Console()
    logo = r"""[bold blue]
     ____        _   _        _    _                              
    | __ )  __ _| |_| |__    / \  (_)_ ____      ____ _ _   _ ___ 
    |  _ \ / _` | __| '_ \  / _ \ | | '__\ \ /\ / / _` | | | / __|
    | |_) | (_| | |_| | | |/ ___ \| | |   \ V  V / (_| | |_| \__ \
    |____/ \__,_|\__|_| |_/_/   \_\_|_|    \_/\_/ \__,_|\__, |___/
                                                        |___/      
    [/bold blue]"""

    console.print()
    console.print(Panel.fit(
        logo,
        title="[bold italic cyan]University of Bath: Databases and Cloud[/bold italic cyan]",
        subtitle="[bold yellow]Flight Management System[/bold yellow]",
    ))
    console.print()

    options = [
        "1. Add a New Flight",
        "2. View Flights by Criteria",
        "3. View Flight Information",
        "4. Update Flight Information",
        "5. Assign Pilot to Flight",
        "6. Delete a Flight",
        "7. View Pilot Schedule",
        "8. View Pilot Information",
        "9. Add a New Pilot",
        "10. Update Pilot Information",
        "11. Delete a Pilot",
        "12. View Destination Information",
        "13. Add a New Destination",
        "14. Update Destination Information",
        "15. Delete a Destination",
        "16. View Number of Flights for a Destination",
        "17. View Number of Flights assigned to a Pilot",
        "18. Reset Database with Sample Data",
        "19. Exit"
    ]

    half_options_count = round(len(options) / 2)
    left_menu_options = options[:half_options_count]
    right_menu_options = options[half_options_count:]

    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column("Left", style="cyan", no_wrap=True)
    table.add_column("Right", style="cyan", no_wrap=True)

    for i in range(half_options_count):
        left_row = left_menu_options[i] if i < len(left_menu_options) else ""
        right_row = right_menu_options[i] if i < len(right_menu_options) else ""
        table.add_row(left_row, right_row)

    console.print(table)


def print_table(data: list[tuple], columns: list[str], title: str):
    console = Console()
    if not data:
        console.print(f"[bold red]No {title} data found[/bold red]")
        return

    table = Table(title=title, show_lines=True)

    # Skip first column of table which is the table ID not relevant to user
    for col in columns[1:]:
        table.add_column(col, style="cyan", no_wrap=True)

    # Add rows
    for row in data:
        table.add_row(*(str(item) if item is not None else "N/A" for item in row[1:]))

    console.print(table)
