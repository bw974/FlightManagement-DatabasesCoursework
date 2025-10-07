import re
from cli import print_table
from database import DBOperations
from utils import get_airport


class Airport:
    # Initialise DBOperations and use the class functions to interact with the database
    def __init__(self):
        self.db = DBOperations()


    # View all airports stored in the database
    def view_all_airports(self) -> None:
        airports = self.db.select_all("Airports")
        if not airports:
            print("No airports listed in database")
            return
        columns = ["AirportID", "Airport Code", "Airport Name", "City", "Country"]
        print_table(airports, columns, title="Information on all airports")
    

    # Add a new airport to the database checking for valid user input
    def add_new_airport(self) -> None:      
        while True:
            airport_code = input("Enter airport code of airport to add: ").strip().upper()
            if not bool(re.fullmatch(r"[A-Z]{3}", airport_code)):
                print("Invalid airport code format, usage: LHR\n")
                continue
            elif self.db.select_by_criteria("Airports", {"AirportCode": airport_code}):
                print(f"Airport {airport_code} already exists\n")
                continue
            break
        
        while True:
            airport_name = input("Enter airport name: ").strip().title()
            if airport_name:
                break
            print("Airport name cannot be empty\n")

        while True:
            city = input("Enter airport city: ").strip().title()
            if city:
                break
            print("City cannot be empty\n")

        while True:
            country = input("Enter airport country: ").strip().title()
            if country:
                break
            print("Country cannot be empty\n")

        self.db.insert("Airports", (None, airport_code, airport_name, city, country))
        print(f"Airport {airport_code} added successfully")
    

    # Update an existing airport's details
    def update_airport(self) -> None:
        try:
            airport = get_airport(self)
        except Exception as e:
            print(f"Error finding airport: {e}\n")
            return

        airport_id = airport[0]
        print("Enter nothing to keep current value:")

        while True:
            new_airport_name = input(f"Enter new airport name (current: {airport[2]}): ").strip().title() or airport[2]
            if new_airport_name:
                break
            print("Airport name cannot be empty\n")

        while True:
            new_city = input(f"Enter new airport city (current: {airport[3]}): ").strip().title() or airport[3]
            if new_city:
                break
            print("City cannot be empty\n")

        while True:
            new_country = input(f"Enter new airport country (current: {airport[4]}): ").strip().title() or airport[4]
            if new_country:
                break
            print("Country cannot be empty\n")

        try:
            self.db.update(
                "Airports",
                {"AirportName": new_airport_name, "City": new_city, "Country": new_country},
                "AirportID",
                airport_id,
            )
            print(f"Airport {airport[1]} updated successfully")
        except Exception as e:
            print(f"Failed to update airport: {e}\n")
            return


    # Delete an existing airport record from the database confirming with the user
    def delete_airport(self) -> None:
        try:
            airport = get_airport(self)
        except Exception as e:
            print(f"Error finding airport: {e}\n")
            return

        confirm = input(f"Enter 'y' to confirm deletion of airport {airport[1]} (anything else will cancel): ").lower()
        if confirm == "y":
            try:
                self.db.delete("Airports", "AirportID", airport[0])
                print(f"Airport {airport[1]} successfully deleted")
            except Exception as e:
                print(f"Failed to delete airport: {e}\n")
                return
        else:
            print("Cancelled, airport not deleted")
