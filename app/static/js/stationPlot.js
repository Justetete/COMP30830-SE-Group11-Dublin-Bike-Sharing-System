// ===============================
// Draw Weekly Prediction Chart (Google Charts)
// ===============================
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
          title: 'Predicted Available Bikes (Next 7 Days)',
          legend: { position: 'bottom' },
          curveType: 'function',
          hAxis: {
            title: 'Date',
            format: 'MMM/dd',
            slantedText: true,
            slantedTextAngle: 20,
            textStyle: {
              fontSize: 6
            },
            gridlines: {
              count: 7
            },
          },
          vAxis: { title: 'Available Bikes', minValue: 0 },
          height: 280
        };

        const chart = new google.visualization.LineChart(
          document.getElementById('weeklyChart')
        );
        chart.draw(chartData, options);
      });
  });
}

// ===============================
// Draw Station Bar Chart (Available Bikes & Stands)
// ===============================
function drawStationBarChart(station) {
  const ctx = document.getElementById('stationBarChart').getContext('2d');

  // Destroy existing chart if present
  if (window.stationChart) {
    window.stationChart.destroy();
  }

  // Create new bar chart
  window.stationChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Available Bikes', 'Free Stands'],
      datasets: [{
        label: 'Count',
        data: [station.available_bikes, station.available_bike_stands],
        backgroundColor: ['#187a3c', '#a8d5ba']
      }]
    },
    options: {
      layout: { padding: { top: 20 } },
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: false },
        datalabels: {
          color: '#333',
          anchor: 'end',
          align: 'top',
          font: {
            weight: 'bold',
            size: 12
          },
          formatter: value => value
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true }
      }
    },
    plugins: [ChartDataLabels]
  });
}

// ===============================
// Load Available Dates for Historical Data Dropdown
// ===============================
function loadAvailableDates(stationId) {
  fetch(`/api/history_dates?station_id=${stationId}`)
    .then(res => res.json())
    .then(dates => {
      const select = document.getElementById('dateSelector');

      // If no dates found
      if (!dates || dates.length === 0) {
        select.innerHTML = `<option disabled>No data</option>`;
        return;
      }

      // Populate dropdown with dates
      select.innerHTML = '';
      dates.forEach(dateStr => {
        const option = document.createElement('option');
        option.value = dateStr;
        option.textContent = dateStr;
        select.appendChild(option);
      });

      // Load time series chart for first date by default
      drawTimeSeriesChart(stationId, dates[0]);

      // Update chart on date selection change
      select.onchange = () => {
        drawTimeSeriesChart(stationId, select.value);
      };
    });
}

// ===============================
// Draw Time Series Chart for Selected Day
// ===============================
function drawTimeSeriesChart(stationId, date) {
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(() => {
    const data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Time');
    data.addColumn('number', 'Available Bikes');
    data.addColumn('number', 'Free Stands');

    const url = `/api/history_data?station_id=${stationId}&date=${date}`;

    fetch(url)
      .then(res => res.json())
      .then(rawData => {
        rawData.forEach(entry => {
          data.addRow([
            new Date(entry.time),
            entry.bikes,
            entry.stands
          ]);
        });

        const options = {
          title: '',
          legend: { position: 'bottom' },
          curveType: 'function',
          hAxis: {
            title: 'Time',
            format: 'H:mm'
          },
          vAxis: {
            title: 'Count',
            minValue: 0
          },
          colors: ['#e67e22', '#3498db'],
          height: 280
        };

        const chart = new google.visualization.LineChart(
          document.getElementById('timeSeriesChart')
        );
        chart.draw(data, options);
      })
      .catch(err => {
        console.error("Failed to draw time series chart:", err);
      });
  });
}

// ===============================
// Show Plot Panel (Right Sidebar)
// ===============================
export function showPlotPanel(station) {
  document.getElementById('plot-title').textContent = station.name;
  document.getElementById('plot-number').textContent = `Station No: ${station.number}`;
  document.getElementById('stationPlotPanel').classList.add('active');

  drawStationBarChart(station);
  loadAvailableDates(station.number);
  drawWeeklyPredictionChart(station.number);
}

// ===============================
// Close Plot Panel
// ===============================
export function closePlotPanel() {
  document.getElementById('stationPlotPanel').classList.remove('active');
}

// Make closePlotPanel accessible from global scope
window.closePlotPanel = closePlotPanel;
