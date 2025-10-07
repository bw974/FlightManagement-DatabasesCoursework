import re
from cli import print_table
from database import DBOperations
from utils import validate_datetime


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
            status = input("Enter status (On Time, Delayed or Cancelled): ").strip().title()
            if status in ["On Time", "Delayed", "Cancelled"]:
                break
            print("Invalid status format, usage: On Time, Delayed or Cancelled\n")

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

        self.db.insert("Flights", (None, flight_num, dep_time, arr_time, status, origin_id, destination_id, None, None))
        print("New flight added successfully, assign pilot and airplane under respective menus")


    # View flights by specific criteria such as departure date, status, destination etc.
    def view_flights_by_criteria(self) -> None:
        criteria_map = {
            "flight number": "FlightNumber",
            "departure date": "DATE(Flights.DepartureTime)",
            "arrival date": "DATE(Flights.ArrivalTime)",
            "status": "Flights.Status",
            "origin airport code": "Origin.AirportCode",
            "destination airport code": "Destination.AirportCode",
            "pilot name": "PilotName",
            "airplane": "Registration"
        }

        for key in criteria_map.keys():
            print(f"- {key.title()}")

        while True:
            choice = input("\nEnter search criteria (e.g. Departure Date): ").strip().lower()
            if choice in criteria_map:
                break
            print("Invalid criteria option, try again, usage: Departure Date\n")

        while True:
            value = input(f"Enter value for {choice.title()} (case-sensitive): ").strip()
            criteria = {criteria_map[choice]: value}
            flights = self.db.select_flights_with_joins(criteria)
            if flights:
                break
            print(f"\nNo flights found for {choice.title()} {value}, try again\n")

        columns = ["Flight Number", "Departure Time", "Arrival Time", "Status", "Origin", "Destination", "Pilot", "Airplane"]
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
        while True:
            flight_num = input("Enter flight number of flight to update: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                flight = self.db.select_by_criteria("Flights", {"FlightNumber": flight_num})
                if flight:
                    break
                print(f"Flight {flight_num} not found")
            else:
                print("Invalid flight number format, usage: AA000")

        flight_id = flight[0]
        print("Leave field blank to keep current value.")

        while True:
            flight_num = input(f"New flight number ({flight[1]}): ").strip().upper() or flight[1]
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                break
            print("Invalid flight number format")

        while True:
            dep_time = input(f"New departure time ({flight[2]}): ").strip() or flight[2]
            if validate_datetime(dep_time):
                break
            print("Invalid datetime format, try again")

        while True:
            arr_time = input(f"New arrival time ({flight[3]}): ").strip() or flight[3]
            if validate_datetime(arr_time):
                break
            print("Invalid datetime format, try again")
        
        while True:
            status = input(f"New status (On Time, Delayed or Cancelled) ({flight[4]}): ").strip().title() or flight[4]
            if status in ["On Time", "Delayed", "Cancelled"]:
                break
            print("Invalid status format, choose either: On Time, Delayed or Cancelled")

        self.db.update(
            "Flights",
            {"FlightNumber": flight_num, "DepartureTime": dep_time, "ArrivalTime": arr_time, "Status": status},
            "FlightID",
            flight_id,
        )
        print(f"Flight {flight_num} updated successfully")


    # Delete an existing flight record from the database confirming with the user before deletion
    def delete_flight(self) -> None:
        while True:
            flight_num = input("Enter flight number of flight to delete: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                flight = self.db.select_by_criteria("Flights", {"FlightNumber": flight_num})
                if flight:
                    break
                print(f"Flight {flight_num} not found")
            else:
                print("Invalid flight number format, usage: AA000")

        confirm = input(f"Are you sure you want to delete flight {flight_num}? (y/n): ").lower()
        if confirm == "y":
            self.db.delete("Flights", "FlightID", flight[0])
            print(f"Flight {flight_num} deleted successfully")
        else:
            print("Delete cancelled.")
