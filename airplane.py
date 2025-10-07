import re
from cli import print_table
from database import DBOperations
from datetime import datetime
from utils import get_flight, get_airplane


class Airplane:
    # Initialise DBOperations and use the class functions to interact with the database
    def __init__(self):
        self.db = DBOperations()


    # View all airplanes stored in the database
    def view_all_airplanes(self) -> None:
        airplanes = self.db.select_all("Airplanes")
        if not airplanes:
            print("No airplanes listed in the database")
            return
        columns = ["AirplaneID", "Registration", "Manufacturer", "Model"]
        print_table(airplanes, columns, title="Information on all airplanes")


    # Add a new airplane to the database checking for valid user input
    def add_new_airplane(self) -> None:
        while True:
            registration = input("Enter airplane registration number (e.g., G-ABCD): ").strip().upper()
            if not bool(re.fullmatch(r"^G-[A-Z]{4}$", registration)):
                print("Invalid registration format, usage: G-XXXX\n")
                continue
            elif self.db.select_by_criteria("Airplanes", {"Registration": registration}):
                print(f"Airplane {registration} already exists\n")
                continue
            break

        while True:
            manufacturer = input("Enter manufacturer: ").strip().title()
            if manufacturer:
                break
            print("Manufacturer cannot be empty\n")

        while True:
            model = input("Enter model: ").strip().title()
            if model:
                break
            print("Model cannot be empty\n")
        # Insert new airplane record
        try:
            self.db.insert("Airplanes", (None, registration, manufacturer, model))
            print(f"Airplane {registration} added successfully")
        except Exception as e:
            print(f"Failed to add airplane: {e}\n")
            return


    # Update an existing airplane's details
    def update_airplane(self) -> None:
        try:
            airplane = get_airplane(self)
        except Exception as e:
            print(f"Error finding airplane: {e}\n")
            return

        airplane_id = airplane[0]
        print("Enter nothing to keep current value:")

        while True:
            new_manufacturer = input(f"Enter new manufacturer (current: {airplane[2]}): ").strip().title() or airplane[2]
            if new_manufacturer:
                break
            print("Manufacturer cannot be empty\n")

        while True:
            new_model = input(f"Enter new model (current: {airplane[3]}): ").strip().title() or airplane[3]
            if new_model:
                break
            print("Model cannot be empty\n")

        try:
            self.db.update(
                "Airplanes",
                {"Manufacturer": new_manufacturer, "Model": new_model},
                "AirplaneID",
                airplane_id,
            )
            print(f"Airplane {airplane[1]} updated successfully")
        except Exception as e:
            print(f"Failed to update airplane: {e}\n")
            return


    # Delete an existing airplane record from the database confirming with the user
    def delete_airplane(self) -> None:
        try:
            airplane = get_airplane(self)
        except Exception as e:
            print(f"Error finding airplane: {e}\n")
            return

        confirm = input(f"Enter 'y' to confirm deletion of airplane {airplane[1]} (anything else will cancel): ").lower()
        if confirm == "y":
            try:
                self.db.delete("Airplanes", "AirplaneID", airplane[0])
                print(f"Airplane {airplane[1]} successfully deleted")
            except Exception as e:
                print(f"Failed to delete airplane: {e}\n")
                return
        else:
            print("Cancelled, airplane not deleted")


    # Allocate an airplane to an existing flight checking for any clashes with other flights
    def assign_airplane(self) -> None:
        # Get details about the flight that will be assigned an airplane      
        try:
            flight = get_flight(self)
            flight_id = flight[0]
            flight_num = flight[1]
            flight_dep_time = datetime.strptime(flight[2], "%Y-%m-%d %H:%M")
            flight_arr_time = datetime.strptime(flight[3], "%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"Error finding flight: {e}\n")
            return

        # Get assigned airplane details
        try:
            airplane = get_airplane(self)
            airplane_id = airplane[0]
            airplane_reg = airplane[1]
        except Exception as e:
            print(f"Error finding airplane: {e}\n")
            return

        # Check if the flight clashes with any existing flights the airplane is assigned to
        try:
            clashing_flights = []
            existing_flight_times = self.db.select_fields_by_criteria("Flights", ["FlightNumber", "DepartureTime", "ArrivalTime"], {"AirplaneID": airplane_id})

            for f in existing_flight_times:
                existing_dep_time = datetime.strptime(f[1], "%Y-%m-%d %H:%M")
                existing_arr_time = datetime.strptime(f[2], "%Y-%m-%d %H:%M")

                if (flight_num == f[0]):
                    print(f"Airplane {airplane_reg} is already assigned to flight {f[0]}\n")
                    return
                elif (flight_dep_time < existing_arr_time and flight_arr_time > existing_dep_time):
                    clashing_flights.append(f)

            if clashing_flights:
                print(f"Airplane {airplane_reg} cannot be assigned to flight {flight_num} ({flight_dep_time} - {flight_arr_time}) as this will clash with the following flights:")
                for flight in clashing_flights:
                    print(f"- {flight[0]} ({flight[1]} - {flight[2]})")
                return

            # Assign airplane to flight
            self.db.update("Flights", {"AirplaneID": airplane_id}, "FlightID", flight_id)
            print(f"Airplane {airplane_reg} assigned to flight {flight_num} successfully")

        except Exception as e:
            print(f"Error assigning airplane: {e}\n")
            return
