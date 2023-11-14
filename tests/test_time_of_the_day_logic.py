from models import SunriseSunsetData
import datetime
from temperature_calculator import get_temp


morning_twilight_start= datetime.datetime(2023, 11, 14, 5, 13, 38) 
sunrise=                datetime.datetime(2023, 11, 14, 5, 34, 17) 
morning_twilight_end=   datetime.datetime(2023, 11, 14, 5, 54, 56) 
noon=                   datetime.datetime(2023, 11, 14, 11, 40, 23) 
evening_twilight_start= datetime.datetime(2023, 11, 14, 17, 25, 49) 
sunset=                 datetime.datetime(2023, 11, 14, 17, 46, 28) 
evening_twilight_end=   datetime.datetime(2023, 11, 14, 18, 7, 7)

test_ssd = SunriseSunsetData(sunrise=sunrise,
                             sunset=sunset,
                             noon=noon,
                             morning_twilight_start=morning_twilight_start,
                             morning_twilight_end=morning_twilight_end,
                             evening_twilight_start=evening_twilight_start,
                             evening_twilight_end=evening_twilight_end)

def test_night_get_temp():
    night_now = datetime.datetime(2023, 11, 14, 1, 1, 1)
    assert get_temp(now=night_now, sun_set_data=test_ssd) == 2700


def test_day_get_temp():
    day_now = datetime.datetime(2023, 11, 14, 11, 1, 1)
    assert get_temp(now=day_now, sun_set_data=test_ssd) == 6000


def test_morning_twilight_get_temp():
    morning_twilight_now = datetime.datetime(2023, 11, 14, 5, 31, 1)
    assert 2700 <= get_temp(now=morning_twilight_now, sun_set_data=test_ssd) <= 6000


def test_evening_twilight_get_temp():
    evening_twilight_now = datetime.datetime(2023, 11, 14, 17, 40, 1)
    assert 2700 <= get_temp(now=evening_twilight_now, sun_set_data=test_ssd) <= 6000