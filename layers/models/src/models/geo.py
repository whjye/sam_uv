from pydantic import BaseModel
from typing import Optional

class Coordinates(BaseModel):
    latitude: float
    longitude: float
    altitude: Optional[float] = None
