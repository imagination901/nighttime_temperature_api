import httpx
from fastapi import FastAPI, Depends
from httpx_client import get_client
from temperature_calculator import calculate_temperature

server = FastAPI()


@server.get("/")
async def healthcheck():
    return {'status': 'OK'}


@server.get('/nighttime_temperature')
async def nighttime_temperature(lat: float, 
                                lng: float,
                                client: httpx.AsyncClient = Depends(get_client)
                                ):
    response = await client.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}')
    response_json = response.json()
    api_data = response_json['results']

    return calculate_temperature(api_data=api_data)