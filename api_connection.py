from PIL import Image
import requests
import os
import shutil

def get_API_data(url, params):
    # generic method to talk to a JSON api.
    data = requests.get(url = url, params = params).json()
    return data

def get_hiking_data(lat, lon):
    # method for getting the data on hiking trails
    key = os.environ.get('HIKING_KEY')
    url = 'https://www.hikingproject.com/data/get-trails'

    params = {'lat' : lat, 'lon' : lon, 'key' : key}

    hiking_data = get_API_data(url, params)

    return hiking_data

def get_weather_data(lat, lon):
    # method for getting data on the weather
    key = os.environ.get('WEATHER_KEY')
    url = 'https://samples.openweathermap.org/data/2.5/forecast/daily'

    params = {'lat' : lat, 'lon' : lon, 'cnt' : 10, 'appid' : key}

    weather_data = get_API_data(url, params)

    return weather_data

def get_map(lat, lon):
    # method for getting a map. Does not use the get_API_data method as the responce is not JSON
    # information on getting images from an API found here:
        # www.dev2qa.com/how-to-download-image-file-from-url-use-python-requests-or-wget-module/
    key = os.environ.get('MAP_KEY')
    params = {'access_token' : key}
    url = f'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lon},{lat},10,0,0/600x600'

    map_image = requests.get(url, params, stream=True) 
    map_image.raw.decode_content = True

    return map_image.raw

def get_lat_lon(place_name):
    key = '24122d2069da4857acfb61e5b14be3f2'
    url = 'https://api.opencagedata.com/geocode/v1/json'

    params = {'key' : key, 'q' : place_name}

    lat_lon = get_API_data(url, params)
    return lat_lon['results'][0]['geometry']

#test_place_name = 'Minneapolis, MN'
#print(get_lat_lon(test_place_name))

"""test_lat = 44.97997
test_lon = -93.26384

# The method used to open the map image. PIL must be imported to do this.

map_img = Image.open(get_map(test_lat, test_lon))
map_img.show()
"""