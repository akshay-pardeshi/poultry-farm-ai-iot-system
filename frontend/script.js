// Chart setup
const ctx = document.getElementById('sensorChart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperature (°C)',
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(230, 126, 34, 0.1)',
                data: [],
                fill: true,
                tension: 0.4
            },
            {
                label: 'Humidity (%)',
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                data: [],
                fill: true,
                tension: 0.4
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

let chartDataIndex = 0;

function updateChart(temp, humid) {
    if (chartDataIndex >= 10) {
        sensorChart.data.labels.shift();
        sensorChart.data.datasets[0].data.shift();
        sensorChart.data.datasets[1].data.shift();
    }

    sensorChart.data.labels.push(new Date().toLocaleTimeString());
    sensorChart.data.datasets[0].data.push(temp);
    sensorChart.data.datasets[1].data.push(humid);

    chartDataIndex++;
    sensorChart.update();
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

// Fetch data from Flask backend every 5 seconds
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/data'); // Change IP if deploying
        const data = await response.json();

        // Update DOM elements
        document.getElementById("temp").innerText = data.temperature;
        document.getElementById("humid").innerText = data.humidity;
        document.getElementById("nh3").innerText = data.nh3;
        document.getElementById("age").innerText = data.age;
        document.getElementById("eggs").innerText = data.egg_forecast;
        document.getElementById("health").innerText = `${data.health_status} (AI: ${data.predicted_health})`;
        document.getElementById("disease").innerText = data.disease_type;
        document.getElementById("sound").innerText = data.sound;
        document.getElementById("predicted-health").innerText = data.predicted_health;
        document.getElementById("prediction-time").innerText = new Date().toLocaleTimeString();

        // 🆕 Update chart
        updateChart(data.temperature, data.humidity);

        // Alert Logic
        const alertList = document.getElementById("alerts");
        alertList.innerHTML = "";

        if (parseFloat(data.temperature) > 32) {
            alertList.innerHTML += "<li>⚠️ High Temperature Detected!</li>";
        }
        if (parseFloat(data.nh3) > 7) {
            alertList.innerHTML += "<li>⚠️ High Ammonia Level!</li>";
        }
        if (data.health_status === "Sick" || data.predicted_health === "Sick") {
            alertList.innerHTML += "<li>🚨 Sickness Detected in Chickens!</li>";
        }
        if (data.sound === "Sneezing" || data.sound === "Distress Call") {
            alertList.innerHTML += "<li>🔔 Unusual Sound Detected!</li>";
        }

        if (alertList.innerHTML === "") {
            alertList.innerHTML = "<li>No alerts at the moment.</li>";
        }

    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("alerts").innerHTML = "<li>🔴 Error connecting to backend</li>";
    }
}

// Initial fetch + auto-refresh every 5 seconds
fetchData();
setInterval(fetchData, 5000);
