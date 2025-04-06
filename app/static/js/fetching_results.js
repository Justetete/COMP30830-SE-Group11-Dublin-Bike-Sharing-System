function predict() {
    console.log("predict function is called");
    document.getElementById('prediction-card').classList.remove('d-none');

    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    const station_id = document.getElementById("station_id").value;
    const resultDiv = document.getElementById("result");

    // Validate input
    if (!date || !time || !station_id) {
        resultDiv.innerHTML = "Please select date time and station.";
        return;
    }

    // Format time to HH:MM:SS
    const formattedTime = `${time}:00`;

    // Send GET request to Flask API
    fetch(`/predict?date=${date}&time=${formattedTime}&station_id=${station_id}`, {
        method: "GET"
    })
        .then(response => response.json())
        .then(data => {
            if (data.predicted_available_bikes !== undefined) {
                resultDiv.innerHTML = `Predicted Available Bikes: ${data.predicted_available_bikes}`;
            } else {
                resultDiv.innerHTML = `Error: ${data.error || "Something went wrong"}`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `Error: ${error.message}`;
        });
}

function drawWeeklyPredictionChart(stationId) {
    google.charts.load('current', { packages: ['corechart'] });
    google.charts.setOnLoadCallback(() => {
      fetch(`/predict_week?station_id=${stationId}`)
        .then(response => response.json())
        .then(data => {
          const chartData = new google.visualization.DataTable();
          chartData.addColumn('datetime', 'Time');
          chartData.addColumn('number', 'Predicted Bikes');
  
          data.forEach(entry => {
            chartData.addRow([
              new Date(entry.time),
              entry.predicted_bikes
            ]);
          });
  
          const options = {
            title: 'Weekly Bike Availability Prediction',
            legend: { position: 'bottom' },
            curveType: 'function',
            hAxis: { format: 'MM/dd HH:mm' },
            vAxis: { minValue: 0 },
            height: 300
          };
  
          const chart = new google.visualization.LineChart(
            document.getElementById('weeklyChart')
          );
          chart.draw(chartData, options);
        });
    });
  }
  
