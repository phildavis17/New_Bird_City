from app.trip import MASTER_TRIP
from flask import render_template
from app import app
from app import trip
from app.trip import Trip

#import app.trip

@app.route('/')
@app.route('/index')
def index():
    #user = {'username': 'Miguel'}
    return "Hello World! I'm working on it, ok?"

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


@app.route('/analysis/<rt_index>')
def hs_route(rt_index):
    pass


# Would I then do something like /analysis/<rt_index>/hotspots/<hotspot>
# and then                       /analysis/<rt_index>/species/<species>