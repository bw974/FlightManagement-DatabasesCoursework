from datetime import datetime


# Ensure datetime is in correct format YYYY-MM-DD HH:MM
def validate_datetime(datetime_string: str) -> bool:
    try:
        datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


# Check value is an integer
def validate_int(value: any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


# Check the string value is not empty
def validate_nonempty_string(value: str) -> bool:
    return bool(value and value.strip())


# Retrieve the flight record based on a user input flight number
def get_flight(self) -> tuple:
    while True:
        flight_num = input("Enter flight number (e.g. BA123): ").strip().upper()
        flight = self.db.select_by_criteria("Flights", {"FlightNumber": flight_num})
        if not flight:
            print("Flight not found, enter a valid flight number, usage: BAXXX\n")
            continue
        if flight[0][4] == "Cancelled":
            print(f"Flight {flight_num} is cancelled and cannot be updated\n")
            continue
        return flight[0]


# Retrieve a pilot record based on user input pilot name
def get_pilot(self) -> tuple:
    while True:
        pilot_name = input("Enter pilot first and last name (e.g. John Smith): ").strip().title()
        pilot_first_name, pilot_last_name = pilot_name.split()
        pilot = self.db.select_by_criteria("Pilots", {"FirstName": pilot_first_name, "LastName": pilot_last_name})
        if not pilot:
            print("Pilot not found, enter a valid first and last name, usage: Firstname Lastname\n")
            continue
        return pilot[0]


# Retrieve an airplane record based on user input airplane registration
def get_airplane(self) -> tuple:
    while True:
        registration = input("Enter airplane registration (e.g. G-ABCD): ").strip().upper()
        airplane = self.db.select_by_criteria("Airplanes", {"Registration": registration})
        if not airplane:
            print("Airplane not found, enter a valid airplane registration, usage: G-XXXX\n")
            continue
        return airplane[0]


# Retrieve the airport record based on user input airport code
def get_airport(self) -> tuple:
    while True:
        airport_code = input("Enter airport code (e.g. LHR): ").strip().upper()
        airport = self.db.select_by_criteria("Airports", {"AirportCode": airport_code})
        if not airport:
            print("Airport not found, enter a valid airport code, usage: LHR\n")
            continue
        return airport[0]
