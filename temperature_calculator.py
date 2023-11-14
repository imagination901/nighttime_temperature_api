from models import SunriseSunsetData
from datetime import datetime
from models import ScreenColorTemperature


def parse_time_str(time_str: str) -> datetime:
    # Parse the string and convert it to a datetime.time object
    time_format = '%I:%M:%S %p'  # Format for "5:34:10 AM"
    parsed_time = datetime.strptime(time_str, time_format).time()
    datetime_object = datetime(
        year=   datetime.now().year,
        month=  datetime.now().month,
        day=    datetime.now().day,
        hour=   parsed_time.hour,
        minute= parsed_time.minute,
        second= parsed_time.second
        )
    return datetime_object 


def get_temp(sun_set_data: SunriseSunsetData) -> int:
    #_now = datetime.now()
    _now = datetime                             (2023, 11, 14, 18, 7, 4)
    '''
    morning_twilight_start= datetime.datetime   (2023, 11, 14, 5, 13, 38) 
    sunrise=datetime.       datetime            (2023, 11, 14, 5, 34, 17) 
    morning_twilight_end=   datetime.datetime   (2023, 11, 14, 5, 54, 56) 

    noon=datetime.          datetime            (2023, 11, 14, 11, 40, 23) 
    
    evening_twilight_start= datetime.datetime   (2023, 11, 14, 17, 25, 49) 
    sunset=datetime.        datetime            (2023, 11, 14, 17, 46, 28) 
    evening_twilight_end=   datetime.datetime   (2023, 11, 14, 18, 7, 7)
    '''

    def _now_is_night_time(now: datetime, ssd: SunriseSunsetData) -> bool:
        if now < ssd.morning_twilight_start or now > ssd.evening_twilight_end:
            return True 
        return False
    
    def _now_is_day_time(now: datetime, ssd: SunriseSunsetData) -> bool:
        if now >= ssd.morning_twilight_end and now < ssd.evening_twilight_start: #type: ignore
            return True
        return False
    
    def _now_is_morning_twilight(now: datetime, ssd: SunriseSunsetData) -> bool:
        if now >= ssd.morning_twilight_start and now < ssd.morning_twilight_end: #type: ignore
            return True
        return False
    
    def _get_temp_gradient(now: datetime, ssd:SunriseSunsetData) -> int:
        if _now_is_morning_twilight(now, ssd):
            now_delta_seconds = (now - ssd.morning_twilight_start).total_seconds()
            morning_delta_seconds = (ssd.morning_twilight_end - ssd.morning_twilight_start).total_seconds() #type: ignore
            morning_temp_gradient = ScreenColorTemperature.nighttime_temperature + \
                ((ScreenColorTemperature.daytime_temperature - ScreenColorTemperature.nighttime_temperature) * \
                (now_delta_seconds/morning_delta_seconds))
            morning_temp_gradient= int(morning_temp_gradient)
            return morning_temp_gradient

        # Otherwise, it's evening twilight gradient we're looking for
        now_delta_seconds = (now - ssd.evening_twilight_start).total_seconds()                          #type: ignore
        evening_delta_seconds = (ssd.evening_twilight_end - ssd.evening_twilight_start).total_seconds() #type: ignore
        evening_temp_gradient = ScreenColorTemperature.daytime_temperature - \
            ((ScreenColorTemperature.daytime_temperature - ScreenColorTemperature.nighttime_temperature) * \
            (now_delta_seconds/evening_delta_seconds))
        evening_temp_gradient= int(evening_temp_gradient)
        return evening_temp_gradient
        

    if _now_is_night_time(_now, sun_set_data):
        return ScreenColorTemperature.nighttime_temperature
    elif _now_is_day_time(_now, sun_set_data):
        return ScreenColorTemperature.daytime_temperature
    elif _now_is_morning_twilight(_now, sun_set_data):
        return _get_temp_gradient(_now, sun_set_data)
    #Otherwise, it's the evening twilitht zone
    return _get_temp_gradient(_now, sun_set_data)


def calculate_temperature(sunrise_sunset_json: dict) -> dict[str, int]:
    times = sunrise_sunset_json['results']
    ssd = SunriseSunsetData(
        sunrise=                parse_time_str(times['sunrise']),
        sunset=                 parse_time_str(times['sunset']),
        noon=                   parse_time_str(times['solar_noon']),
        morning_twilight_start= parse_time_str(times['civil_twilight_begin']),
        evening_twilight_end=   parse_time_str(times['civil_twilight_end'])
    )
    ssd.morning_twilight_end = ssd.sunrise + (ssd.sunrise - ssd.morning_twilight_start)
    ssd.evening_twilight_start = ssd.sunset - (ssd.evening_twilight_end - ssd.sunset)

    temperature = get_temp(sun_set_data=ssd)

    return {'temperature': temperature}
