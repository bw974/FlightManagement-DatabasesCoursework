import sqlite3

# This class defines functions for interacting with the database using SQL queries and sqlite3
class DBOperations:
    # Initialise DBOperations objects with a connection to the database
    def __init__(self, db="FlightManagement.db"):
        try:
            self.con = sqlite3.connect(db)
            self.cur = self.con.cursor()
        except Exception as e:
            print(f"Failed to connect to {db}: {e}")
            

    def create_table(self, table, headings) -> None:
        self.cur.execute(f"DROP TABLE IF EXISTS {table}")
        self.cur.execute(f"CREATE TABLE {table} {headings}")
        self.con.commit()


    def insert(self, table: str, values: tuple) -> None:
        parameters = ",".join("?" * len(values))
        self.cur.execute(f"INSERT INTO {table} VALUES({parameters})", values)
        self.con.commit()


    def select(self, table: str, criteria: str, value: str) -> tuple:
        self.cur.execute(f"SELECT * FROM {table} WHERE {criteria} = ?", (value,))
        return self.cur.fetchone()


    def select_all(self, table: str) -> list[tuple]:
        self.cur.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()


    def update(self, table: str, updates: dict, criteria: str, value) -> None:
        set_clause = ",".join([f"{col}=?" for col in updates.keys()])
        params = list(updates.values()) + [value]
        self.cur.execute(f"UPDATE {table} SET {set_clause} WHERE {criteria} = ?", params)
        self.con.commit()


    def delete(self, table: str, criteria: str, value) -> None:
        self.cur.execute(f"DELETE FROM {table} WHERE {criteria} = ?", (value,))
        self.con.commit()


    def commit_and_close(self):
        self.con.commit()
        self.con.close()


# Set up the database by creating and populating the tables
def setup_database():
    # Create DBOperations object to connect and interact with the database
    db = DBOperations()

    tables = {
        "Flights": """(
            FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightNumber TEXT UNIQUE NOT NULL,
            DepartureTime TEXT NOT NULL,
            ArrivalTime TEXT,
            Status TEXT NOT NULL,
            OriginID INTERGER NOT NULL,
            DestinationID INTEGER NOT NULL,
            PilotID INTEGER,
            AirplaneID INTEGER,
            FOREIGN KEY (OriginID) REFERENCES Airports(AirportID),
            FOREIGN KEY (DestinationID) REFERENCES Airports(AirportID),
            FOREIGN KEY (PilotID) REFERENCES Pilots(PilotID),
            FOREIGN KEY (AirplaneID) REFERENCES Airplanes(AirplaneID)
        )""",
        "Airports": """(
            AirportID INTEGER PRIMARY KEY AUTOINCREMENT,
            AirportCode TEXT UNIQUE NOT NULL,
            AirportName TEXT NOT NULL,
            City TEXT NOT NULL,
            Country TEXT NOT NULL
        )""",
        "Pilots": """(
            PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Position TEXT NOT NULL,
            ExperienceYears INTEGER NOT NULL
        )""",
        "Airplanes": """(
            AirplaneID INTEGER PRIMARY KEY AUTOINCREMENT,
            Registration TEXT UNIQUE NOT NULL,
            Manufacturer TEXT NOT NULL,
            Model TEXT NOT NULL
        )"""
    }

    sample_data = {
        "Flights": [
            (None, "BA101", "2025-09-15 08:00", "2025-09-15 12:00", "On Time", 1, 2, 1, 1),
            (None, "BA102", "2025-09-15 09:00", "2025-09-15 13:30", "Delayed", 2, 3, 2, 2),
            (None, "BA103", "2025-09-16 10:00", "2025-09-16 18:00", "On Time", 3, 4, 3, 3),
            (None, "BA104", "2025-09-16 14:00", None, "Cancelled", 4, 5, 4, 4),
            (None, "BA105", "2025-09-17 07:00", "2025-09-17 19:00", "On Time", 5, 6, 5, 5),
            (None, "BA106", "2025-09-17 22:00", "2025-09-18 07:00", "On Time", 6, 7, 6, 6),
            (None, "BA107", "2025-09-18 03:00", "2025-09-18 09:00", "Delayed", 7, 8, 7, 7),
            (None, "BA108", "2025-09-18 12:00", "2025-09-18 15:00", "On Time", 8, 9, 8, 8),
            (None, "BA109", "2025-09-19 11:00", "2025-09-19 14:00", "On Time", 9, 10, 9, 9),
            (None, "BA110", "2025-09-19 20:00", "2025-09-20 06:00", "On Time", 10, 1, 10, 10),
            (None, "BA111", "2025-09-20 06:00", "2025-09-20 10:00", "On Time", 1, 3, 2, 2),
            (None, "BA112", "2025-09-20 08:00", "2025-09-20 11:00", "On Time", 2, 5, 3, 3),
            (None, "BA113", "2025-09-21 09:00", "2025-09-21 12:00", "On Time", 1, 4, 4, 4),
            (None, "BA114", "2025-09-21 17:00", "2025-09-22 05:00", "On Time", 6, 2, 5, 5),
            (None, "BA115", "2025-09-22 23:00", "2025-09-23 07:00", "On Time", 10, 7, 6, 6)
        ],
        "Airports": [
            (None, "JFK", "John F. Kennedy International Airport", "New York", "USA"),
            (None, "LAX", "Los Angeles International Airport", "Los Angeles", "USA"),
            (None, "LHR", "Heathrow Airport", "London", "UK"),
            (None, "CDG", "Charles de Gaulle Airport", "Paris", "France"),
            (None, "HND", "Haneda Airport", "Tokyo", "Japan"),
            (None, "SYD", "Sydney Kingsford Smith Airport", "Sydney", "Australia"),
            (None, "DXB", "Dubai International Airport", "Dubai", "UAE"),
            (None, "YYZ", "Toronto Pearson International Airport", "Toronto", "Canada"),
            (None, "BER", "Berlin Brandenburg Airport", "Berlin", "Germany"),
            (None, "SIN", "Singapore Changi Airport", "Singapore", "Singapore")
        ],
        "Pilots": [
            (None, "John", "Smith", "Captain", 15),
            (None, "Alice", "Johnson", "First Officer", 12),
            (None, "David", "Brown", "Captain", 20),
            (None, "Emma", "Davis", "Second Officer", 6),
            (None, "Michael", "Wilson", "Captain", 25),
            (None, "Sophia", "Taylor", "Second Officer", 7),
            (None, "Daniel", "Lee", "Captain", 18),
            (None, "Olivia", "Martinez", "First Officer", 14),
            (None, "James", "Anderson", "Captain", 22),
            (None, "Mia", "Thomas", "First Officer", 11)
        ],
        "Airplanes": [
            (None, "G-ABCD", "Boeing", "737-800"),
            (None, "G-EFGH", "Boeing", "737-800"),
            (None, "G-IJKL", "Airbus", "A320"),
            (None, "G-MNOP", "Airbus", "A320"),
            (None, "G-QRST", "Boeing", "777-300ER"),
            (None, "G-UVWX", "Boeing", "777-300ER"),
            (None, "G-YZAB", "Airbus", "A350-900"),
            (None, "G-CDEF", "Boeing", "787-9 Dreamliner"),
            (None, "G-GHIJ", "Embraer", "E195"),
            (None, "G-KLMN", "Bombardier", "CS300"),
            (None, "G-OPQR", "Airbus", "A380-800"),
            (None, "G-STUV", "Boeing", "747-400"),
            (None, "G-WXYZ", "Airbus", "A380-800")
        ]
    }

    for table, headings in tables.items():
        db.create_table(table, headings)
        for values in sample_data[table]:
            db.insert(table, values)
    db.commit_and_close()
    print("Database reset")
