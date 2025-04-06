import sys
import os
import unittest
from unittest.mock import MagicMock

# Make the path to the app/database directory so we can import JCDecauxAPI_to_DB.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'database')))

# Import the function to be tested from the JCDecauxAPI_to_DB
from JCDecauxAPI_to_DB import stations_to_db

class TestJCDecauxAPIToDB(unittest.TestCase):
    """
    Unit tests for the JCDecauxAPI_to_DB.py module.
    These tests verify that station and availability data is processed
    and inserted into the database correctly when passed as JSON.
    """

    def setUp(self):
        """
        Prepare sample JSON data to simulate a response from the JCDecaux API.
        This data includes a single station entry with all required fields.
        """
        self.sample_data = '''
        [
            {
                "number": 42,
                "address": "Test Street",
                "banking": true,
                "bike_stands": 20,
                "name": "Station 42",
                "status": "OPEN",
                "position": {"lat": 53.3, "lng": -6.2},
                "available_bikes": 10,
                "available_bike_stands": 10,
                "last_update": 1700000000000
            }
        ]
        '''

    def test_station_and_availability_insert(self):
        """
        Test that the station is inserted when it doesn't already exist,
        and that availability data is always inserted.
        Uses MagicMock to simulate the SQLAlchemy engine and connection.
        """
        # Create a mock SQLAlchemy engine and connection object
        mock_engine = MagicMock()
        mock_conn = MagicMock()

        # Simulate a database connection context
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        # Simulate that the station does not yet exist (SELECT COUNT(*) returns 0)
        mock_conn.execute.return_value.scalar.return_value = 0

        # Call the function being tested
        stations_to_db(self.sample_data, mock_engine)

        # Check that SQL execution was triggered
        self.assertTrue(mock_conn.execute.called, "Expected SQL execution was not triggered.")

        # Verify that at least two SQL commands were executed:
        # one for inserting the station, one for inserting availability
        self.assertGreaterEqual(
            mock_conn.execute.call_count, 2,
            "Expected at least 2 SQL executions (station + availability insert)."
        )

if __name__ == "__main__":
    unittest.main()
