from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import WeatherData, SensorData
import requests
from datetime import datetime, UTC
from dotenv import load_dotenv
import os
import uvicorn
import json

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weather/city/{city_name}")
async def get_weather(city_name: str, request: Request, db: Session = Depends(get_db)):
    try:
        url = f"{BASE_URL}/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        weather = WeatherData(
            city_name=city_name,
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            weather_description=data["weather"][0]["description"],
            timestamp=datetime.now(UTC)
        )
        db.add(weather)
        db.commit()
        
        return templates.TemplateResponse("weather.html", {
            "request": request,
            "city": city_name,
            "weather": data
        })
    except requests.RequestException:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada o error en la API")

@app.post("/sensor/data")
async def post_sensor_data(data: dict, db: Session = Depends(get_db)):
    try:
        sensor = SensorData(
            temperature=data["temperature"],
            humidity=data["humidity"],
            timestamp=datetime.now(UTC)
        )
        db.add(sensor)
        db.commit()
        return {"status": "success"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Datos inválidos")

@app.get("/weather/last")
async def get_last_weather(request: Request, db: Session = Depends(get_db)):
    weather_data = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "weather_data": weather_data
    })

@app.get("/sensor/last")
async def get_last_sensor(request: Request, db: Session = Depends(get_db)):
    sensor_data = db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(10).all()
    return templates.TemplateResponse("sensor.html", {
        "request": request,
        "sensor_data": sensor_data
    })

@app.get("/charts")
async def charts(request: Request, db: Session = Depends(get_db)):
    try:
        weather_data = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()
        sensor_data = db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(10).all()
        
        # Convertir datos a formato JSON serializable
        weather_data = [
            {
                "city_name": item.city_name or "",
                "temperature": float(item.temperature) if item.temperature is not None else 0.0,
                "humidity": float(item.humidity) if item.humidity is not None else 0.0,
                "pressure": float(item.pressure) if item.pressure is not None else 0.0,
                "wind_speed": float(item.wind_speed) if item.wind_speed is not None else 0.0,
                "weather_description": item.weather_description or "",
                "timestamp": item.timestamp.isoformat() if item.timestamp else ""
            }
            for item in weather_data
        ]
        sensor_data = [
            {
                "temperature": float(item.temperature) if item.temperature is not None else 0.0,
                "humidity": float(item.humidity) if item.humidity is not None else 0.0,
                "timestamp": item.timestamp.isoformat() if item.timestamp else ""
            }
            for item in sensor_data
        ]
        
        return templates.TemplateResponse("charts.html", {
            "request": request,
            "weather_data": weather_data,
            "sensor_data": sensor_data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráficos: {str(e)}")
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

