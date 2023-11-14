import httpx

def test_external_api_response():
    client = httpx.Client()
    lat, lng = 1.1, 2.2
    response = client.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}')
    assert response.status_code == 200