
# Database Testing – JCDecaux & OpenWeather Integration

This document details the testing efforts specifically focused on the **database modules** inside the `app/database/` directory of the project.

Due to the suspension of the Amazon RDS instance,
the project now uses local file outputs to simulate and validate data ingestion logic. However, previous testing and files still remain in this repo and run when the Amazon RDS is turned on (left in repo for clarity and wholeness, only omitted due to cost).

---

## Test Types Performed

The following tests were designed to validate the core functionality of the database pipeline for both JCDecaux and OpenWeather integrations:

- **Mocking**:
  - `mock_open()` to intercept and verify local file writing
  - `MagicMock()` to simulate SQL connection calls
  - `patch()` to fake external API responses and keys

- **Assertions**:
  - `mock_file.assert_called()` ensures write was triggered
  - `handle.write.call_args_list` allows checking actual content
  - `mock_conn.execute.call_count` verifies row generation (even without DB)

---

## Targeted Modules

| Module                      | Description                                        |
|----------------------------|----------------------------------------------------|
| `JCDecaux_DB.py`           | Sets up `station` and `availability` tables       |
| `OpenWeather_DB.py`        | Sets up `current_weather` and `daily_forecast` tables   |
| `JCDecauxAPI_to_DB.py`     | Parses JCDecaux JSON data and inserts into tables |
| `OpenWeatherAPI_to_DB.py`  | Combines station + weather data for DB insertion  |

---

## Test Files & Purpose

Test code is located in the `/tests` directory (outside of `app/`). Each test file directly targets one of the modules above.

| Test File                      | What It Tests                                                            |
|-------------------------------|---------------------------------------------------------------------------|
| `test_jcdecaux_db.py`         | Ensures station and availability table creation statements execute       |
| `test_openweather_db.py`      | Verifies table creation for weather and forecast tables                  |
| `test_jcdecauxapi_to_db.py`   | Tests station insertion logic and always-insert availability logic       |
| `test_openweatherapi_to_db.py`| Tests integration of station and weather data with insert verification   |
| `test_jcdecauxapi_to_file.py`  | Validates transformation and local writing logic for station data       |
| `test_openweatherapi_to_file.py` | Verifies weather API response handling and record simulation            |

Each test mocks the SQLAlchemy `engine.connect()` call to prevent any live database interaction.

---

## How to Run the Tests

From the project root, to run Amazon RDS tests:

```bash
python3 -m unittest tests/test_jcdecaux_db.py
python3 -m unittest tests/test_openweather_db.py
python3 -m unittest tests/test_jcdecauxapi_to_db.py
python3 -m unittest tests/test_openweatherapi_to_db.py
```

From the project root, to run all tests applicable without RDS (recommended):

```bash
python3 -m unittest tests/test_jcdecauxapi_to_file.py
python3 -m unittest tests/test_openweatherapi_to_file.py
```

---

## Conclusion

The adapted database testing approach guarantees:
- The parsing logic is thoroughly validated
- Integration with local storage works in place of a live DB
- No loss of test coverage despite cloud service suspension

These tests are lightweight, mock-driven, and ready for continuous integration or future upgrade when the DB is restored.
