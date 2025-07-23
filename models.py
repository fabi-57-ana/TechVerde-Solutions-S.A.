from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = "weather_api"
    
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100), index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    weather_description = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow)

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)