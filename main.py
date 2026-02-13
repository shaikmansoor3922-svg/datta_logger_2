from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

latest_data = []

class SensorData(BaseModel):
    values: List[float]


@app.post("/upload")
def upload_data(data: SensorData):
    global latest_data
    latest_data = data.values
    print("Received:", latest_data)
    return {"message": "Data received successfully"}


@app.get("/latest")
def get_latest():
    return {"values": latest_data}


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("dashboard.html", "r") as f:
        return f.read()
