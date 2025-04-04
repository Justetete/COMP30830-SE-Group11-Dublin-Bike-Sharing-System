
# Testing Suite Summary

This document provides a combined overview of the test suite implemented for the Dublin Bike Sharing System, covering both the backend Flask application and the database ingestion logic.

---

## Overview

The project includes a unified test suite that brings together:
- **Application-level tests** for Flask routes, APIs, and authentication
- **Database module tests** for table creation and data insertion logic

The test suite is organized under the `tests/` directory, with each module structured to reflect its purpose. Tests are implemented using Python's built-in `unittest` framework, with extensive use of mocking (`unittest.mock`) to isolate functionality and avoid dependence on live services or a real database.

---

## Test Structure

```
tests/
├── app/
│   └── test_app.py              # Flask app and API endpoint tests
├── database/
│   ├── test_jcdecaux_db.py
│   ├── test_openweather_db.py
│   ├── test_jcdecauxapi_to_db.py
│   └── test_openweatherapi_to_db.py
└── test_suite.py                # Aggregates test cases into one suite
```

---

## Included Test Types

### Flask App Tests (test_app.py)
- Routing and session redirect behavior
- API responses: `/api/bike_stations`, `/api/weather`, `/api/google-maps-key`, etc.
- Authentication handling with Firebase (mocked)
- Login, logout, and dashboard access flow

### Database Tests (test_*.py)
- SQL table creation for stations, availability, weather, and forecast
- Insertion logic for data coming from JCDecaux and OpenWeather APIs
- All database connections and executions are mocked for test reliability

---

## Running the Suite

The test suite is bundled into `tests/test_suite.py`. Run from the project root:

```bash
python -m tests.test_suite
```

This will run:
- All Flask app tests (enabled by default)
- Database tests (currently commented out, can be enabled easily)

---

## Coverage

Coverage is tracked using `coverage.py`:

```bash
coverage run -m unittest tests.test_suite
coverage report -m
```

Example output:

```
Name                    Stmts   Miss  Cover
---------------------------------------------
app/app.py                108     25    77%
tests/app/test_app.py      75      1    99%
tests/test_suite.py        10      6    40%
TOTAL                     193     32    83%
```

> Note: Database modules are excluded unless uncommented in the suite. Under the instruction of Alessio suspending AWS RDS

---

## Conclusion

This combined test suite ensures robust coverage of both the backend API and the critical data ingestion logic. By keeping the test modules modular and mock-driven, the application remains testable, scalable, and maintainable.
