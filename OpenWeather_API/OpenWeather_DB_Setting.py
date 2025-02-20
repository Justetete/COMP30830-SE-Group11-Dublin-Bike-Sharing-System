from sqlalchemy import create_engine, text
import OpenWeather_DB_info

# Load credentials
USER = OpenWeather_DB_info.USER
PASSWORD = OpenWeather_DB_info.PASSWORD
PORT = OpenWeather_DB_info.PORT
DB = OpenWeather_DB_info.DB
URI = OpenWeather_DB_info.URI

# Use PyMySQL 
connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/"
engine = create_engine(connection_string, echo=True)

# MySQL command to create the 'cuttent' table
current_sql = text("""
CREATE TABLE IF NOT EXISTS current (
    dt DATETIME NOT NULL,
    feels_like FLOAT,
    humidity INTEGER,
    pressure INTEGER,
    sunrise DATETIME,
    sunset DATETIME,
    `temp` FLOAT,
    uvi FLOAT,
    weather_id INTEGER,
    wind_gust FLOAT,
    wind_speed FLOAT,
    rain_1h FLOAT,
    snow_1h FLOAT,
    PRIMARY KEY (dt)   
)
""")

# MySQL command to create the 'daily' table
# delete domain future_dt DATETIME NOT NULL
daily_sql = text("""
CREATE TABLE IF NOT EXISTS daily (
    dt DATETIME NOT NULL,
    humidity INTEGER,
    pop FLOAT,
    pressure INTEGER,
    temp_max FLOAT,
    temp_min FLOAT,
    uvi FLOAT,
    weather_id INTEGER,
    wind_speed FLOAT,
    wind_gust FLOAT,
    rain FLOAT,
    snow FLOAT,
    PRIMARY KEY (dt)
)
""")

# MySQL command to create the 'hourly' table
# delete domain future_dt DATETIME NOT NULL
hourly_sql = text("""
CREATE TABLE IF NOT EXISTS hourly (
    dt DATETIME NOT NULL,   
    feels_like FLOAT,
    humidity INTEGER,
    pop FLOAT,
    pressure INTEGER,
    `temp` FLOAT,
    uvi FLOAT,
    weather_id INTEGER,
    wind_speed FLOAT,
    wind_gust FLOAT,
    rain_1h FLOAT,
    snow_1h FLOAT,
    PRIMARY KEY (dt)
)
""")

try:
    with engine.connect() as connection:
        print("Successfully connected!")

        # Create the database if it doesn't exist
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB}`;"))
        print(f"Database `{DB}` created or already exists.")
    
    # Update connection string to include the database
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True)

    with engine.connect() as connection:
        # Show all database variables
        result = connection.execute(text("SHOW VARIABLES;"))
        print("\nMySQL Variables:")
        for row in result:
            print(row)
except Exception as e:
    print("Connection failed:", e)

# Ensure 'current' table is created
try:
    with engine.connect() as connection:
        connection.execute(current_sql)
        print("'current' table created successfully.")
except Exception as e:
    print("Error creating 'current' table:", e)

# Ensure 'daily' table is created
try:
    with engine.connect() as connection:
        connection.execute(daily_sql)
        print("'daily' table created successfully.")
except Exception as e:
    print("Error creating 'daily' table:", e)

# Ensure 'hourly' table is created
try:
    with engine.connect() as connection:
        connection.execute(hourly_sql)
        print("'hourly' table created successfully.")
except Exception as e:
    print("Error creating 'hourly' table:", e)
