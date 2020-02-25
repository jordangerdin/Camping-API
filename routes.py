from flask import Flask, render_template, flash, redirect, url_for, request
from api_connection import *
from forms import LocationInputForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blargitsasecretthatdoesntmatterforthiscontext'

trail_dictionary = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/find_trails', methods=['GET', 'POST'])
def hello():
    loc_form = LocationInputForm()
    if loc_form.validate_on_submit():
        location_name = loc_form.city.data + ', ' + loc_form.state.data
        try:
            coord = get_lat_lon(location_name)
            if coord is not None:
                trail_dictionay = get_hiking_data(coord['lat'], coord['lng'])['trails']
            else:
                flash('test')
        except:
            flash('There was a problem connecting to the geocoding API ' + location_name + 'test')
    return render_template('home.html', location_form = loc_form, trail_list = trail_dictionary)

@app.route('/show_extra', methods=['POST'])
def show_extra():
    lat_long = request.form.get('trail_select')
    lat_long_list = lat_long.split(',')

    weather_data = get_weather_data(lat_long_list[0],lat_long_list[1])
    for day in weather_data['list']:
        day['dt'] = datetime.fromtimestamp(day['dt'])
        for key, temp in day['temp'].items():
            day['temp'][key] = k_to_f(temp)

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
    return render_template('show_weather.html', weather_list = weather_data, location_form = loc_form, trail_list = trail_dictionary)


def k_to_f(kelvin):
    return int((float(kelvin) - 273.15) * 9/5 + 32)
