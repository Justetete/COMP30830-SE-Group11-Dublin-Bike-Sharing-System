from flask import Flask, render_template, json

import random, requests, json

app = Flask(__name__)




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
def home():
    return render_template('index.html', title="Dublin Bikes", stations=bike_station, temp=temp, wind_speed=wind_speed, weather_main=weather_main)

if __name__ == '__main__':
    app.run(debug=True)


