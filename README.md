# Dublin Bike sharing Website Project - COMP30380 Software Engineering

## Group Members
- Jian, Xinchi
- Kavanagh, Alex
- Tully, Mark



## Project Description

- Collect "DublinBikes" dynamic station occupancy data from JCDecaux
- Every 5 minutes, aiming to have several weeks of continuous data
- Collect data about weather from "OpenWeather" for every hour
- Store data in a database Amazon RDS (MySQL)
- Display station data on a google map
- Possibly encode the occupancy and availability in color/size of the markers simple map interactivity
- Display more detailed occupancy (hourly, daily) bar chart when a station is clicked
- Clicking on station will show weather forecast too (OpenWeather)
- Machine Learning model to predict occupancy based on collected data
- Predications are regularly updated as new occupancy data is collected
- We have a frontend (CSS, HTML, JS) for an application
- API is implemented with python flask app running on EC2
- EC2 instance will scrape bike data and stores in RDS MySql
