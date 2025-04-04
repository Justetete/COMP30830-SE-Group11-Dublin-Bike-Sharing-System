import unittest

# Import the test case for the Flask app
from app.test_app import TestFlaskApp

### we are instructed to suspend the RDS due to costs, however from talking to Alessio on discord and the TAs it was clear that we had our RDS running perfectly

# from database.test_jcdecaux_db import TestJCDecauxDB
# from database.test_openweather_db import TestOpenWeatherDB
# from database.test_jcdecauxapi_to_db import TestJCDecauxAPIToDB
# from database.test_openweatherapi_to_db import TestOpenWeatherAPIToDB

def suite():
    """
    Creates a test suite that aggregates individual test cases.
    """
    test_suite = unittest.TestSuite()

    # Add Flask app tests
    test_suite.addTest(unittest.makeSuite(TestFlaskApp))

    """ 
    Here I would include the test cases for the 'database' side of the project, however Prof. Ferrari has instructed that it is 'SUSPENDED' 
    Since these programs test the RDS database I cannot run them, however as from talking to Alessio on Discord, our RDS was working and all code was too prior to him stopping it
    """
    # test_suite.addTest(unittest.makeSuite(TestJCDecauxDB))
    # test_suite.addTest(unittest.makeSuite(TestOpenWeatherDB))
    # test_suite.addTest(unittest.makeSuite(TestJCDecauxAPIToDB))
    # test_suite.addTest(unittest.makeSuite(TestOpenWeatherAPIToDB))

    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
