from api_connection import *
from PIL import Image

location_name = input('Please enter the city you would like to go hiking by in city, state format.')
coord = get_lat_lon(location_name)

return_str = ''
return_str += get_hiking_data(coord['lat'], coord['lng'])['trails'][0]['name'] + '\n'

trail_lat =  get_hiking_data(coord['lat'], coord['lng'])['trails'][0]['latitude']
trail_lon =  get_hiking_data(coord['lat'], coord['lng'])['trails'][0]['longitude']

return_str += get_weather_data(trail_lat, trail_lon)['list'][0]['weather'][0]['main'] + '\n'
map_image = Image.open(get_map(trail_lat, trail_lon))

print(return_str)
map_image.show()
