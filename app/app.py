# Import modules utilised in app
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import json
import requests
import firebase_admin
import os
from firebase_admin import credentials, auth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Load API keys from configuration file, 'config.json'
def load_config():
    with open("config.json") as config_file:
        return json.load(config_file)

config = load_config()
JCDECAUX_API_KEY = config["JCDECAUX_API_KEY"]
OPENWEATHER_API_KEY = config["OPENWEATHER_API_KEY"]
GOOGLE_MAPS_API_KEY = config["GOOGLE_MAPS_API_KEY"]

# City contract name for JCDecaux bike-sharing API
CONTRACT = "dublin"
# API URL for fetching bike station data in Dublin
BIKE_API_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={JCDECAUX_API_KEY}"

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate("dublin-bikes-bc821-firebase-adminsdk-fbsvc-6b3b526527.json")
    firebase_admin.initialize_app(cred)

initialize_firebase()

#### Routes ####

@app.route("/")
def home():
    """
    Redirect users based on authentication status.
    """
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    """
    Display dashboard with bike station data.
    """
    if "user" not in session:
        return redirect(url_for("login"))
    
    first_name = session.get("first_name", "User")
    bike_stations = fetch_bike_stations()
    return render_template("index.html", title="Dublin Bikes", stations=bike_stations, google_maps_api_key=GOOGLE_MAPS_API_KEY, first_name=first_name)

@app.route("/login")
def login():
    """
    Render login page.
    """
    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Logout user by removing session data.
    """
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/api/weather")
def get_weather():
    """
    Fetch real-time weather data from OpenWeather API.
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    return jsonify(fetch_weather_data(lat, lon))

@app.route("/api/bike_stations")
def get_bike_stations():
    """
    Fetch real-time bike station data for Dublin.
    """
    return jsonify(fetch_bike_stations())

@app.route("/api/google-maps-key")
def get_google_maps_key():
    """
    Securely return the Google Maps API key.
    """
    return jsonify({"apiKey": GOOGLE_MAPS_API_KEY})

@app.route("/verify_login", methods=["POST"])
def verify_login():
    """
    Verify user login with Firebase authentication.
    """
    try:
        data = request.json
        id_token = data.get("idToken")
        if not id_token:
            return jsonify({"success": False, "error": "Missing token"}), 401
        
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]
        session["user"] = user_id  # Store session

        return jsonify({"success": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401

@app.route("/signup")
def signup():
    """
    Render the sign-up page.
    """
    return render_template("sign-up.html")

### Helper Functions ###

def fetch_weather_data(lat, lon):
    """
    Fetch weather data for given latitude and longitude.
    """
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    return requests.get(weather_url).json()


def fetch_bike_stations():
    """
    Fetch bike station data from JCDecaux API.
    """
    return requests.get(BIKE_API_URL).json()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
