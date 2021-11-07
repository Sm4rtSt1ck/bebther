import sqlite3
from main import debug
import datetime
import pathlib

db = sqlite3.Connection


def start() -> None:
    """Opening the database file if possible"""
    global db
    # Trying to connect to the database
    try:
        db = sqlite3.connect(
            f"{pathlib.Path(__file__).parent.resolve()}/Database/weather.db")
        debug(f"Database opened")
    except Exception as e:
        debug(f"Exception on opening database: {e}")
        quit()
    initialize()


def initialize() -> None:
    """Adding tables to the database if needed"""
    # Additional check if the database file was lost
    if db is None:
        debug(f"Database not found. Exiting")
        quit()
    # Creating tables if those does not exist
    db.execute("""CREATE TABLE IF NOT EXISTS Weather(
        Date date PRIMARY KEY,
        City text NOT NULL,
        Source text NOT NULL,
        Temperature float,
        TemperatureNight float,
        TemperatureDay float,
        Pressure float,
        Ultraviolet integer,
        SunriseTime time,
        SunsetTime time,
        Humidity float,
        WindSpeed float
    )
    """)
    debug("Database initialized")


def write(data) -> bool:
    """Write data to the database
    :param data: Formatted dict() of data"""
    debug(data["Date"].strftime("%Y-%m-%d"))
    global db
    # Checking if data is provided
    if data is None:
        debug("No data was provided, exiting the function")
        return False
    try:
        # Writing data to the database
        db.execute(f"""INSERT INTO Weather(Date, City, Source, Temperature, \
            TemperatureDay, TemperatureNight, Pressure, Ultraviolet,\
                 SunriseTime, SunsetTime, Humidity, WindSpeed)
    VALUES(\
        date('{data["Date"].strftime("%Y-%m-%d")}'),\
        '{data["City"]}',\
        '{data["WeatherSource"]}',\
        {data["Temperature"]},\
        {data["DayTemperature"]},\
        {data["NightTemperature"]},\
        {data["Pressure"]},\
        {data["UVIndex"]},\
        time('{data["SunriseTime"]}'),\
        time('{data["SunsetTime"]}'),\
        {data["Humidity"]},\
        {data["WindSpeed"]})""")
        # Commiting the changes
        db.commit()
        debug("Database modified")
        return True
    # Handling exceptions like 404
    except Exception as e:
        debug(f"Couldn't modify database: {e}")
        return False


def read(date: datetime.date) -> dict:
    """Returns database data as a formatted dict()
    :param date: PrimaryKey (Date)"""
    # Changing the date to the SQL format
    date = date.strftime("%Y-%m-%d")
    if date is None:
        return None
    global db
    result = dict()
    # Setting the row factory to get the dict
    db.row_factory = sqlite3.Row
    try:
        cur = db.cursor()
        # Getting the database row
        cur.execute(f"""SELECT * from Weather WHERE Date = date('{date}')""")
        result = cur.fetchone()  # Parsing the row into the dict
        return result
    except Exception as e:
        debug(f"Couldn't read database data: {e}")
        return None


def close() -> None:
    """Closes the database"""
    db.close()
