from flask import Flask, render_template, flash, redirect, url_for, request
from api_connection import *
from forms import LocationInputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blargitsasecretthatdoesntmatterforthiscontext'

@app.route('/', methods=['GET', 'POST'])
@app.route('/find_trails', methods=['GET', 'POST'])
def hello():
    loc_form = LocationInputForm()
    trail_dictionary = {}
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
    return render_template('home.html', location_form = loc_form, trail_list = trail_dictionary)

@app.route('/show_map', methods=['POST'])
def show_map():
    return render_template('home.html')