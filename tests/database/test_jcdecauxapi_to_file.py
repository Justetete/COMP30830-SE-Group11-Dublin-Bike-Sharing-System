import sys
import os
import unittest
from unittest.mock import mock_open, patch

# Add the database module to the path so we can import from app/database/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'database')))

from JCDecauxAPI_to_DB import stations_to_db  # Import the target function


class TestJCDecauxToFile(unittest.TestCase):
    """
    This test case verifies that the stations_to_db function correctly
    handles JSON input and writes it to a local file, simulating the
    expected behavior when database access is disabled.
    """

    def setUp(self):
        """
        Sample JCDecaux JSON payload used for testing.
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

    @patch("builtins.open", new_callable=mock_open)
    def test_writes_data_to_file(self, mock_file):
        """
        Test that verifies the stations_to_db function attempts to write the parsed
        station data to a file. This assumes the function has been refactored to
        support file output rather than live database writing.
        """
        mock_engine = None  # Simulate that no DB connection is passed
        stations_to_db(self.sample_data, mock_engine)

        # Ensure that open() was called — indicating a file write was attempted
        mock_file.assert_called()

        # Verify that data was written to the file handle
        handle = mock_file()
        self.assertTrue(handle.write.called)

        # Combine all write calls and check that the expected station name appears
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        self.assertIn("Station 42", written_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
