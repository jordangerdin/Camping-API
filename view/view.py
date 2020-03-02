from model.model import Bookmarks
from api_connection import get_hiking_data, get_lat_lon

# View for bookmarks db, may not be necessary with web-based frontend

class View:
    def __init__(self, view_model):
        self.view_model = view_model

    def add_new_trail(self):
        coord = get_lat_lon(input('Enter a location to search: '))
        trail_data = get_hiking_data(coord['lat'], coord['lng'])['trails'][0]

        id = trail_data['id']
        name = trail_data['name']
        trailtype = trail_data['type']
        difficulty = trail_data['difficulty']
        stars = trail_data['stars']
        location = trail_data['location']
        url = trail_data['url']
        length = trail_data['length']
        ascent = trail_data['ascent']
        descent = trail_data['descent']
        longitude = trail_data['longitude']
        latitude = trail_data['latitude']
        condition_details = trail_data['conditionDetails']

        self.view_model.insertTrail(id, name, trailtype, difficulty, stars, location, url, length, ascent, descent, longitude, latitude, condition_details)

    def get_user_input(self, message):
        return input(message)
