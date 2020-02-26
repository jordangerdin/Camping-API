from flask import Flask, render_template, flash, redirect, url_for, request
from api_connection import *
from forms import LocationInputForm
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blargitsasecretthatdoesntmatterforthiscontext'

trail_dictionary = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/find_trails', methods=['GET', 'POST'])
def hello():
    # Gets the location info from the user through thte form, gives it to the geocoding API, gets the lat and long from it and feeds that to the hiking API
    # Hiking API returns a dictionary of trails that's saved in a global variable for future use and fed to the main page.
    global trail_dictionary

    loc_form = LocationInputForm()
    if loc_form.validate_on_submit():
        location_name = loc_form.city.data + ', ' + loc_form.state.data
        try:
            coord = get_lat_lon(location_name)
            if coord is not None:
                trail_dictionary = get_hiking_data(coord['lat'], coord['lng'])['trails']
        except:
            flash('There was a problem connecting to the geocoding API')
    return render_template('home.html', location_form = loc_form, trail_list = trail_dictionary)

@app.route('/show_extra', methods=['POST'])
def show_extra():
    #Using a global variable to store the trails so we can minimize API calls while still using the data accross different pages.
    global trail_dictionary 

    #This is the same code from hello(), because we're adding to that page and want to keep its origional functionality.
    loc_form = LocationInputForm()
    if loc_form.validate_on_submit():
        location_name = loc_form.city.data + ', ' + loc_form.state.data
        try:
            coord = get_lat_lon(location_name)
            if coord is not None:
                trail_dictionary = get_hiking_data(coord['lat'], coord['lng'])['trails']
            else:
                flash('test')
        except:
            flash('There was a problem connecting to the geocoding API ' + location_name + 'test')

    # Getting the lat and long of the trail
    lat_long = request.form.get('trail_select')
    lat_long_list = lat_long.split(',')

    # The show weather set up. Makes an API call to get the weather for the next ten days and feeds that to the page
    if request.form['submit_button'] == 'show_weather':
        weather_data = get_weather_data(lat_long_list[0],lat_long_list[1])
        for day in weather_data['list']:
            day['dt'] = datetime.fromtimestamp(day['dt'])
            for key, temp in day['temp'].items():
                day['temp'][key] = k_to_f(temp)
        return render_template('show_weather.html', weather_list = weather_data, location_form = loc_form, trail_list = trail_dictionary)

    # The show map set up 
    else:
        return render_template('show_map.html', lat = lat_long_list[0], lon = lat_long_list[1], key = os.environ.get('MAP_KEY'), location_form = loc_form, trail_list = trail_dictionary)


def k_to_f(kelvin):
    # A helpter function to make the weather's temperature data into a unit that Americans know what to do with.
    return int((float(kelvin) - 273.15) * 9/5 + 32)
