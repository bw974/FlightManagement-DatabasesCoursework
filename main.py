from cli import show_menu
from database import setup_database
from flights import FlightQueries
from airports import AirportQueries
from pilots import PilotQueries
from airplanes import AirplaneQueries


def main():  

    flights = FlightQueries()
    airports = AirportQueries()
    pilots = PilotQueries()
    airplanes = AirplaneQueries()

    options = {
        1: flights.add_new_flight,
        2: flights.view_by_criteria,
        3: flights.view_flight_info,
        4: flights.update_flight,
        5: flights.assign_pilot,
        6: flights.delete_flight,
        7: flights.view_pilot_schedule,
        8: pilots.view_pilot_info,
        9: pilots.add_new_pilot,
        10: pilots.update_pilot,
        11: pilots.delete_pilot,
        12: airports.view_airport_info,
        13: airports.add_new_airport,
        14: airports.update_airport,
        15: airports.delete_airport,
        16: flights.num_flights_per_airport,
        17: flights.num_flights_per_pilot,
        18: setup_database,
        19: exit
    }

    # Show the UI menu
    show_menu()
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            chosen_option = options.get(choice)
            if not chosen_option:
                print("Invalid option, please select between 1 and 20")
            # Execute the chosen option
            chosen_option()
        except ValueError:
            print("Enter a valid integer, please try again")


if __name__ == "__main__":
   main()
