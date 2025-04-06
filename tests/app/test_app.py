import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add path to access app.py from root/app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app import app  # Import the Flask app instance


class TestFlaskApp(unittest.TestCase):
    """
    Full test suite for app.py including:
    - Page and API route status
    - Session-based routing
    - Firebase login simulation
    - API endpoints used by frontend
    """

    def setUp(self):
        # Set up test client before each test
        self.app = app.test_client()
        self.app.testing = True

    def test_home_redirects_to_login(self):
        # Unauthenticated access to "/" redirects to /login
        response = self.app.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_login_page_renders(self):
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_signup_page_renders(self):
        response = self.app.get("/signup")
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_login(self):
        with self.app.session_transaction() as sess:
            sess["user"] = "test-user"
        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login", response.data.lower())

    def test_dashboard_redirects_if_not_logged_in(self):
        response = self.app.get("/dashboard", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login", response.data.lower())

    @patch("app.fetch_bike_stations")
    def test_dashboard_renders_when_logged_in(self, mock_fetch):
        mock_fetch.return_value = [{"number": 1, "name": "Station A", "position": {"lat": 53.3, "lng": -6.2}}]
        with self.app.session_transaction() as sess:
            sess["user"] = "test-user"
            sess["first_name"] = "Test"

        response = self.app.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dublin Bikes", response.data)

    @patch("app.fetch_bike_stations")
    def test_api_bike_stations(self, mock_fetch):
        mock_fetch.return_value = [{"number": 1, "name": "Station A"}]
        response = self.app.get("/api/bike_stations")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"number": 1, "name": "Station A"}])

    @patch("app.fetch_weather_data")
    def test_api_weather(self, mock_fetch_weather):
        mock_fetch_weather.return_value = {"main": {"temp": 15}, "wind": {"speed": 5}, "weather": [{"main": "Clear"}]}
        response = self.app.get("/api/weather?lat=53.3&lon=-6.2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("main", response.get_json())

    def test_api_google_maps_key(self):
        response = self.app.get("/api/google-maps-key")
        self.assertEqual(response.status_code, 200)
        self.assertIn("apiKey", response.get_json())

    @patch("app.auth.verify_id_token")
    def test_verify_login_success(self, mock_verify):
        mock_verify.return_value = {"uid": "test-user"}
        response = self.app.post("/verify_login", json={"idToken": "fake-token"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["success"], True)

    def test_verify_login_missing_token(self):
        response = self.app.post("/verify_login", json={})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["success"], False)

    def test_api_history_data_missing_param(self):
        response = self.app.get("/api/history_data")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing station_id", response.get_data(as_text=True))

    def test_api_history_dates_missing_param(self):
        response = self.app.get("/api/history_dates")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing station_id", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
