from PIL import Image
import requests
import os

def get_API_data(url, params):
    data = requests.get(url = url, params = params).json()
    return data

def get_hiking_data(lat, lon):
    key = os.environ.get('HIKING_KEY')
    url = 'https://www.hikingproject.com/data/get-trails'

    params = {'lat' : lat, 'lon' : lon, 'key' : key}

    hiking_data = get_API_data(url, params)

    return hiking_data
