from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from dataclasses import dataclass

class SunriseSunsetData(BaseModel):
    sunrise:                    datetime 
    sunset:                     datetime 
    noon:                       datetime
    morning_twilight_start:     datetime 
    morning_twilight_end:       Optional[datetime]= None
    evening_twilight_start:     Optional[datetime]= None
    evening_twilight_end:       datetime


@dataclass
class ScreenColorTemperature:
    nighttime_temperature: int  = 2700
    daytime_temperature: int    = 6000
