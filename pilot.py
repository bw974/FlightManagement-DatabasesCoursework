from cli import print_table
from database import DBOperations
from datetime import datetime
from utils import validate_int, get_flight, get_pilot


class Pilot:
    # Initialise DBOperations and use the class functions to interact with the database
    def __init__(self):
        self.db = DBOperations()


    #  View all pilots stored in the database
    def view_all_pilots(self) -> None:
        pilots = self.db.select_all("Pilots")
        if not pilots:
            print("No pilots listed in database")
            return
        columns = ["PilotID", "First Name", "Last Name", "Position", "Experience (Years)"]
        print_table(pilots, columns, title="Information on all pilots")


    # Add a new pilot to the database checking for valid user input
    def add_new_pilot(self) -> None:
        while True:
            first_name = input("Enter pilot's first name: ").strip().title()
            if first_name:
                break
            print("First name cannot be empty\n")

        while True:
            last_name = input("Enter pilot's last name: ").strip().title()
            if last_name:
                break
            print("Last name cannot be empty\n")

        while True:
            position = input("Enter pilot's position (Captain, First Officer or Second Officer): ").strip().title()
            if position in ["Captain", "First Officer", "Second Officer"]:
                break
            print("Invalid position format, choose either: Captain, First Officer or Second Officer\n")

        while True:
            exp_years = input("Enter pilot's years of experience: ").strip()
            if validate_int(exp_years):
                exp_years = int(exp_years)
                break
            print("Invalid input, enter a valid integer\n")

        self.db.insert("Pilots", (None, first_name, last_name, position, exp_years))
        print("New pilot added successfully")
    

    # Update an existing pilot's details
    def update_pilot(self) -> None:
        try:
            pilot = get_pilot(self)
        except Exception as e:
            print(f"Error finding pilot: {e}\n")
            return

        pilot_id = pilot[0]
        print("Enter nothing to keep current value:")

        while True:
            new_first_name = input(f"Enter new first name (current: {pilot[1]}): ").strip().title() or pilot[1]
            if new_first_name:
                break
            print("First name cannot be empty\n")

        while True:
            new_last_name = input(f"Enter new last name (current: {pilot[2]}): ").strip().title() or pilot[2]
            if new_last_name:
                break
            print("Last name cannot be empty\n")

        while True:
            new_position = input(f"Enter new position (current: {pilot[3]}): ").strip().title() or pilot[3]
            if new_position in ["Captain", "First Officer", "Second Officer"]:
                break
            print("Invalid position format, choose either: Captain, First Officer or Second Officer\n")

        while True:
            new_exp_years = input(f"Enter new experience years (current: {pilot[4]}): ").strip() or pilot[4]
            if validate_int(new_exp_years):
                new_exp_years = int(new_exp_years)
                break
            print("Invalid experience years format, enter a valid integer\n")

        try:
            self.db.update(
                "Pilots",
                {"FirstName": new_first_name, "LastName": new_last_name, "Position": new_position, "ExperienceYears": new_exp_years},
                "PilotID",
                pilot_id,
            )
            print(f"Pilot {new_first_name} {new_last_name} updated successfully")
        except Exception as e:
            print(f"Failed to update pilot: {e}\n")
            return
    

    # Delete an existing pilot record from the database, confirming with the user
    def delete_pilot(self) -> None:
        try:
            pilot = get_pilot(self)
        except Exception as e:
            print(f"Error finding pilot: {e}\n")
            return

        confirm = input(f"Enter 'y' to confirm deletion of pilot {pilot[1]} {pilot[2]} (anything else will cancel): ").lower()
        if confirm == "y":
            try:
                self.db.delete("Pilots", "PilotID", pilot[0])
                print(f"Pilot {pilot[1]} {pilot[2]} successfully deleted")
            except Exception as e:
                print(f"Failed to delete pilot: {e}\n")
                return
        else:
            print("Cancelled, pilot not deleted")


    # Assign a pilot to an existing flight checking any clashes with other flights
    def assign_pilot(self) -> None:
        # Get details about the flight that will be assigned a pilot      
        try:
            flight = get_flight(self)
            flight_id = flight[0]
            flight_num = flight[1]
            flight_status = flight[4]
            if flight_status == "Cancelled":
                print(f"Flight {flight_num} is cancelled and cannot be updated\n")
                return
            flight_dep_time = datetime.strptime(flight[2], "%Y-%m-%d %H:%M")
            flight_arr_time = datetime.strptime(flight[3], "%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"Error finding flight: {e}\n")
            return

        # Get assigned pilot details
        try:
            pilot = get_pilot(self)
            pilot_id = pilot[0]
            pilot_name = f"{pilot[1]} {pilot[2]}"
        except Exception as e:
            print(f"Error finding pilot: {e}\n")
            return
    
        # Check if the flight clashes with the pilot's existing schedule
        try:
            clashing_flights = []
            existing_flight_times = self.db.select_fields_by_criteria("Flights", ["FlightNumber", "DepartureTime", "ArrivalTime"], {"PilotID": pilot_id})

            for f in existing_flight_times:
                existing_dep_time = datetime.strptime(f[1], "%Y-%m-%d %H:%M")
                existing_arr_time = datetime.strptime(f[2], "%Y-%m-%d %H:%M")

                if (flight_num == f[0]):
                    print(f"Pilot {pilot_name} is already assigned to flight {f[0]}")
                    return
                elif (flight_dep_time < existing_arr_time and flight_arr_time > existing_dep_time):
                    clashing_flights.append(f)

            if clashing_flights:
                print(f"Pilot {pilot_name} cannot be assigned to flight {flight_num} ({flight_dep_time} - {flight_arr_time}) as this will clash with the following flights:")
                for flight in clashing_flights:
                    print(f"- {flight[0]} ({flight[1]} - {flight[2]})")
                return

            # Assign pilot to flight
            self.db.update("Flights", {"PilotID": pilot_id}, "FlightID", flight_id)
            print(f"Pilot {pilot_name} assigned to flight {flight_num} successfully")

        except Exception as e:
            print(f"Error assigning pilot: {e}")


    # View a particular pilot's flight schedule listing all the flights assigned to them
    def view_pilot_schedule(self) -> None:
        # Get pilot details
        try:
            pilot = get_pilot(self)
            pilot_id = pilot[0]
            pilot_name = f"{pilot[1]} {pilot[2]}"
        except Exception as e:
            print(f"Error finding pilot: {e}\n")
            return

        # Get pilot's flight schedule
        flights = self.db.select_flights_with_joins({"Flights.PilotID": pilot_id})

        columns = ["FlightID", "Flight Number", "Departure Time", "Arrival Time", "Status", "Origin", "Destination", "Pilot", "Airplane"]
        print_table(flights, columns, title=f"Flight Schedule for Pilot {pilot_name}")
