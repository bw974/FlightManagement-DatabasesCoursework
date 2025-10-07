-- The below SQL statements have been used throughout the program in a reusable way in python to execute different database operations

-- FlightManagement.db schema which includes all the statements to create each table: Flights, Airports, Pilots and Airplanes
DROP TABLE IF EXISTS Flights
CREATE TABLE Flights(
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
)

DROP TABLE IF EXISTS Airports
CREATE TABLE Airports(
    AirportID INTEGER PRIMARY KEY AUTOINCREMENT,
    AirportCode TEXT UNIQUE NOT NULL,
    AirportName TEXT NOT NULL,
    City TEXT NOT NULL,
    Country TEXT NOT NULL
)

DROP TABLE IF EXISTS Pilots
CREATE TABLE Pilots(
    PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Position TEXT NOT NULL,
    ExperienceYears INTEGER NOT NULL
)

DROP TABLE IF EXISTS Airplanes
CREATE TABLE Airplanes(
    AirplaneID INTEGER PRIMARY KEY AUTOINCREMENT,
    Registration TEXT UNIQUE NOT NULL,
    Manufacturer TEXT NOT NULL,
    Model TEXT NOT NULL
)

-- Example SQL queries for different CRUD operations used throughout the program, some were used programmatically such as INSERT

-- Show details of all flights by joining flight table with airport, pilot and airplanes tables
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

-- Count the number of flights going to each destination and sort by the count in descending order
SELECT FlightID, Destination.AirportCode AS Destination, COUNT(Flights.FlightID) AS NumFlights
FROM Flights
JOIN Airports AS Destination ON Flights.DestinationID = Destination.AirportID
GROUP BY Destination.AirportCode
ORDER BY NumFlights DESC

-- Insert new pilot record to the database
INSERT INTO Pilots
VALUES (None, "Jean", "Paul", "Captain", 12)

-- Update airport record to change the airport name of Heathrow
UPDATE Airports
SET AirportName = "London Heathrow Airport"
WHERE AirportCode = "LHR"

-- Delete an airplane record of reg G-ABCD
DELETE FROM Airplanes
WHERE Registration = "G-ABCD"
