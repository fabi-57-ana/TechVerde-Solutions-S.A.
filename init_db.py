from database import Base, engine
from models import WeatherData, SensorData

Base.metadata.create_all(bind=engine)