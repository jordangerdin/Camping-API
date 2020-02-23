from PIL import Image
import requests
import os
import shutil
def get_API_data(url, params):
    data = requests.get(url = url, params = params).json()
    return data

def get_hiking_data(lat, lon):
    key = os.environ.get('HIKING_KEY')
    url = 'https://www.hikingproject.com/data/get-trails'

    params = {'lat' : lat, 'lon' : lon, 'key' : key}

    hiking_data = get_API_data(url, params)

    return hiking_data

def get_weather_data(lat, lon):
    key = os.environ.get('WEATHER_KEY')
    url = 'https://samples.openweathermap.org/data/2.5/forecast/daily'

    params = {'lat' : lat, 'lon' : lon, 'cnt' : 10, 'appid' : key}

    weather_data = get_API_data(url, params)

    return weather_data

def get_map(lat, lon):
    key = os.environ.get('MAP_KEY')
    params = {'access_token' : key}
    url = f'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lon},{lat},10,0,0/600x600'

    map_image = requests.get(url, params, stream=True) 
    map_image.raw.decode_content = True

    return map_image.raw

"""test_lat = 44.97997
test_lon = -93.26384

map_img = Image.open(get_map(test_lat, test_lon))
map_img.show()
"""