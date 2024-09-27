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