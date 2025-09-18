import sqlite3


def create_sample_data(db_name, table_name, column_names, table_data):

    # Connect to database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Delete table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create table
    cur.execute(f"CREATE TABLE {table_name} {column_names}")

    # Insert data into table
    placeholders = "(" + ",".join(["?"] * len(table_data[0])) + ")"
    cur.executemany(f"INSERT INTO {table_name} VALUES {placeholders}", table_data)

    # Close database
    conn.commit()
    conn.close()


if __name__ == "__main__":

    db_name = "FlightManagement.db"

    flight_table = "Flights"
    flight_columns = """(
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        FlightNumber TEXT UNIQUE NOT NULL,
        DepartureTime TEXT NOT NULL,
        ArrivalTime TEXT NOT NULL,
        Status TEXT,
        DestinationID INTEGER NOT NULL,
        PilotID INTEGER,
        FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID),
        FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID)
    )"""
    flight_data = [
        (None, "AA101", "2025-09-15 08:00", "2025-09-15 12:00", "On Time", 1, 1),
        (None, "AA202", "2025-09-15 09:00", "2025-09-15 13:30", "Delayed", 2, 2),
        (None, "BA303", "2025-09-16 10:00", "2025-09-16 18:00", "On Time", 3, 3),
        (None, "AF404", "2025-09-16 14:00", "2025-09-16 16:00", "Cancelled", 4, 4),
        (None, "JL505", "2025-09-17 07:00", "2025-09-17 19:00", "On Time", 5, 5),
        (None, "QF606", "2025-09-17 22:00", "2025-09-18 07:00", "On Time", 6, 6),
        (None, "EK707", "2025-09-18 03:00", "2025-09-18 09:00", "Delayed", 7, 7),
        (None, "AC808", "2025-09-18 12:00", "2025-09-18 15:00", "On Time", 8, 8),
        (None, "LH909", "2025-09-19 11:00", "2025-09-19 14:00", "On Time", 9, 9),
        (None, "SQ010", "2025-09-19 20:00", "2025-09-20 06:00", "On Time", 10, 10),
        (None, "AA111", "2025-09-20 06:00", "2025-09-20 10:00", "On Time", 1, 2),
        (None, "DL222", "2025-09-20 08:00", "2025-09-20 11:00", "On Time", 2, 3),
        (None, "UA333", "2025-09-21 09:00", "2025-09-21 12:00", "On Time", 1, 4),
        (None, "VA444", "2025-09-21 17:00", "2025-09-22 05:00", "On Time", 6, 5),
        (None, "AI555", "2025-09-22 23:00", "2025-09-23 07:00", "On Time", 10, 6)
    ]

    destination_table = "Destinations"
    destination_columns = """(
        DestinationID INTEGER PRIMARY KEY AUTOINCREMENT,
        City TEXT NOT NULL,
        Country TEXT NOT NULL,
        AirportCode TEXT UNIQUE NOT NULL
    )"""
    destination_data = [
        (None, "New York", "USA", "JFK"),
        (None, "Los Angeles", "USA", "LAX"),
        (None, "London", "UK", "LHR"),
        (None, "Paris", "France", "CDG"),
        (None, "Tokyo", "Japan", "HND"),
        (None, "Sydney", "Australia", "SYD"),
        (None, "Dubai", "UAE", "DXB"),
        (None, "Toronto", "Canada", "YYZ"),
        (None, "Berlin", "Germany", "BER"),
        (None, "Singapore", "Singapore", "SIN")
    ]

    pilot_table = "Pilots"
    pilot_columns = """(
        PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        ExperienceYears INTEGER NOT NULL
    )"""
    pilot_data = [
        (None, "John", "Smith", 15),
        (None, "Alice", "Johnson", 12),
        (None, "David", "Brown", 20),
        (None, "Emma", "Davis", 8),
        (None, "Michael", "Wilson", 25),
        (None, "Sophia", "Taylor", 10),
        (None, "Daniel", "Lee", 18),
        (None, "Olivia", "Martinez", 14),
        (None, "James", "Anderson", 22),
        (None, "Mia", "Thomas", 9)
    ]

    # Create flights table
    create_sample_data(db_name, flight_table, flight_columns, flight_data)

    # Create destinations table
    create_sample_data(db_name, destination_table, destination_columns, destination_data)

    # Create pilots table
    create_sample_data(db_name, pilot_table, pilot_columns, pilot_data)
