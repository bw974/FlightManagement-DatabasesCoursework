import re
from cli import print_table
from database import DBOperations
from utils import get_flight, validate_datetime


class Flight:
    # Initialise DBOperations and use the class functions to interact with the database
    def __init__(self):
        self.db = DBOperations()


    # Add a new flight to the database checking for valid user input
    def add_new_flight(self) -> None:
        while True:
            flight_num = input("Enter flight number (e.g. BA123): ").strip().upper()
            if not bool(re.fullmatch(r"BA\d{3}", flight_num)):
                print("Invalid flight number format, usage: BAXXX\n")
                continue
            elif self.db.select_by_criteria("Flights", {"FlightNumber": flight_num}):
                print(f"Flight {flight_num} already exists\n")
                continue
            break

        while True:
            dep_time = input("Enter departure time (YYYY-MM-DD HH:MM): ").strip()
            if validate_datetime(dep_time):
                break
            print("Invalid datetime format, usage: YYYY-MM-DD HH:MM\n")

        while True:
            arr_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ").strip()
            if not validate_datetime(arr_time):
                print("Invalid datetime format, usage: YYYY-MM-DD HH:MM\n")
                continue
            if arr_time <= dep_time:
                print("Arrival time must be later than departure time\n")
                continue
            break

        while True:
            origin_airport_code = input("Enter origin airport code (e.g. LHR): ").strip().upper()
            origin_airport = self.db.select_by_criteria("Airports", {"AirportCode": origin_airport_code})
            if origin_airport:
                origin_id = origin_airport[0][0]
                break
            print("Airport not found, enter a valid airport code\n")

        while True:
            destination_airport_code = input("Enter destination airport code (e.g. LAX): ").strip().upper()
            destination_airport = self.db.select_by_criteria("Airports", {"AirportCode": destination_airport_code})
            if destination_airport_code == origin_airport_code:
                print("Destination airport cannot be the same as origin airport\n")
                continue
            if not destination_airport:
                print("Airport not found, enter a valid airport code\n")
                continue
            destination_id = destination_airport[0][0]
            break
        # Add new flight record where status is On Time by default and the pilot/airplane are assigned by another airline employee later
        self.db.insert("Flights", (None, flight_num, dep_time, arr_time, "On Time", origin_id, destination_id, None, None))
        print("New flight added successfully, assign pilot and airplane under respective menus")


    # View flights by specific criteria such as departure date, status, destination etc.
    def view_flights_by_criteria(self) -> None:
        print("\nSearch Criteria:")
        criteria_map = {
            "departure date": "DATE(DepartureTime)",
            "arrival date": "DATE(ArrivalTime)",
            "status": "Status",
            "origin": "Origin",
            "destination": "Destination"
        }

        for key in criteria_map.keys():
            print(f"- {key.title()}")

        while True:
            choice = input("\nEnter search criteria (e.g. Departure Date): ").strip().lower()
            if choice in criteria_map:
                break
            print("Invalid criteria option, try again, usage: Departure Date, Arrival Date, Status, Origin, Destination\n")

        while True:
            if choice in ["departure date", "arrival date"]:
                value = input(f"Enter value for {choice.title()} (YYYY-MM-DD): ").strip()
            if choice == "status":
                value = input(f"Enter value for {choice.title()} (On Time, Delayed or Cancelled): ").strip().title()
            if choice in ["origin", "destination"]:
                value = input(f"Enter value for {choice.title()} (e.g. LHR): ").strip().upper()

            criteria = {criteria_map[choice]: value}
            flights = self.db.select_flights_with_joins(criteria)
            if flights:
                break
            print(f"\nNo flights found for {choice.title()} {value}, try again\n")

        columns = ["FlightID", "Flight Number", "Departure Time", "Arrival Time", "Status", "Origin", "Destination", "Pilot", "Airplane"]
        print_table(flights, columns, title=f"Flights for {choice.title()} {value}")


    # View all flights stored in the database including origin and destination airports, assigned pilot and airplane
    def view_all_flights(self) -> None:
        flights = self.db.select_flights_with_joins()
        if not flights:
            print("No flights listed in database")
            return
        columns = ["FlightID", "Flight Number", "Departure Time", "Arrival Time", "Status", "Origin", "Destination", "Pilot", "Airplane"]
        print_table(flights, columns, title="Information on all flights")


    # Update an existing flight schedule such as changing departure time or status
    def update_flight(self) -> None:
        try:
            flight = get_flight(self)
            flight_num = flight[1]
            flight_status = flight[4]
            if flight_status == "Cancelled":
                print(f"Flight {flight_num} is cancelled and cannot be updated\n")
                return
        except Exception as e:
            print(f"Error finding flight: {e}\n")
            return

        flight_id = flight[0]
        print("Enter nothing to keep current value:")

        while True:
            status = input(f"Enter new status (On Time, Delayed or Cancelled - current: {flight[4]}): ").strip().title() or flight[4]
            if status in ["On Time", "Delayed", "Cancelled"]:
                break
            print("Invalid status format, choose either: On Time, Delayed or Cancelled")

        # If the user has cancelled the flight, the flight times are removed and pilot/airplane unassigned/ freed up for other flights
        # Assumption: once a flight is cancelled it can no longer be reinstated
        if status == "Cancelled":
            new_dep_time = None
            new_arr_time = None
            pilot = None
            airplane = None
            self.db.update(
                "Flights",
                {"DepartureTime": new_dep_time, "ArrivalTime": new_arr_time, "Status": status, "PilotID": pilot, "AirplaneID": airplane},
                "FlightID",
                flight_id,
            )
            print(f"Flight {flight_num} cancelled successfully")
            return

        while True:
            new_dep_time = input(f"Enter new departure time (current: {flight[2]}): ").strip() or flight[2]
            if validate_datetime(new_dep_time):
                break
            print("Invalid datetime format, usage: YYYY-MM-DD HH:MM\n")

        while True:
            new_arr_time = input(f"Enter new arrival time (current: {flight[3]}): ").strip() or flight[3]
            if not validate_datetime(new_arr_time):
                print("Invalid datetime format, usage: YYYY-MM-DD HH:MM\n")
                continue
            if new_arr_time <= new_dep_time:
                print("Arrival time must be later than departure time\n")
                continue
            break            

        self.db.update(
            "Flights",
            {"DepartureTime": new_dep_time, "ArrivalTime": new_arr_time, "Status": status},
            "FlightID",
            flight_id,
        )
        print(f"Flight {flight_num} updated successfully")


    # Delete an existing flight record from the database confirming with the user before deletion
    def delete_flight(self) -> None:
        try:
            flight = get_flight(self)
        except Exception as e:
            print(f"Error finding flight: {e}\n")
            return

        confirm = input(f"Enter 'y' to confirm deletion of flight {flight[1]} (anything else will cancel): ").lower()
        if confirm == "y":
            try:
                self.db.delete("Flights", "FlightID", flight[0])
                print(f"Flight {flight[1]} successfully deleted")
            except Exception as e:
                print(f"Failed to delete flight: {e}\n")
                return
        else:
            print("Cancelled, flight not deleted")
