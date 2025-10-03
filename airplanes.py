from cli import print_table
from database import DBOperations
from utils import validate_nonempty_string


class AirplaneQueries:
    def __init__(self):
        self.db = DBOperations()


    def view_airplane_info(self):
        airplanes = self.db.select_all("Airplanes")
        if not airplanes:
            print("No airplanes listed in the database")
            return
        columns = ["AirplaneID", "Registration", "Manufacturer", "Model"]
        print_table(airplanes, columns, title="Airplane Info")


    def add_new_airplane(self):
        while True:
            registration = input("Enter airplane registration number (e.g., G-ABCD): ").strip().upper()
            if validate_nonempty_string(registration) and registration.startswith("G-") and len(registration) == 6:
                break
            print("Invalid registration format. Usage: G-XXXX")

        manufacturer = input("Enter manufacturer: ").strip().title()
        while not validate_nonempty_string(manufacturer):
            print("Manufacturer cannot be empty.")
            manufacturer = input("Enter manufacturer: ").strip().title()

        model = input("Enter model: ").strip().title()
        while not validate_nonempty_string(model):
            print("Model cannot be empty.")
            model = input("Enter model: ").strip().title()

        try:
            self.db.insert("Airplanes", (None, registration, manufacturer, model))
            print(f"Airplane {registration} added successfully.")
        except Exception as e:
            print(f"Failed to add airplane: {e}")


    def update_airplane(self):
        registration = input("Enter registration number of the airplane to update: ").strip().upper()
        airplane = self.db.select("Airplanes", "Registration", registration)
        if not airplane:
            print("Airplane not found.")
            return

        airplane_id = airplane[0]
        print("Leave field blank to keep current value.")
        new_reg = input(f"New registration ({airplane[1]}): ").strip().upper() or airplane[1]
        new_manufacturer = input(f"New manufacturer ({airplane[2]}): ").strip().title() or airplane[2]
        new_model = input(f"New model ({airplane[3]}): ").strip().title() or airplane[3]

        try:
            self.db.update(
                "Airplanes",
                {"Registration": new_reg, "Manufacturer": new_manufacturer, "Model": new_model},
                "AirplaneID",
                airplane_id,
            )
            print(f"Airplane {new_reg} updated successfully.")
        except Exception as e:
            print(f"Failed to update airplane: {e}")


    def delete_airplane(self):
        registration = input("Enter registration number of the airplane to delete: ").strip().upper()
        airplane = self.db.select("Airplanes", "Registration", registration)
        if not airplane:
            print("Airplane not found.")
            return

        confirm = input(f"Are you sure you want to delete airplane {registration}? (y/n): ").lower()
        if confirm == "y":
            try:
                self.db.delete("Airplanes", "AirplaneID", airplane[0])
                print(f"Airplane {registration} deleted successfully.")
            except Exception as e:
                print(f"Failed to delete airplane: {e}")
        else:
            print("Delete cancelled.")
