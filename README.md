# Flight Management System

Welcome to the BathAirways Flight Management System!

## Requirements:

- Python version 3.10+
- Rich library for coloured terminal output (see step 2)

## Installation

1. To run this application, first clone this repository and change directory to where `main.py` is located:

```
git clone https://github.com/bw974/FlightManagement-DatabasesCoursework.git

cd FlightManagement-DatabasesCoursework
```

2. Secondly, install the required dependencies (`rich`):

```
pip install -r requirements.txt
```

3. Next, run the main program and you should see the UI of the CLI program in your terminal:

```
python main.py
```

4. The `FlightManagement.db` database in this system uses `sqlite3` and persists data even when the program is closed and ran multiple times. The system features a `Database Reset` option to re-populate the database with sample data if you need to reset it for any reason.