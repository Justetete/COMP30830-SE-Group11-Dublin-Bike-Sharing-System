import json
import traceback
import sqlalchemy
from sqlalchemy import create_engine, text as sql_text
import OpenWeather_DB_info
from datetime import datetime
import os

def load_weather_data(file_path):
    """Load weather data from a given file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

# Load database credentials
USER = OpenWeather_DB_info.USER
PASSWORD = OpenWeather_DB_info.PASSWORD
PORT = OpenWeather_DB_info.PORT
DB = OpenWeather_DB_info.DB
URI = OpenWeather_DB_info.URI

connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"
engine = create_engine(connection_string, echo=True)

# Define data folders
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDERS = {
    "current": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Current"),
    "daily": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Daily"),
    "hourly": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Hourly"),
}

def insert_current_weather(data, engine):
    """Insert current weather data into the database"""
    try:
        dt = datetime.fromtimestamp(data.get("dt", 0)).strftime('%Y-%m-%d %H:%M:%S')
        values = {
            "dt": dt,
            "feels_like": data.get("feels_like"),
            "humidity": data.get("humidity"),
            "pressure": data.get("pressure"),
            "sunrise": datetime.fromtimestamp(data.get("sunrise", 0)).strftime('%Y-%m-%d %H:%M:%S'),
            "sunset": datetime.fromtimestamp(data.get("sunset", 0)).strftime('%Y-%m-%d %H:%M:%S'),
            "temp": data.get("temp"),
            "uvi": data.get("uvi"),
            "weather_id": data.get("weather", [{}])[0].get("id"),
            "wind_speed": data.get("wind_speed"),
            "wind_gust": data.get("wind_gust", 0),
            "rain_1h": data.get("rain", {}).get("1h", 0),
            "snow_1h": data.get("snow", {}).get("1h", 0)
        }
        query = sql_text("""
            INSERT INTO current (dt, feels_like, humidity, pressure, sunrise, sunset, temp, uvi, weather_id, wind_speed, wind_gust, rain_1h, snow_1h)
            VALUES (:dt, :feels_like, :humidity, :pressure, :sunrise, :sunset, :temp, :uvi, :weather_id, :wind_speed, :wind_gust, :rain_1h, :snow_1h)
            ON DUPLICATE KEY UPDATE temp=VALUES(temp)
        """)
        with engine.connect() as conn:
            conn.execute(query, values)
            conn.commit()
        print(f"Inserted current weather data at {dt}")
    except Exception as e:
        print("Error inserting current weather data:", e)
        print(traceback.format_exc())

def insert_hourly_weather(data, engine):
    """Insert hourly weather data into the database"""
    try:
        with engine.connect() as conn:
            for hour in data:
                dt = datetime.fromtimestamp(hour["dt"]).strftime('%Y-%m-%d %H:%M:%S')
                values = {
                    "dt": dt,
                    "temp": hour.get("temp"),
                    "humidity": hour.get("humidity"),
                    "pressure": hour.get("pressure"),
                    "wind_speed": hour.get("wind_speed"),
                    "weather_id": hour.get("weather", [{}])[0].get("id")
                }
                query = sql_text("""
                    INSERT INTO hourly (dt, temp, humidity, pressure, wind_speed, weather_id)
                    VALUES (:dt, :temp, :humidity, :pressure, :wind_speed, :weather_id)
                    ON DUPLICATE KEY UPDATE temp=VALUES(temp)
                """)
                conn.execute(query, values)
            conn.commit()
        print("Inserted hourly weather data.")
    except Exception as e:
        print("Error inserting hourly weather data:", e)
        print(traceback.format_exc())

def insert_daily_weather(data, engine):
    """Insert daily weather data into the database"""
    try:
        with engine.connect() as conn:
            for day in data:
                dt = datetime.fromtimestamp(day["dt"]).strftime('%Y-%m-%d %H:%M:%S')
                values = {
                    "dt": dt,
                    "temp_max": day.get("temp", {}).get("max"),
                    "temp_min": day.get("temp", {}).get("min"),
                    "humidity": day.get("humidity"),
                    "pressure": day.get("pressure"),
                    "wind_speed": day.get("wind_speed"),
                    "weather_id": day.get("weather", [{}])[0].get("id")
                }
                query = sql_text("""
                    INSERT INTO daily (dt, temp_max, temp_min, humidity, pressure, wind_speed, weather_id)
                    VALUES (:dt, :temp_max, :temp_min, :humidity, :pressure, :wind_speed, :weather_id)
                    ON DUPLICATE KEY UPDATE temp_max=VALUES(temp_max)
                """)
                conn.execute(query, values)
            conn.commit()
        print("Inserted daily weather data.")
    except Exception as e:
        print("Error inserting daily weather data:", e)
        print(traceback.format_exc())

def main():
    """Main function to read stored weather data and insert it into the database"""
    for category, folder in FOLDERS.items():
        files = sorted(os.listdir(folder), reverse=True)
        if files:
            latest_file = os.path.join(folder, files[0])
            weather_data = load_weather_data(latest_file)
            if weather_data:
                if category == "current":
                    insert_current_weather(weather_data, engine)
                elif category == "hourly":
                    insert_hourly_weather(weather_data, engine)
                elif category == "daily":
                    insert_daily_weather(weather_data, engine)

if __name__ == "__main__":
    main()