import re
from cli import print_table
from database import DBOperations
from utils import validate_int, validate_datetime


class FlightQueries:
    def __init__(self):
        self.db = DBOperations()

    
    def view_flight_info(self):
        flights = self.db.select_all("Flights")
        if not flights:
            print("No flights listed in database")
            return
        columns = ["FlightID", "Flight Number", "Departure Time", "Arrival Time", "Status"]
        print_table(flights, columns, title="Flight Info")


    def add_new_flight(self):
        while True:
            flight_num = input("Enter flight number: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                break
            print("Invalid flight number format")

        while True:
            dep_time = input("Enter departure time (YYYY-MM-DD HH:MM): ").strip()
            if validate_datetime(dep_time):
                break
            print("Invalid datetime format, try again")

        while True:
            arr_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ").strip()
            if validate_datetime(arr_time):
                break
            print("Invalid datetime format, try again")

        while True:
            status = input("Enter status (On Time, Delayed or Cancelled): ").strip().title()
            if status in ["On Time", "Delayed", "Cancelled"]:
                break
            print("Invalid status format, choose either: On Time, Delayed or Cancelled")

        while True:
            airport_code = input("Enter destination airport code: ").strip().upper()
            airport = self.db.select("Airports", "AirportCode", airport_code)
            if airport:
                airport_id = airport[0]
                break
            print("Airport not found, please enter a valid airport code")

        pilot_id = input("Enter pilot ID (or leave blank): ").strip()
        pilot_id = int(pilot_id) if validate_int(pilot_id) else None

        self.db.insert("Flights", (None, flight_num, dep_time, arr_time, status, airport_id, pilot_id))
        print("New flight added successfully")


    def update_flight(self):
        while True:
            flight_num = input("Enter flight number of flight to update: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                flight = self.db.select("Flights", "FlightNumber", flight_num)
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


    def delete_flight(self):
        while True:
            flight_num = input("Enter flight number of flight to delete: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{2}\d{3}", flight_num)):
                flight = self.db.select("Flights", "FlightNumber", flight_num)
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

# TODO - write more complex functions

    def view_by_criteria(self):
        return


    def update_schedule(self):
        return


    def assign_pilot(self):
        return


    def view_pilot_schedule(self):
        return


    def num_flights_per_airport(self):
        return


    def num_flights_per_pilot(self):
        return
