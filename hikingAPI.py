from PIL import Image
import requests
import os

lat = 40.0274
lon = -105.2519
key = os.environ.get('HIKING_KEY')

params = {'lat' : lat, 'lon' : lon, 'key' : key}
url = 'https://www.hikingproject.com/data/get-trails'

hiking_data = requests.get(url = url, params = params).json()

print(hiking_data)