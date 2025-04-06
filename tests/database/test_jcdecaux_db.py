import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Make the path to the app/database directory so we can import JCDecaux_DB.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'database')))

# Import the module under test
import JCDecaux_DB

class TestJCDecauxDB(unittest.TestCase):
    """
    Unit tests for the JCDecaux_DB.py module.
    These tests focus on verifying that SQL table creation statements
    are correctly executed using a mocked SQLAlchemy engine connection.
    """

    @patch("JCDecaux_DB.engine.connect")
    def test_create_station_table(self, mock_connect):
        """
        Test that the SQL for creating the 'station' table executes successfully.
        The database engine's connect method is mocked to avoid hitting a real DB.
        """
        # Create a mock connection object
        mock_conn = MagicMock()
        # Simulate the context manager behavior of engine.connect()
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Execute the 'station' table SQL creation statement using the mock connection
        JCDecaux_DB.station_sql.execute(mock_conn)

        # Verify that the execute method was called at least once
        mock_conn.execute.assert_called()

    @patch("JCDecaux_DB.engine.connect")
    def test_create_availability_table(self, mock_connect):
        """
        Test that the SQL for creating the 'availability' table executes successfully.
        Again, the connection is mocked to isolate the test from any real DB activity.
        """
        # Create a mock connection object
        mock_conn = MagicMock()
        # Simulate the context manager behavior of engine.connect()
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Execute the 'availability' table SQL creation statement using the mock connection
        JCDecaux_DB.availability_sql.execute(mock_conn)

        # Verify that the execute method was called at least once
        mock_conn.execute.assert_called()

if __name__ == "__main__":
    unittest.main()
