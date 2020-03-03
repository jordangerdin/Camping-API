from flask import Flask, render_template, flash, redirect, url_for, request
from api_connection import *
from forms import LocationInputForm
from datetime import datetime
import os
import view_model
from model.model import Bookmarks
from sql_database.database import SQLTrailDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blargitsasecretthatdoesntmatterforthiscontext'

trail_dictionary = {}
trailsDB = SQLTrailDB

@app.route('/', methods=['GET', 'POST'])
@app.route('/find_trails', methods=['GET', 'POST'])
def home():
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
            else:
                flash('City and state not found.', 'error')
        except:
            flash('There was a problem connecting to the geocoding API', 'error')
    return render_template('home.html', location_form = loc_form, trail_list = trail_dictionary)

@app.route('/show_extra', methods=['POST'])
def show_extra():
    #Using a global variable to store the trails so we can minimize API calls while still using the data accross different pages.
    global trail_dictionary 

    #This is the same code from home(), because we're adding to that page and want to keep its origional functionality.
    loc_form = LocationInputForm()
    if loc_form.validate_on_submit():
        location_name = loc_form.city.data + ', ' + loc_form.state.data
        try:
            coord = get_lat_lon(location_name)
            if coord is not None:
                trail_dictionary = get_hiking_data(coord['lat'], coord['lng'])['trails']
            else:
                flash('City and state not found.', 'error')
        except:
            flash('There was a problem connecting to the geocoding API', 'error')
  
    if(request.form.get('trail_select')):
        # Getting the trail's info
        trail_id = request.form.get('trail_select')
        for trail in trail_dictionary:
            if int(trail['id']) == int(trail_id):
                trail_id = trail['id']
                trail_name = trail['name']
                trail_type = trail['type']
                trail_difficulty = trail['difficulty']
                trail_stars = trail['stars']
                trail_location = trail['location']
                trail_url = trail['url']
                trail_length = trail['length']
                trail_ascent = trail['ascent']
                trail_descent = trail['descent']
                trail_lat  = trail['latitude']
                trail_lon  = trail['longitude']
                trail_condition_details = trail['conditionDetails']

        # The show weather set up. Makes an API call to get the weather for the next ten days and feeds that to the page
        if request.form['submit_button'] == 'show_weather':
            weather_data = get_weather_data(trail_lat, trail_lon)
            for time in weather_data['list']:
                time['dt'] = datetime.fromtimestamp(time['dt'])
                time['main']['temp'] = k_to_f(time['main']['temp'])
            return render_template('show_weather.html', weather_list = weather_data, location_form = loc_form, trail_list = trail_dictionary, trail_name = trail_name)

        elif request.form['submit_button'] == 'save_trail':
            # saving a trail 
            trailsViewModel = view_model.ViewModel(trailsDB)

            trail = Bookmarks(trail_id = trail_id, name = trail_name, trail_type=trail_type, difficulty=trail_difficulty, stars=trail_stars, location=trail_location, url=trail_url, length=trail_length, ascent=trail_ascent, descent=trail_descent, longitude=trail_lon, latitude=trail_lat, condition_details=trail_condition_details)

            trailsViewModel.insertTrail(trail=trail)

            flash(f'{trail_name} has been saved!', 'success')
        else:
            # The show map set up  
            return render_template('show_map.html', lat = trail_lat, lon = trail_lon, key = os.environ.get('MAP_KEY'), location_form = loc_form, trail_list = trail_dictionary, trail_name = trail_name)
    else:
        flash('Please select a trail', 'error')

    #rerenders the homepage 
    return render_template('home.html', location_form = loc_form, trail_list = trail_dictionary)

def k_to_f(kelvin):
    # A helpter function to make the weather's temperature data into a unit that Americans know what to do with.
    return int((float(kelvin) - 273.15) * 9/5 + 32)
