# Config file for BathAirways flight management system
# This contains the CLI UI elements, menu options, database schema and sample data to populate the DB with

logo = r"""
 ____        _   _        _    _                              
| __ )  __ _| |_| |__    / \  (_)_ ____      ____ _ _   _ ___ 
|  _ \ / _` | __| '_ \  / _ \ | | '__\ \ /\ / / _` | | | / __|
| |_) | (_| | |_| | | |/ ___ \| | |   \ V  V / (_| | |_| \__ \
|____/ \__,_|\__|_| |_/_/   \_\_|_|    \_/\_/ \__,_|\__, |___/
                                                    |___/      
"""

title="[bold italic cyan]University of Bath: Databases and Cloud[/bold italic cyan]"

subtitle="[bold yellow]Flight Management System[/bold yellow]"

main_menu_options = [
    "1. Flight Management",
    "2. Pilot Management",
    "3. Airport Management",
    "4. Airplane Management",
    "5. Summary Data",
    "6. Database Reset",
    "0. Exit"
]

flight_menu_options = [
    "1. Add a New Flight",
    "2. View Flights by Criteria",
    "3. View All Flight Information",
    "4. Update Flight Information",
    "5. Delete a Flight",
    "0. Back"
]

pilot_menu_options = [
    "1. Add a New Pilot",
    "2. View Pilot Schedule",
    "3. View All Pilot Information",
    "4. Update Pilot Information",
    "5. Assign Pilot to Flight",
    "6. Delete a Pilot",
    "0. Back"
]

airport_menu_options = [
    "1. Add a New Airport",
    "2. View All Airport Information",
    "3. Update Airport Information",
    "4. Delete an Airport",
    "0. Back"
]

airplane_menu_options = [
    "1. Add a New Airplane",
    "2. View All Airplane Information",
    "3. Update Airplane Information",
    "4. Assign Airplane to Flight",
    "5. Delete an Airplane",
    "0. Back"
]

summary_menu_options = [
    "1. View Number of Flights per Origin",
    "2. View Number of Flights per Destination",
    "3. View Number of Flights per Pilot",
    "4. View Number of Flights per Airplane",
    "0. Back"
]

tables = {
    "Flights": """(
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        FlightNumber TEXT UNIQUE NOT NULL,
        DepartureTime TEXT,
        ArrivalTime TEXT,
        Status TEXT NOT NULL,
        OriginID INTEGER NOT NULL,
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
        (None, "BA104", None, None, "Cancelled", 4, 5, None, None),
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
