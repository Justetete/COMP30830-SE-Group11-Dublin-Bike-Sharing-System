from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

JCDECAUX_API_KEY = "1bee4dcd68c8e76a61647efcc43b3e68a55cacaf"
OPENWEATHER_API_KEY = "5361004f3b8168405f9c7f15918a4186"
CONTRACT = "dublin"  # Change to your city

#OPENWEATHER_API_KEY = "your_actual_openweather_api_key"
BIKE_API_URL = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=1bee4dcd68c8e76a61647efcc43b3e68a55cacaf"

@app.route("/")
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
