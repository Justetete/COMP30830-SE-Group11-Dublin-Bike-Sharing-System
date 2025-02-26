<<<<<<< HEAD
from flask import Flask, render_template, jsonify, request
import requests
=======
from flask import Flask, render_template, json

import random, requests, json
>>>>>>> origin/main

app = Flask(__name__)

JCDECAUX_API_KEY = "1bee4dcd68c8e76a61647efcc43b3e68a55cacaf"
OPENWEATHER_API_KEY = "5361004f3b8168405f9c7f15918a4186"
CONTRACT = "dublin"  # Change to your city

#OPENWEATHER_API_KEY = "your_actual_openweather_api_key"
BIKE_API_URL = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=1bee4dcd68c8e76a61647efcc43b3e68a55cacaf"

<<<<<<< HEAD
@app.route("/")
=======

# Load JSON data from the .txt file
bike_path = 'bikes_2025-02-24_16-12-33.txt' 

with open(bike_path, 'r') as file:
    bike_stations = json.load(file)  # Parse the JSON content

bike_station = random.choice(bike_stations)


# OpenWeather API endpoint
API_KEY = "5361004f3b8168405f9c7f15918a4186"
LAT = bike_station['position']["lat"]  
LON = bike_station['position']["lng"]  
UNITS = "Fahrenheit"  # Use "imperial" for Fahrenheit

url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units={UNITS}"


response = requests.get(url)
if response.status_code == 200:
    weather_data = response.json()
    print(json.dumps(weather_data, indent=4))  # Pretty print the JSON data
else:
    print(f"Error: Unable to fetch weather data. Status code {response.status_code}")

temp = weather_data["main"]["temp"]
wind_speed = weather_data["wind"]["speed"]
weather_main = weather_data["weather"][0]["main"]
@app.route('/')
>>>>>>> origin/main
def home():
    bike_stations = requests.get(BIKE_API_URL).json()
    return render_template("index.html", title="Dublin Bikes", stations=bike_stations)

@app.route("/api/weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()
    return jsonify(weather_data)

@app.route("/api/bike_stations")
def get_bike_stations():
    bike_stations = requests.get(BIKE_API_URL).json()
    return jsonify(bike_stations)

if __name__ == "__main__":
    app.run(debug=True)


