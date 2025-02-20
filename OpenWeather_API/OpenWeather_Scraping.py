import requests
import json
import os
import datetime
import time
import traceback
import OpenWeather_API_info  # Import API information from separate file

# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDERS = {
    "current": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Current"),
    "daily": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Daily"),
    "hourly": os.path.join(SCRIPT_DIR, "OpenWeather_Data/Hourly"),
}

# Ensure the data folders exist
for folder in FOLDERS.values():
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Folder '{folder}' Created!")
    else:
        print(f"Folder '{folder}' Already Exists.")

def write_to_txtfile(data, category):
    """Save the retrieved data to a corresponding folder"""
    if category not in FOLDERS:
        print(f"Invalid category: {category}")
        return
    
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(FOLDERS[category], f"{category}_weather_{now}.txt")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def fetch_weather_data():
    """Fetch weather data from OpenWeather API"""
    params = {
        "lat": OpenWeather_API_info.LAT,
        "lon": OpenWeather_API_info.LON,
        "appid": OpenWeather_API_info.API_KEY,
        "units": "metric",
        "exclude": "minutely"  # Excluding minutely data
    }
    try:
        response = requests.get(OpenWeather_API_info.BASE_URL, params=params)
        print(response)
        if response.status_code == 200:
            weather_data = response.json()
            
            # Store different types of weather data in respective folders
            write_to_txtfile(weather_data.get("current", {}), "current")
            write_to_txtfile(weather_data.get("daily", {}), "daily")
            write_to_txtfile(weather_data.get("hourly", {}), "hourly")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(f"Response content: {response.text}")  # Print detailed error message
    except:
        print(traceback.format_exc())

def main():
    """Fetch weather data every hour"""
    while True:
        fetch_weather_data()
        time.sleep(60 * 60)  # Sleep for 1 hour

if __name__ == "__main__":
    main()
