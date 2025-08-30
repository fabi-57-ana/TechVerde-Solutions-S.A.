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
        print("Iniciando generación de gráficos...")
        # Datos actuales de la base de datos
        weather_data = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()
        sensor_data = db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(10).all()
        
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

        print(f"Weather data: {weather_data}")
        print(f"Sensor data: {sensor_data}")

        # Usar coordenadas fijas para "El Corito" (independiente de latest_city)
        lat, lon = -30.3333, -64.2500  # Coordenadas aproximadas de El Corito
        forecast_city = " 'El Corito', El Simbolar, Córdoba"
        print(f"Coordenadas para pronóstico: ({lat}, {lon}), Ciudad: {forecast_city}")

        # Consultar Open-Meteo para pronóstico de 7 días
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,weathercode&forecast_days=7"
        print(f"URL de pronóstico: {url}")
        response = requests.get(url)
        response.raise_for_status()
        forecast_data = response.json().get("hourly", {})
        times = forecast_data.get("time", [])
        temps = forecast_data.get("temperature_2m", [])
        humidities = forecast_data.get("relative_humidity_2m", [])
        weather_codes = forecast_data.get("weathercode", [])

        # Formatear pronóstico (7 días, datos diarios aproximados)
        formatted_forecast = []
        for i in range(0, 7 * 24, 24):  # Tomar un valor por día
            if i < len(times):
                formatted_forecast.append({
                    "date": times[i][:10],  # Fecha en formato YYYY-MM-DD
                    "temp_max": max(temps[i:i+24]) if i+23 < len(temps) else temps[i],
                    "temp_min": min(temps[i:i+24]) if i+23 < len(temps) else temps[i],
                    "humidity": humidities[i] if i < len(humidities) else 0,
                    "description": weather_code_to_description(weather_codes[i]) if i < len(weather_codes) else "Desconocido"
                })

        print(f"Datos de pronóstico formateados: {formatted_forecast}")

        return templates.TemplateResponse("charts.html", {
            "request": request,
            "weather_data": weather_data,
            "sensor_data": sensor_data,
            "forecast_data": formatted_forecast,
            "forecast_city": forecast_city
        })
    except Exception as e:
        print(f"Error en charts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar gráficos: {str(e)}")

def get_lat_lon(city_name):
    city_coords = {
        "Salta": (-24.7859, -65.4117),
        "Santa Fe": (-31.6333, -60.7000),
        "Buenos Aires": (-34.6037, -58.3816),
        "Cordoba": (-31.4167, -64.1833)
    }
    return city_coords.get(city_name, (-24.7859, -65.4117))  # Default a Salta

def weather_code_to_description(code):
    # Mapeo básico de códigos WMO a descripciones (simplificado)
    code_map = {
        0: "Cielo despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
        3: "Nublado", 45: "Niebla", 48: "Niebla helada", 51: "Llovizna ligera",
        53: "Llovizna moderada", 55: "Llovizna densa", 61: "Lluvia ligera",
        63: "Lluvia moderada", 65: "Lluvia fuerte", 80: "Chubascos ligeros",
        81: "Chubascos moderados", 82: "Chubascos fuertes"
    }
    return code_map.get(code, "Desconocido")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


