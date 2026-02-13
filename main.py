from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")

latest_data = []
last_update_time = 0
all_data = []

class SensorData(BaseModel):
    values: List[float]

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/upload")
def upload_data(data: SensorData):
    global latest_data, last_update_time, all_data
    
    latest_data = data.values
    last_update_time = time.time()
    all_data.append(data.values)

    return {"message": "Data received"}

@app.get("/latest")
def get_latest():
    return {
        "values": latest_data,
        "last_update": last_update_time
    }

@app.get("/all")
def get_all():
    return {"history": all_data}
