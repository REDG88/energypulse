document.getElementById('askButton').addEventListener('click', async function() {
    const userQuery = document.getElementById('userQuery').value;
    const queryType = 'fault_detection'; // You can modify this based on your requirements

    const response = await fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: userQuery, type: queryType })
    });

    const data = await response.json();
    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
});

// Function to render the chart
function renderChart(data) {
    const ctx = document.getElementById('faultMetricsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Fault Occurrences',
                data: Object.values(data),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Call this function to initially load fault metrics when the page loads
window.onload = async () => {
    const response = await fetch('/metrics');  // You will implement this endpoint
    const metricsData = await response.json();
    renderChart(metricsData);
};
