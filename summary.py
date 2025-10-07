from cli import print_table
from database import DBOperations


class Summary:
    # Initialise DBOperations and use the class functions to interact with the database
    def __init__(self):
        self.db = DBOperations()


    # Count and print the number of flights per origin airport
    def num_flights_per_origin(self) -> None:
        flights_per_origin = self.db.select_flights_per_origin()
        if not flights_per_origin:
            print("No flights listed in the database")
            return
        columns = ["FlightID", "Origin Airport", "Number of Flights"]
        print_table(flights_per_origin, columns, title="Number of flights from each origin")
        return


    # Count and print the number of flights per destination airport
    def num_flights_per_destination(self) -> None:
        flights_per_destination = self.db.select_flights_per_destination()
        if not flights_per_destination:
            print("No flights listed in the database")
            return
        columns = ["FlightID", "Destination Airport", "Number of Flights"]
        print_table(flights_per_destination, columns, title="Number of flights to each destination")
        return


    # Count and print the number of flights per pilot
    def num_flights_per_pilot(self) -> None:
        flights_per_pilot = self.db.select_flights_per_pilot()
        if not flights_per_pilot:
            print("No flights listed in the database")
            return
        columns = ["FlightID", "Pilot", "Number of Flights"]
        print_table(flights_per_pilot, columns, title="Number of flights allocated to each pilot")
        return


    # Count and print the number of flights per airplane
    def num_flights_per_airplane(self) -> None:
        flights_per_airplane = self.db.select_flights_per_airplane()
        if not flights_per_airplane:
            print("No flights listed in the database")
            return
        columns = ["FlightID", "Airplane", "Number of Flights"]
        print_table(flights_per_airplane, columns, title="Number of flights allocated to each airplane")
