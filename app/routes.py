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