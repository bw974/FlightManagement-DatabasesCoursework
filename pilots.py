from cli import print_table
from database import DBOperations
from utils import validate_int


class PilotQueries:
    def __init__(self):
        self.db = DBOperations()


    def view_pilot_info(self):
        pilots = self.db.select_all("Pilots")
        if not pilots:
            print("No pilots listed in database")
            return
        columns = ["PilotID", "First Name", "Last Name", "Position", "Experience (Years)"]
        print_table(pilots, columns, title="Pilot Info")


    def add_new_pilot(self):
        first_name = input("Enter pilot's first name: ").strip().title()
        last_name = input("Enter pilot's last name: ").strip().title()
        
        while True:
            position = input("Enter pilot's position (Captain, First Officer or Second Officer): ").strip().title()
            if position in ["Captain", "First Officer", "Second Officer"]:
                break
            print("Invalid position format, choose either: Captain, First Officer or Second Officer")

        while True:
            exp_years = input("Enter pilot's years of experience: ").strip()
            if validate_int(exp_years):
                exp_years = int(exp_years)
                break
            print("Invalid input, enter a valid integer")

        self.db.insert("Pilots", (None, first_name, last_name, position, exp_years))
        print("New pilot added successfully")
    

    def update_pilot(self):
        first_name = input("Enter first name of the pilot to update: ").strip().title()
        last_name = input("Enter last name of the pilot to update: ").strip().title()

        pilot = self.db.select("Pilots", "FirstName", first_name)
        if not pilot or pilot[2] != last_name:  # pilot[2] is LastName
            print("Pilot not found.")
            return

        pilot_id = pilot[0]
        print("Leave field blank to keep current value.")

        first_name = input(f"New first name ({pilot[1]}): ").strip().title() or pilot[1]
        last_name = input(f"New last name ({pilot[2]}): ").strip().title() or pilot[2]
        position = input(f"New position ({pilot[3]}): ").strip().title() or pilot[3]

        while True:
            exp_years = input(f"New experience years ({pilot[4]}): ").strip()
            if not exp_years:
                exp_years = pilot[4]
                break
            if validate_int(exp_years):
                exp_years = int(exp_years)
                break
            print("Invalid input. Enter a valid integer.")

        self.db.update(
            "Pilots",
            {"FirstName": first_name, "LastName": last_name, "Position": position, "ExperienceYears": exp_years},
            "PilotID",
            pilot_id,
        )
        print("Pilot updated successfully.")
    

    def delete_pilot(self):
        first_name = input("Enter first name of the pilot to delete: ").strip().title()
        last_name = input("Enter last name of the pilot to delete: ").strip().title()

        pilot = self.db.select("Pilots", "FirstName", first_name)
        if not pilot or pilot[2] != last_name:
            print("Pilot not found.")
            return

        confirm = input(f"Are you sure you want to delete {first_name} {last_name}? (y/n): ").lower()
        if confirm == "y":
            self.db.delete("Pilots", "PilotID", pilot[0])
            print("Pilot deleted successfully.")
        else:
            print("Delete cancelled.")
