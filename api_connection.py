import requests
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

def get_API_data(url, params):
    # generic method to talk to a JSON api.
    data = requests.get(url = url, params = params).json()
    return data

def get_hiking_data(lat, lon):
    # method for getting the data on hiking trails
    key = os.getenv('HIKING_KEY')
    url = 'https://www.hikingproject.com/data/get-trails'

    params = {'lat' : lat, 'lon' : lon, 'key' : key}

    hiking_data = get_API_data(url, params)

    return hiking_data

def get_weather_data(lat, lon):
    
    key = os.getenv('WEATHER_KEY')

    url = 'https://api.openweathermap.org/data/2.5/forecast'

    params = {'lat' : lat, 'lon' : lon, 'appid' : key}

    weather_data = get_API_data(url, params)

    return weather_data

def get_lat_lon(place_name):
    # method for getting the lat and long from a place name.
    key = os.getenv('GEOCODING_KEY')
    url = 'https://api.opencagedata.com/geocode/v1/json'

    params = {'key' : key, 'q' : place_name}

    lat_lon = get_API_data(url, params)

    return lat_lon['results'][0]['geometry']

