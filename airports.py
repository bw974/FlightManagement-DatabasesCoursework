import re
from cli import print_table
from database import DBOperations


class AirportQueries:
    def __init__(self):
        self.db = DBOperations()


    def view_airport_info(self):
        airports = self.db.select_all("Airports")
        if not airports:
            print("No airports listed in database")
            return
        columns = ["AirportID", "Airport Code", "Airport Name", "City", "Country"]
        print_table(airports, columns, title="Airport Info")
    

    def add_new_airport(self):      
        while True:
            airport_code = input("Enter airport code of airport to add: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{3}", airport_code)):
                break
            print("Invalid airport code format, usage: LHR")

        airport_name = input("Enter airport name: ").strip().title()
        city = input("Enter airport city: ").strip().title()
        country = input("Enter airport country: ").strip().title()

        self.db.insert("Airports", (None, airport_code, airport_name, city, country))
        print("New airport added successfully")
    

    def update_airport(self):
        while True:
            airport_code = input("Enter airport code of airport to update: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{3}", airport_code)):
                airport = self.db.select("Airports", "AirportCode", airport_code)
                if airport:
                    break
                print(f"Airport {airport_code} not found")
            else:
                print("Invalid airport code format, usage: LHR")

        dest_id = airport[0]
        print("Leave field blank to keep current value.")

        airport_code = input(f"New airport code ({airport[1]}): ").strip().title() or airport[1]
        airport_name = input(f"New airport name ({airport[2]}): ").strip().title() or airport[2]
        city = input(f"New airport city ({airport[3]}): ").strip().title() or airport[3]
        country = input(f"New airport country ({airport[4]}): ").strip().title() or airport[4]

        self.db.update(
            "Airports",
            {"AirportCode": airport_code, "AirportName": airport_name, "City": city, "Country": country},
            "AirportID",
            dest_id,
        )
        print(f"Airport {airport_code} updated successfully.")
    

    def delete_airport(self):
        while True:
            airport_code = input("Enter airport code of airport to delete: ").strip().upper()
            if bool(re.fullmatch(r"[A-Z]{3}", airport_code)):
                airport = self.db.select("airports", "AirportCode", airport_code)
                if airport:
                    break
                print(f"Airport {airport_code} not found")
            else:
                print("Invalid airport code format, usage: LHR")

        confirm = input(f"Are you sure you want to delete airport {airport_code}? (y/n): ").lower()
        if confirm == "y":
            self.db.delete("Airports", "AirportID", airport[0])
            print(f"Airport {airport_code} deleted successfully.")
        else:
            print("Delete cancelled.")
