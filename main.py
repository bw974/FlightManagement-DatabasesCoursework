from database import setup_database
import airplane, airport, cli, config, flight, pilot, summary


# Used to recursively ask user to choose an option from the submenu or go back to main menu
def choose_option(operations: dict, options_list: list[str]):
    print("\nWhat do you want to do?\n")
    cli.print_options(options_list)
    while True:
        try:
            choice = int(input(f"\nEnter your choice (0 to {len(operations)}): "))
            if choice == 0:
                return
            chosen_option = operations.get(choice)
            if not chosen_option:
                print(f"Invalid option, choose a number between 0 and {len(operations)}")
                continue
            chosen_option()
        except ValueError:
            print(f"Enter a valid number between 0 and {len(operations)}")


# Main program
def main():
    # Initialise each table's query objects and functions
    airplane_options = airplane.Airplane()
    airport_options = airport.Airport()
    flight_options = flight.Flight()
    pilot_options = pilot.Pilot()
    summary_options = summary.Summary()

    # Print the BathAirways banner and title
    cli.print_banner(config.logo, config.title, config.subtitle)

    # Define main menu and it's function calls to sub-menu options, database reset or exit
    main_menu = {
        1: lambda: choose_option(flight_menu, config.flight_menu_options),
        2: lambda: choose_option(pilot_menu, config.pilot_menu_options),
        3: lambda: choose_option(airport_menu, config.airport_menu_options),
        4: lambda: choose_option(airplane_menu, config.airplane_menu_options),
        5: lambda: choose_option(summary_menu, config.summary_menu_options),
        6: setup_database,
        0: exit
    }
    # Define flight menu options and function calls
    flight_menu = {
        1: flight_options.add_new_flight,
        2: flight_options.view_flights_by_criteria,
        3: flight_options.view_all_flights,
        4: flight_options.update_flight,
        5: flight_options.delete_flight,
    }
    # Define pilot menu options and function calls
    pilot_menu = {
        1: pilot_options.add_new_pilot,
        2: pilot_options.view_pilot_schedule,
        3: pilot_options.view_all_pilots,
        4: pilot_options.update_pilot,
        5: pilot_options.assign_pilot,
        6: pilot_options.delete_pilot
    }
    # Define airport menu options and function calls
    airport_menu = {
        1: airport_options.add_new_airport,
        2: airport_options.view_all_airports,
        3: airport_options.update_airport,
        4: airport_options.delete_airport
    }
    # Define airplane menu options and function calls
    airplane_menu = {
        1: airplane_options.add_new_airplane,
        2: airplane_options.view_all_airplanes,
        3: airplane_options.update_airplane,
        4: airplane_options.assign_airplane,
        5: airplane_options.delete_airplane
    }
    # Define summary menu options and function calls
    summary_menu = {
        1: summary_options.num_flights_per_origin,
        2: summary_options.num_flights_per_destination,
        3: summary_options.num_flights_per_pilot,
        4: summary_options.num_flights_per_airplane
    }

    # Present main menu ask user to select option for sub-menus
    while True:
        print("Welcome to BathAirways! Please select a menu option:\n")
        cli.print_options(config.main_menu_options)
        try:
            choice = int(input(f"\nEnter your choice (0 to {len(config.main_menu_options) - 1}): "))
            chosen_option = main_menu.get(choice)
            if not chosen_option:
                print(f"Invalid option, choose a number between 0 and {len(config.main_menu_options) - 1}")
            # Execute the chosen option
            chosen_option()
        except ValueError:
            print(f"Enter a valid number between 0 and {len(config.main_menu_options) - 1}")


# Entry point for main function
if __name__ == "__main__":
   main()
