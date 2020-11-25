from flask import render_template
from app import app
from app.route import Route

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return "Hello World!"

@app.route('/base/<title>')
def base(title):
    #title = "this is a test"
    return render_template('base.html', title=title)

#newbirdcity/analysis/001101110/prospect park (birds that are specialties of this park, while on this route)
#newbirdcity/analysis/11111111111111/prospect park
#newbirdcity/analysis/prospect park (basline info about prospect park)

@app.route('/analysis')
def analysis():
    title = "Hotspot Analysis"
    return render_template('analysis.html', title=title)


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