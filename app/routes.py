from app.trip import MASTER_TRIP, trip_from_index
from flask import render_template, redirect, flash, url_for, request
#from flask_wtf import FlaskForm
#from wtforms import BooleanField, SubmitField
from app import app
from app import trip
from app.trip import Trip
from app.forms import MyForm

#import app.trip

@app.route('/')
@app.route('/index')
def index():
    #user = {'username': 'Miguel'}
    return render_template('index.html')

@app.route('/base/<title>')
def base(title):
    #title = "this is a test"/
    return render_template('base.html', title=title)

#newbirdcity/analysis/001101110/prospect park (birds that are specialties of this park, while on this route)
#newbirdcity/analysis/11111111111111/prospect park
#newbirdcity/analysis/prospect park (basline info about prospect park)

@app.route('/analysis')
def analysis():
    title = "Hotspot Analysis"
    #dummy_trip = trip.build_master_trip(MASTER_TRIP)
    hotspots = MASTER_TRIP["Hotspot Names"]
    species = MASTER_TRIP["Birds"]
    return render_template('analysis.html', title=title, hotspots=hotspots, birds=species)


@app.route('/analysis/species/<sp_name>')
def analysis_species(sp_name):
    pass


@app.route('/analysis/hotspots/<hs_name>') # the /hotspots/ part saves me from having to decide whether the thing submitted is a park or a bird
def analysis_hotspot(hs_name):
    pass


@app.route('/analysis/<trip_index>')
def hs_trip(trip_index):
    new_trip = trip_from_index(MASTER_TRIP, trip_index)
    return render_template('trip.html', this_trip=new_trip)


@app.route('/analysis/<trip_index>/specialties')
def specialties(trip_index):
    new_trip = trip_from_index(MASTER_TRIP, trip_index)
    return render_template('specialties.html', this_trip=new_trip)


@app.route('/analysis/<trip_index>/hotspot/<hotspot_name>')
def trip_park(trip_index, park_name):
    new_trip = trip_from_index(MASTER_TRIP, trip_index)
    return render_template('trip_hotspot.html', master_dict=MASTER_TRIP, this_trip=new_trip, this_hotspot=hotspot_name)

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/form_test', methods=['GET', 'POST'])
def form_test():
    form = MyForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for("base", title=request.form['name']))
    return render_template('form.html', form=form)
    

# Would I then do something like /analysis/<rt_index>/hotspots/<hotspot>
# and then                       /analysis/<rt_index>/species/<species>