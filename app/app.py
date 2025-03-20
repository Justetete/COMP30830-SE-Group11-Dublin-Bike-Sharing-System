from flask import Flask, render_template, jsonify, request
import json
import requests  # Used to fetch data from external APIs

app = Flask(__name__)  # Create a Flask web application instance

# ============================== #
#         API CONFIGURATION      #


# API keys for JCDecaux (bike station data) and OpenWeather (weather data)
#JCDECAUX_API_KEY = "1bee4dcd68c8e76a61647efcc43b3e68a55cacaf"
#OPENWEATHER_API_KEY = "5361004f3b8168405f9c7f15918a4186"


with open("config.json") as config_file:
    config = json.load(config_file)



JCDECAUX_API_KEY = config["JCDECAUX_API_KEY"]
OPENWEATHER_API_KEY = config["OPENWEATHER_API_KEY"]
GOOGLE_MAPS_API_KEY = config["GOOGLE_MAPS_API_KEY"]

# City contract name for JCDecaux bike-sharing API
CONTRACT = "dublin"

# API URL for fetching bike station data in Dublin
BIKE_API_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={JCDECAUX_API_KEY}"

# ============================== #

# ============================== #
#           ROUTES               #


@app.route('/')
def home():
    """
    Renders the homepage with bike station data.

    This function fetches bike station data from JCDecaux's API and passes it 
    to the `index.html` template for rendering.

    Returns:
        Rendered HTML template with bike station data.
    """
    # Fetch bike station data from the JCDecaux API
    bike_stations = requests.get(BIKE_API_URL).json()

    # Render the homepage template and pass the station data to it
    return render_template("index.html", title="Dublin Bikes", stations=bike_stations, google_maps_api_key=GOOGLE_MAPS_API_KEY)


@app.route("/api/weather")
def get_weather():
    """
    Fetches weather data for a given latitude and longitude.

    This function extracts latitude and longitude from request parameters 
    and queries the OpenWeather API for real-time weather conditions.

    Returns:
        JSON response containing weather data.
    """
    lat = request.args.get("lat")  # Extract latitude from request
    lon = request.args.get("lon")  # Extract longitude from request

    # Construct the OpenWeather API URL with parameters
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"

    # Fetch weather data from the OpenWeather API
    weather_data = requests.get(weather_url).json()

    # Return weather data as a JSON response
    return jsonify(weather_data)


@app.route("/api/bike_stations")
def get_bike_stations():
    """
    Fetches real-time bike station data for Dublin.

    This function requests data from the JCDecaux API and returns a JSON response.

    Returns:
        JSON response containing bike station data.
    """
    # Fetch bike station data from JCDecaux API
    bike_stations = requests.get(BIKE_API_URL).json()

    # Return bike station data as a JSON response
    return jsonify(bike_stations)

# ============================== #


# ============================== #
#       APPLICATION START        #

if __name__ == "__main__":
    """
    Runs the Flask application in debug mode.

    Debug mode allows for automatic reloading during development and better error messages.
    """
    app.run(debug=True)


# ============================== #

