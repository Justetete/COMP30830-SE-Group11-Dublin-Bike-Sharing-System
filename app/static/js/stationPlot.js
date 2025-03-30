// Display current Station infromation (avaialable bikes and stands)
function drawStationBarChart(station) {
    const ctx = document.getElementById('stationBarChart').getContext('2d');
  
    if (window.stationChart) {
      window.stationChart.destroy();
    }
  
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

  function loadAvailableDates(stationId) {
    fetch(`/api/history_dates?station_id=${stationId}`)
    .then(res => res.json())
    .then(dates => {
        if (!dates || dates.length === 0) {
        document.getElementById('dateSelector').innerHTML = `<option disabled>No data</option>`;
        return;
        }

        const select = document.getElementById('dateSelector');
        select.innerHTML = '';

        dates.forEach(dateStr => {
        const option = document.createElement('option');
        option.value = dateStr;
        option.textContent = dateStr;
        select.appendChild(option);
        });

        drawTimeSeriesChart(stationId, dates[0]);

        select.onchange = () => {
        drawTimeSeriesChart(stationId, select.value);
        };
    });
  }

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
  
  
  // Open the right side panel
  export function showPlotPanel(station) {
    document.getElementById('plot-title').textContent = station.name;
    document.getElementById('plot-number').textContent = `Station No: ${station.number}`;
    document.getElementById('stationPlotPanel').classList.add('active');
  
    drawStationBarChart(station);
    loadAvailableDates(station.number);
  }
  
  // Close the panel
  export function closePlotPanel() {
    document.getElementById('stationPlotPanel').classList.remove('active');
  }
  
  window.closePlotPanel = closePlotPanel;
  