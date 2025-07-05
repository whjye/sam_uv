from pydantic import BaseModel
from typing import Optional


class WeatherDataRecord(BaseModel):
    tavg: Optional[float] = None
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    prcp: Optional[float] = None
    snow: Optional[float] = None
    wdir: Optional[float] = None
    wspd: Optional[float] = None
    wpgt: Optional[float] = None
    pres: Optional[float] = None
    tsun: Optional[float] = None


class WeatherDataList(BaseModel):
    data: list[WeatherDataRecord] = None