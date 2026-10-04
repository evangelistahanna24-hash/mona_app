<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mona Visual Engine</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f0f2f6; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .success { color: #0a8c3e; font-weight: bold; }
        button { background: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 16px; }
        button:hover { background: #e03e3e; }
    </style>
</head>
<body>

<div class="card">
    <h2>📡 Data Received from Streamlit</h2>
    <div id="streamlit-data">Waiting for input...</div>
</div>

<div class="card">
    <h2>🧾 Calculation / Result Area</h2>
    <p>Processed health index appears below:</p>
    <div id="result-display" class="success">—</div>
    <br>
    <button onclick="sendResultToStreamlit()">📥 Send Result Back to Dashboard</button>
</div>

<script>
// ─── RECEIVE from Streamlit ───
let receivedData = null;

function receiveStreamlitData(data) {
    receivedData = data;
    const display = document.getElementById('streamlit-data');
    display.innerHTML = `
        <strong>Age:</strong> ${data.age} yrs<br>
        <strong>Weight:</strong> ${data.weight} kg<br>
        <strong>Heart Rate:</strong> ${data.heart_rate} bpm<br>
        <strong>Condition:</strong> ${data.condition}
    `;
    // Example local calculation
    const healthIndex = Math.round((data.weight / data.age) * data.heart_rate / 10);
    document.getElementById('result-display').textContent = `Health Index Score: ${healthIndex}`;
}

// Catch initial data sent at load
if (window.initialData) {
    receiveStreamlitData(window.initialData);
}

// Listen for updates from Streamlit
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'FROM_STREAMLIT_TO_HTML') {
        receiveStreamlitData(event.data.payload);
    }
});

// ─── SEND back to Streamlit ───
function sendResultToStreamlit() {
    const resultData = {
        status: "processed",
        health_index: document.getElementById('result-display').textContent,
        note: "Calculated inside HTML visual",
        timestamp: new Date().toISOString()
    };

    window.parent.postMessage({
        type: 'FROM_HTML_TO_STREAMLIT',
        payload: resultData
    }, '*');

    alert("✅ Result sent to Streamlit dashboard!");
}
</script>

</body>
</html># mona_app
