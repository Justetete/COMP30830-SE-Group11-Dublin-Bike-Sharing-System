// -------------------------add a heatmap to Google Map------------------
function addHeatmap(stations) {
    // Create an array to store the heatmap data points
    var heatmapData = [];
    // Iterate through the stations and add their location and available bikes as data points
    stations.forEach((station) => {
        var location = new google.maps.LatLng(Number(station.positionLat), Number(station.positionLng));
        var weight = parseInt(station.availableBikes, 10);

        // Add the data point to the heatmapData array
        heatmapData.push({location: location, weight: weight});
    });
    // Create the heatmap
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        radius: 50,
        opacity: 0.6,
        gradient: [
            "rgba(255, 255, 255, 0)",
            "rgba(173, 216, 230, 1)",
            "rgba(135, 206, 235, 1)",
            "rgba(135, 206, 250, 1)",
            "rgba(100, 149, 237, 1)",
            "rgba(70, 130, 180, 1)",
            "rgba(65, 105, 225, 1)",
            "rgba(0, 0, 255, 1)",
            "rgba(0, 0, 205, 1)",
            "rgba(0, 0, 139, 1)",
            "rgba(0, 0, 128, 1)",
            "rgba(25, 25, 112, 1)",
            "rgba(0, 0, 90, 1)",
            "rgba(0, 0, 60, 1)"
        ]
    });
    // Add event listener to the toggle button
    document.getElementById("toggle-heatmap").addEventListener("click", function () {
        if (heatmap.getMap() == null) {
            // Show the heatmap layer
            heatmap.setMap(map);
        } else {
            // Hide the heatmap layer
            heatmap.setMap(null);
        }
    });
}