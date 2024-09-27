document.getElementById('askButton').addEventListener('click', async function() {
    const userQuery = document.getElementById('userQuery').value;
    const queryType = 'fault_detection';  // Modify as needed

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

// Function to render dynamic table
function renderTable(data) {
    const tableBody = document.getElementById('data-table-body');
    tableBody.innerHTML = '';  // Clear existing content

    data.forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(cellData => {
            const td = document.createElement('td');
            td.innerText = cellData;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

// Fetch the data when the page loads
window.onload = async () => {
    const response = await fetch('/metrics');
    const metricsData = await response.json();
    renderChart(metricsData);

    const tableResponse = await fetch('/');  // Fetch initial CSV data
    const tableData = await tableResponse.json();
    renderTable(tableData);
};
