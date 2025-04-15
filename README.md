# Dublin Bike sharing Website Project - COMP30380 Software Engineering  
<img src="https://github.com/Justetete/COMP30830-SE-Group11-Dublin-Bike-Sharing-System/blob/main/app/static/imgs/logo2.png" width="20%">

## Table of Contents
- [Project Overview](#project-overview)
- [Group Members](#group-members)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Testing](#testing)

## Project Overview

This project is designed to provide a dynamic and interactive web application that displays real-time Dublin Bikes station occupancy information along with weather updates and predictive analytics. By integrating data from JCDecaux (DublinBikes) and OpenWeather APIs, the application provides users with a comprehensive view of bike station statuses and anticipated occupancy trends.

- [ ] add the architecture of the application

## Group Members

- Jian, Xinchi: [Github](https://github.com/Justetete)
- Kavanagh, Alex: [Github](https://github.com/AlexanderKav)
- Tully, Mark: [Github](https://github.com/mtully-64)

## Features

- **Dynamic Data Collection:**  
  - Collects live "DublinBikes" station occupancy data from the JCDecaux API.
  - Aggregates several days of continuous histroical data for robust analytics.

- **Weather Integration:**  
  - Retrieves weather data from the OpenWeather API on an hourly basis.
  - Displays current weather conditions and forecast for bike stations.

- **Data Management & Storage:**  
  - Stores collected data in a local MySQL database, previously an AWS RDS (code for this remains for wholeness of project).
  - Enables historical data analysis and machine learning model training.

- **Interactive Map Display:**  
  - Visualizes all Dublin Bikes stations using Google Maps API.
  - Each station is represented by a marker that can be clicked to reveal detailed station data.
  - Clicking on a station reveals detailed occupancy bar charts (hourly and daily) along with weather forecast data.

- **Predictive Analytics:**  
  - Implements a machine learning model to predict station occupancy based on historical data and weather patterns.
  - Regularly updates predictions as new data is collected.

- **Full-Stack Implementation:**  
  - Frontend developed using HTML, CSS, and JavaScript.
  - Backend API built with Python Flask, running on an EC2 instance.
  - Automated data scraping from EC2 to feed the local MySQL database.
 
- **protocol**
- [ ] add the wireframe for our website

- **Interface**
- [ ] add the main screenshot of the website

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask (API)
- **Database:** MySQL (local, but could be hosted on Amazon RDS)
- **Cloud Infrastructure:** AWS - EC2
- **APIs:** JCDecaux API for DublinBikes data, OpenWeather API for weather information, Firebase for Authentification
- **Mapping:** Google Maps API
- **Machine Learning:** Python libraries for training and predictions

## Project Structure

```
repo/
├── app/
│   ├── app.py                  # Flask entry point
│   ├── config.json             # App configuration
│   ├── dublin-bikes-bc821-firebase*.json                  # Firebase credentials
│   ├── templates/              # HTML templates
│   └── static/              # Frontend - JavaScript (auth, map, weather, etc.) & CSS
├── tests/
│   ├── app/                    # Flask app route/API tests
│   └── database/              # Unit tests for DB ingestion python files
├── docs/                       # Project documentation
└── README.md
```

## Installation and Setup

1. **Clone the Repository:**
  ```bash
  git clone https://github.com/Justetete/COMP30830-SE-Group11-Dublin-Bike-Sharing-System
  cd COMP30830-SE-Group11-Dublin-Bike-Sharing-System
  ```
    
2. **Setup Virtual Environment for Python**
- Navigate to the backend folder
- Create a virtual environment and install dependencies

```bash
cd app
python -m venv venv

# Activate the virtual environment

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r pip_comp30830_requirements.txt
```

3. **Running the Application**
  
```python
# Code to start that Flask App
python app.py
```

- Open `http://127.0.0.1:5000` in your browser.

## Usage
- Interactive Map:
Navigate to the main page to see all Dublin Bike stations displayed on a Google Map. Selecting specific markers indicate the current bike occupancy and availability.

- Station Details:
Click on a station marker to view detailed occupancy data (hourly and daily) and the local weather forecast.

- Predictive Analytics:
Access the predictions section to see forecasted station occupancy based on the trained machine learning model.

## Testing

### Test Structure
- `tests/database/`: Unit tests for data ingestion scripts (with SQLAlchemy mocking)
- `tests/app/`: Flask app route/API tests using `unittest` and `test_client`
- `tests/test_suite.py`: Central test runner for combining all test cases

### Run All Tests
```bash
python -m tests.test_suite
```

---

## Code Coverage

To measure test coverage:

```bash
coverage run -m unittest tests.test_suite
coverage report -m
```

### Coverage Report

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app\app.py                108     25    77%   47, 75-95, 103-110, 166-167, 182-183, 190, 194
tests\app\test_app.py     75      1    99%   106
tests\test_suite.py        10      6    40%   17-31, 34-35
-----------------------------------------------------
TOTAL                     193     32    83%
```

Database-related code connected to the RDS is excluded from this run, as database tests are currently commented out in the suite. This is done under Alessio's instruction to stop the AWS RDS, however the code still remains in the GitHub repo and works (once you start the AWS RDS). Instead to still provide testing under 'databases' I have included testing for parsing API data correctly and writing the expected contents to local database

---

This application demonstrates a robust full-stack system integrating live transport data, external weather forecasting, and real-time visual analytics with cloud-based infrastructure.
