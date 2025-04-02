
# Database Testing – JCDecaux & OpenWeather Integration

This document details the testing efforts specifically focused on the **database modules** inside the `app/database/` directory of the project.

---

## Test Types Performed

The following tests were designed to validate the core functionality of the database pipeline for both JCDecaux and OpenWeather integrations:

- **Unit Testing** of database schema creation logic.
- **Mocking** of SQLAlchemy engine and connections to simulate DB interactions.
- **Insert Logic Testing** to ensure correct handling of station and weather data.

All database tests were implemented using Python’s built-in `unittest` framework and `unittest.mock`, as shown in week 10 lectures.

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

Each test mocks the SQLAlchemy `engine.connect()` call to prevent any live database interaction.

---

## How to Run the Tests

From the project root:

```bash
python3 -m unittest tests/test_jcdecaux_db.py
python3 -m unittest tests/test_openweather_db.py
python3 -m unittest tests/test_jcdecauxapi_to_db.py
python3 -m unittest tests/test_openweatherapi_to_db.py
```

---

## Results Summary

- **All database tests passed**
- **Repeatable**: Fully mocked and safe to run without a real MySQL server
- No external dependencies required for running the tests

---

## Conclusion

Testing for the database logic ensures:
- Tables are created as expected
- Station and weather records are correctly processed and inserted
- Mocking provides reliability and speed for validation

These tests contribute significantly to the robustness and maintainability of the data ingestion pipeline.
