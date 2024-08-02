# src/utils/fetch_weather_data.py

import requests
from config import WEATHER_API_URL, WEATHER_API_KEY, CURRENT_WEATHER_ENDPOINT

def fetch_current_weather(lat, lon):
    url = WEATHER_API_URL + CURRENT_WEATHER_ENDPOINT.format(lat, lon, WEATHER_API_KEY)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed with status code: {response.status_code}")
        return None

if __name__ == '__main__':
    lat = 50.814
    lon = 15.709
    weather_data = fetch_current_weather(lat, lon)
    print(weather_data)
