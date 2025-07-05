from pydantic import BaseModel
from models.geo import Coordinates
from datetime import datetime

class GeolocatorEvent(BaseModel):
    address: str

class WeatherHistoryEvent(BaseModel):
    datetime: datetime
    coordinates: Coordinates