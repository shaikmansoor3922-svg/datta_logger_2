from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse

app = FastAPI()

latest_data = []

class SensorData(BaseModel):
    values: List[float]

@app.get("/")
def home():
    return {"status": "Server Running"}

@app.post("/upload")
def upload_data(data: SensorData):
    global latest_data
    latest_data = data.values
    print("Received:", latest_data)
    return {"message": "Data received successfully"}

@app.get("/latest")
def get_latest():
    return {"values": latest_data}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head>
        <title>ESP Data Dashboard</title>
        <script>
            async function fetchData() {
                const res = await fetch('/latest');
                const data = await res.json();
                document.getElementById("data").innerText = JSON.stringify(data.values);
            }
            setInterval(fetchData, 2000);
        </script>
    </head>
    <body onload="fetchData()">
        <h2>Live Sensor Data</h2>
        <p id="data">Loading...</p>
    </body>
    </html>
    """
