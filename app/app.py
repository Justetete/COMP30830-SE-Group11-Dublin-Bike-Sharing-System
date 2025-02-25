from flask import Flask, render_template, json

import random, requests

app = Flask(__name__)



# Load JSON data from the .txt file
bike_path = 'bikes_2025-02-24_16-12-33.txt' 
#weather_path = 'current_weather_2025-02-24_15-17-44.txt'
weather_data = 'current_weather_2025-02-24_15-17-44.txt'

with open(weather_data, 'r') as file:
    weather_data = json.load(file)  # Parse the JSON content


with open(bike_path, 'r') as file:
    bike_stations = json.load(file)  # Parse the JSON content

bike_station = random.choice(bike_stations)

temp = weather_data["temp"]
wind_speed = weather_data["wind_speed"]
weather_main = weather_data["weather"][0]["main"]
@app.route('/')
def home():
    return render_template('index.html', title="Dublin Bikes", stations=bike_station, temp=temp, wind_speed=wind_speed, weather_main=weather_main)

if __name__ == '__main__':
    app.run(debug=True)
