from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import json
import requests
import firebase_admin
import os
from firebase_admin import credentials, auth

app = Flask(__name__)
#app.secret_key = "your_secret_key" 
app.secret_key = os.urandom(24)  # Required for session management


# Load API keys
with open("config.json") as config_file:
    config = json.load(config_file)

JCDECAUX_API_KEY = config["JCDECAUX_API_KEY"]
OPENWEATHER_API_KEY = config["OPENWEATHER_API_KEY"]
GOOGLE_MAPS_API_KEY = config["GOOGLE_MAPS_API_KEY"]

# City contract name for JCDecaux bike-sharing API
CONTRACT = "dublin"

# API URL for fetching bike station data in Dublin
BIKE_API_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={JCDECAUX_API_KEY}"

#BIKE_API_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={JCDECAUX_API_KEY}"

# Initialize Firebase Admin SDK
cred = credentials.Certificate("dublin-bikes-bc821-firebase-adminsdk-fbsvc-6b3b526527.json")  # Replace with your Firebase service account key
firebase_admin.initialize_app(cred)

@app.route("/")
def home():
    """
    Renders the homepage with bike station data.

    This function fetches bike station data from JCDecaux's API and passes it 
    to the `index.html` template for rendering.

    Returns:
        Rendered HTML template with bike station data.
    """
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # Restrict access if not logged in

    first_name = session.get("first_name", "User")  # Get first name from session
    #session["first_name"] = first_name
    bike_stations = requests.get(BIKE_API_URL).json()  # Fetch bike station data
    return render_template("index.html", title="Dublin Bikes", stations=bike_stations, google_maps_api_key=GOOGLE_MAPS_API_KEY, first_name=first_name)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove the user from session
    return redirect(url_for("login"))

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


@app.route("/api/google-maps-key")
def get_google_maps_key():
    """
    Securely fetch the Google Maps API key from the server.
    The frontend can request this endpoint instead of hardcoding the key.
    """
    return jsonify({"apiKey": GOOGLE_MAPS_API_KEY})


@app.route("/verify_login", methods=["POST"])
def verify_login():
    try:
        data = request.json
        id_token = data.get("idToken")

        if not id_token:
            return jsonify({"success": False, "error": "Missing token"}), 401

        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]

        # ✅ Store session
        session["user"] = user_id  

        return jsonify({"success": True, "user_id": user_id})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401

    
@app.route("/signup")
def signup():
    return render_template("sign-up.html")  # This serves the signup.html file


if __name__ == "__main__":
    app.run(debug=True)


