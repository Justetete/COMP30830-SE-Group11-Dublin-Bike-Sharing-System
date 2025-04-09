
# Testing Suite Summary

This document provides a combined overview of the test suite implemented for the Dublin Bike Sharing System, covering the backend Flask application, database ingestion logic, and machine learning predictions.

---

## Overview

The project includes a unified test suite that brings together:
- **Application-level tests** for Flask routes, APIs, and authentication
- **Database module tests** for data insertion logic from local file-based simulations instead of RDS access
- **Machine Learning model tests** for prediction accuracy and model loading

The test suite is organized under the `tests/` directory, with each module structured to reflect its purpose. Tests are implemented using Python's built-in `unittest` framework, with extensive use of mocking (`unittest.mock`) to isolate functionality and avoid dependence on live services or a real database.

---

## Test Structure

```
tests/
├── app/
│   └── test_app.py                         # Flask app and API endpoint tests
├── database/
│   ├── test_jcdecaux_db.py                # Excluded due to RDS Suspension
│   ├── test_openweather_db.py             # Excluded due to RDS Suspension
│   ├── test_jcdecauxapi_to_db.py          # Excluded due to RDS Suspension
│   ├── test_openweatherapi_to_db.py       # Excluded due to RDS Suspension
│   ├── test_jcdecauxapi_to_file.py        # File-based JCDecaux transformation logic test
│   └── test_openweatherapi_to_file.py     # File-based weather transformation logic test
├── machine_learning/
│   └── test_prediction.py                 # ML model loading and prediction tests
└── test_suite.py                          # Aggregates test cases into one suite
```

> Database tests previously targeting RDS (`test_jcdecaux_db.py`, etc.) are now commented out under instruction to suspend AWS resources.

---

## Included Test Types

### Flask App Tests (test_app.py)
- Routing and session redirect behavior
- API responses: `/api/bike_stations`, `/api/weather`, `/api/google-maps-key`, etc.
- Authentication handling with Firebase (mocked)
- Login, logout, and dashboard access flow

### File-Based Database Logic Tests
- **JCDecaux Transformation Test**: Verifies station/availability parsing and file output logic
- **OpenWeather Transformation Test**: Confirms weather forecast handling, structure parsing, and simulated insertions
- Mocks the file I/O and API response structures for reliability without external calls

### Machine Learning Model Tests
- Validates that the model file (`Dubike_random_forest_model.joblib`) loads correctly
- Ensures the model produces a numeric output given valid feature input
- Checks proper handling of invalid input dimensions
- Simulates prediction logic as used in API routes

---

## Running the Suite

The test suite is bundled into `tests/test_suite.py`. Run from the project root:

```bash
python -m tests.test_suite
```

This will run:
- All Flask app tests (enabled by default)
- File-based database logic tests (enabled)
- ML prediction tests
- Commented-out RDS tests (available if re-enabled)

---

## Coverage

Coverage is tracked using `coverage.py`:

```bash
coverage run -m unittest tests.test_suite
coverage report -m
```

Example output:

```
Name                                      Stmts   Miss  Cover
--------------------------------------------------------------
app/app.py                                  108     25    77%
tests/app/test_app.py                        75      1    99%
tests/database/test_jcdecauxapi_to_file.py   35      0   100%
tests/database/test_openweatherapi_to_file.py36      0   100%
tests/machine_learning/test_prediction.py    28      0   100%
tests/test_suite.py                          14      0   100%
--------------------------------------------------------------
TOTAL                                       296     26    91%
```

> Note: Database modules interacting with RDS are excluded unless uncommented in the suite.

---

## Conclusion

This modular test suite ensures comprehensive test coverage across the backend, machine learning model, and data handling logic. With the switch to local file mocking and use of model testing, the project remains robust, testable, and AWS-independent while maintaining production-level logic readiness.
