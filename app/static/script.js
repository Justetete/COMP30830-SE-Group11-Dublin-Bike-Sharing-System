let mapLoaded = false;
const mapElement = document.getElementById('map');
let map;

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !mapLoaded) {
            // Load the Google Maps API when the map is in view
            const script = document.createElement('script');
            script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDuYhHbAe7sJjIaVw8NL-pSHacXpH3cv1U&callback=initMap';
            script.async = true;
            script.defer = true;
            document.body.appendChild(script);

            mapLoaded = true; // Prevent loading multiple times
        }
    });
});

observer.observe(mapElement);

window.initMap = function() {
    // Initialize the map centered at Dublin
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 53.349805, lng: -6.26031 }, // Dublin, Ireland
        zoom: 12
    });

    // Create an InfoWindow instance
    const infoWindow = new google.maps.InfoWindow();

    // Fetch all bike stations and add markers
    fetch("/api/bike_stations")
        .then(response => response.json())
        .then(stations => {
            stations.forEach(station => {
                let marker = new google.maps.Marker({
                    position: station.position,
                    map: map,
                    title: station.name
                });

                // Add a click event to open the InfoWindow and fetch weather info when a marker is clicked
                marker.addListener("click", function() {
                    fetchWeatherData(station); // Fetch weather data
                    const contentString = `
                        <div class="info-window-content">
                            <h2>Station No: ${station.number}</h2>
                            <ul>
                                <li><strong>Address:</strong> ${station.address}</li>
                                <li><strong>Total Bikes:</strong> ${station.bike_stands}</li>
                                <li><strong>Available Bikes:</strong> ${station.available_bikes}</li>
                                <li><strong>Available Stands:</strong> ${station.available_bike_stands}</li>
                            </ul>
                        </div>
                    `;
                    infoWindow.setContent(contentString);
                    infoWindow.open(map, marker);
                });
            });
        })
        .catch(error => console.error("Error fetching bike stations:", error));
};

// Fetch weather data for a specific bike station
function fetchWeatherData(station) {
    const lat = station.position.lat;
    const lon = station.position.lng;
    
    fetch(`/api/weather?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(weatherData => {
            // Update weather info on the page
            updateWeatherInfo(weatherData, station);
        })
        .catch(error => console.error("Error fetching weather data:", error));
}

// Function to update weather info on the page
function updateWeatherInfo(weatherData, station) {
    document.getElementById("temp-here").textContent = `${weatherData.main.temp}°C`;
    document.getElementById("wind-here").textContent = `${weatherData.wind.speed} m/s`;
    document.getElementById("cond-here").textContent = weatherData.weather[0].main;

    // Update the bike station details
    const bikeInfo = document.querySelector(".bike-info");
    const bikeInfoHtml = `
        <h2>Station No: ${station.number}</h2>
        <ul>
            <li><strong>Address:</strong> ${station.address}</li>
            <li><strong>Total Bikes:</strong> ${station.bike_stands}</li>
            <li><strong>Available Bikes:</strong> ${station.available_bikes}</li>
            <li><strong>Available Stands:</strong> ${station.available_bike_stands}</li>
        </ul>
    `;
    bikeInfo.innerHTML = bikeInfoHtml;
}






