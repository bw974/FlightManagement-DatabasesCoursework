import sqlite3
import config

# This class defines functions for interacting with the database using SQL queries and sqlite3
class DBOperations:
    # Initialise DBOperations objects with a connection to the database
    def __init__(self, db="FlightManagement.db"):
        try:
            self.con = sqlite3.connect(db)
            self.cur = self.con.cursor()
        except Exception as e:
            print(f"Failed to connect to {db}: {e}")
            

    # SQL query to create a table in the database with specified headings
    def create_table(self, table, headings) -> None:
        self.cur.execute(f"DROP TABLE IF EXISTS {table}")
        self.cur.execute(f"CREATE TABLE {table} {headings}")
        self.con.commit()


    # SQL query to insert a new record into a specified table
    def insert(self, table: str, values: tuple) -> None:
        parameters = ",".join("?" * len(values))
        self.cur.execute(f"INSERT INTO {table} VALUES({parameters})", values)
        self.con.commit()


    # SQL query to return all records from a table
    def select_all(self, table: str) -> list[tuple]:
        self.cur.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()


    # SQL query to return records filtered by a specified criteria condition
    def select_by_criteria(self, table: str, criteria: dict) -> list[tuple]:
        condition = " AND ".join([f"{c} = ?" for c in criteria.keys()])
        self.cur.execute(f"SELECT * FROM {table} WHERE {condition}", tuple(criteria.values()))
        return self.cur.fetchall()


    # SQL query to return specified columns of records filtered based on criteria
    def select_fields_by_criteria(self, table: str, fields: list[str], criteria: dict) -> list[tuple]:
        cols = ",".join(fields)
        condition = " AND ".join([f"{col} = ?" for col in criteria.keys()])
        self.cur.execute(f"SELECT {cols} FROM {table} WHERE {condition}", tuple(criteria.values()))
        return self.cur.fetchall()
    

    # SQL query to return flight table data joined with airport, pilot and airplane details
    def select_flights_with_joins(self, criteria: dict | None = None) -> list[tuple]:
        query = """
            SELECT Flights.FlightID,
                Flights.FlightNumber,
                Flights.DepartureTime,
                Flights.ArrivalTime,
                Flights.Status,
                Origin.AirportCode AS Origin,
                Destination.AirportCode AS Destination,
                CONCAT(Pilots.FirstName, " ", Pilots.LastName) AS Pilot,
                Airplanes.Registration AS Airplane
            FROM Flights
            JOIN Airports AS Origin ON Flights.OriginID = Origin.AirportID
            JOIN Airports AS Destination ON Flights.DestinationID = Destination.AirportID
            LEFT JOIN Pilots ON Flights.PilotID = Pilots.PilotID
            LEFT JOIN Airplanes ON Flights.AirplaneID = Airplanes.AirplaneID
        """

        params = ()
        if criteria:
            condition = " WHERE " + " AND ".join([f"{col} = ?" for col in criteria.keys()])
            query += condition
            params = tuple(criteria.values())

        query += " ORDER BY Flights.DepartureTime"
        self.cur.execute(query, params)
        return self.cur.fetchall()
    

    # SQL query to return count of flights per origin airport
    def select_flights_per_origin(self) -> list[tuple]:
        query = """
            SELECT FlightID, Origin.AirportCode AS Origin, COUNT(Flights.FlightID) AS NumFlights
            FROM Flights
            JOIN Airports AS Origin ON Flights.OriginID = Origin.AirportID
            GROUP BY Origin.AirportCode
            ORDER BY NumFlights DESC
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    # SQL query to return count of flights per destination airport
    def select_flights_per_destination(self) -> list[tuple]:
        query = """
            SELECT FlightID, Destination.AirportCode AS Destination, COUNT(Flights.FlightID) AS NumFlights
            FROM Flights
            JOIN Airports AS Destination ON Flights.DestinationID = Destination.AirportID
            GROUP BY Destination.AirportCode
            ORDER BY NumFlights DESC
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    # SQL query to return count of flights per pilot, ensuring those unassigned pilots are not counted 
    def select_flights_per_pilot(self) -> list[tuple]:
        query = """
            SELECT FlightID, CONCAT(Pilots.FirstName, " ", Pilots.LastName) AS Pilot, COUNT(Flights.FlightID) AS NumFlights
            FROM Flights
            LEFT JOIN Pilots ON Flights.PilotID = Pilots.PilotID
            WHERE Pilot != " "
            GROUP BY Pilot
            ORDER BY NumFlights DESC
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    # SQL query to return count of flights per airplane, ensuring unassigned airplanes are not counted
    def select_flights_per_airplane(self) -> list[tuple]:
        query = """
            SELECT FlightID, Airplanes.Registration AS Airplane, COUNT(Flights.FlightID) AS NumFlights
            FROM Flights
            LEFT JOIN Airplanes ON Flights.AirplaneID = Airplanes.AirplaneID
            WHERE Airplane NOT NULL
            GROUP BY Airplane
            ORDER BY NumFlights DESC
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    # SQL query to update a particular record defined by a certain criteria
    def update(self, table: str, updates: dict, criteria: str, value) -> None:
        set_clause = ",".join([f"{col}=?" for col in updates.keys()])
        params = list(updates.values()) + [value]
        self.cur.execute(f"UPDATE {table} SET {set_clause} WHERE {criteria} = ?", params)
        self.con.commit()


    # SQL query to delete a specified record
    def delete(self, table: str, criteria: str, value) -> None:
        self.cur.execute(f"DELETE FROM {table} WHERE {criteria} = ?", (value,))
        self.con.commit()


    # Commit changes and close the database connection
    def commit_and_close(self):
        self.con.commit()
        self.con.close()


# Set up the database by creating and populating the tables
def setup_database():
    # Create DBOperations object to connect and interact with the database
    db = DBOperations()

    for table, headings in config.tables.items():
        db.create_table(table, headings)
        for values in config.sample_data[table]:
            db.insert(table, values)
    db.commit_and_close()
    print("\nSuccessfully reset database with sample data\n")
