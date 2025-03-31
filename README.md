# Dublin Bike sharing Website Project - COMP30380 Software Engineering 
![image](https://github.com/Justetete/COMP30830-SE-Group11-Dublin-Bike-Sharing-System/blob/main/app/static/imgs/logo2.png)

## Table of Contents
- [Project Overview](#project-overview)
- [Group Members](#group-members)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)

## Project Overview

This project is designed to provide a dynamic and interactive web application that displays real-time Dublin Bikes station occupancy information along with weather updates and predictive analytics. By integrating data from JCDecaux (DublinBikes) and OpenWeather APIs, the application provides users with a comprehensive view of bike station statuses and anticipated occupancy trends.

## Group Members

- Jian, Xinchi
- Kavanagh, Alex
- Tully, Mark

## Features

- **Dynamic Data Collection:**  
  - Collects live "DublinBikes" station occupancy data from the JCDecaux API every 5 minutes.
  - Aggregates several weeks of continuous data for robust analytics.

- **Weather Integration:**  
  - Retrieves weather data from the OpenWeather API on an hourly basis.
  - Displays current weather conditions and forecast for bike stations.

- **Data Management & Storage:**  
  - Stores collected data in an Amazon RDS (MySQL) database.
  - Enables historical data analysis and machine learning model training.

- **Interactive Map Display:**  
  - Uses Google Maps to visualize bike stations.
  - Marker colors and sizes encode real-time occupancy and availability.
  - Clicking on a station reveals detailed occupancy bar charts (hourly and daily) along with weather forecast data.

- **Predictive Analytics:**  
  - Implements a machine learning model to predict station occupancy based on historical data and weather patterns.
  - Regularly updates predictions as new data is collected.

- **Full-Stack Implementation:**  
  - Frontend developed using HTML, CSS, and JavaScript.
  - Backend API built with Python Flask, running on an EC2 instance.
  - Automated data scraping from EC2 to feed the RDS MySQL database.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask (API)
- **Database:** MySQL (hosted on Amazon RDS)
- **Cloud Infrastructure:** AWS (EC2, RDS)
- **APIs:** JCDecaux API for DublinBikes data, OpenWeather API for weather information
- **Mapping:** Google Maps API
- **Machine Learning:** Python libraries for training and predictions

## Project Structure

- **frontend/**: Contains HTML, CSS, and JavaScript files for the web interface.
- **backend/**: Holds the Flask API code, machine learning scripts, and dependencies.
- **database/**: SQL scripts for setting up the RDS database schema.
- **docs/**: Additional documentation and design materials.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/DublinBikeSharing.git
   cd DublinBikeSharing

2. **Setup Backend**
- Navigate to the backend folder
- Create a virtual environment and install dependencies

```bash
# Change to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment on Mac
source venv/bin/activate

# If you're on Windows, use this command instead:
# venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt
```

3. **Running the Application**
- Start the Flask API
  
```python
# Code to start that Flask App
python app.py
```

- Open 'template/index.html' in your browser to view the interactive map

## Usage
- Interactive Map:
Navigate to the main page to see all Dublin Bike stations displayed on a Google Map. Marker sizes and colors indicate the current bike occupancy and availability.

- Station Details:
Click on a station marker to view detailed occupancy data (hourly and daily) and the local weather forecast.

- Predictive Analytics:
Access the predictions section to see forecasted station occupancy based on the trained machine learning model.
