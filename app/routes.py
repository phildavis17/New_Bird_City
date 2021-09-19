from app.db_definitions import Hotspot, HotspotConfig, Period
from flask import render_template, redirect, flash, url_for, request
from flask.helpers import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import relation, sessionmaker
from wtforms import BooleanField

from app import app
from app import analysis
from app.forms import MyForm, TripCreationForm 

# from app.analysis import Analysis

engine = create_engine("sqlite:///data/NBC_DEV_DB.db")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Demo_User_001"}
    return render_template("index.html", user=user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/user/<username>")
def user_page(username: str):
    with Session() as user_session:
        user = dict()
        user["username"] = "Demo_User_001"
        user["trips"] = analysis.get_user_analyses(user_session, user["username"])
    return render_template("user_page.html", user=user)


@app.route("/user/<username>/<tripid>", methods = ["GET", "POST"])
def trip_page(username: str, tripid: str):
    user = {"username": username}    
    with session as trip_session:
        trip = analysis.build_analysis(trip_session, tripid)
        trip.analysis_id = str(tripid)
        if request.method == "POST":
            return "Post!"
            trip.set_hs_active_by_id(list(request.form.keys()))
            #return redirect(url_for("trip_details_page", username=username, tripid=tripid, hsbv=trip.get_current_bv()))
    return render_template("analysis.html", user=user, trip=trip)


@app.route("/user/<username>/<tripid>/<hsbv>", methods = ["GET", "POST"])
def trip_details_page(username: str, tripid: str, hsbv: str):
    # I'm doing this in a stateless way, because my understanding is that this is in keeping
    # with the general vibe of the web. Possible I'm wrong!
    user = {"username": username}
    with session as trip_session:
        trip = analysis.build_analysis(trip_session, tripid)
        trip.set_hs_active_by_bv(hsbv)
    return render_template("trip.html", trip=trip)


# TESTING        
@app.route("/formtest", methods = ["GET", "POST"])
def form_test():
    form = MyForm()
    if request.method == "POST" and form.validate_on_submit():
        return redirect(url_for("form_output", text="test1"))
    return render_template("form.html", form=form)


@app.route("/formtest/<username>", methods = ["GET", "POST"])
def form_output(username: str):
    form = TripCreationForm()
    for c in username:
        setattr(form, c, BooleanField())
    return render_template("output.html", form=form)

@app.route("/user/<username>/new-trip")
def new_trip(username: str):
    return "Look, I'm workin on it, OK?"

@app.route("/user/<username>/edit/<tripid>")
def edit_trip(username:str, tripid: str):
    user = {
        "username": username,
        "tripid": tripid,
    }
    return render_template("edit_trip.html", user=user)

@app.route("/user/<username>/cheap-trip", methods = ["GET", "POST"])
def cheap_trip(username: str):
    # get a list of all hotspots in the system
    user = {
        "username": username,
    }
    with Session() as period_session:
        periods = period_session.query(Period)
        period_dict = {p.Description: p.PeriodId for p in periods}

    if request.method == "POST":
        trip_info = dict(request.form)
        t_name, t_period = None, None
        t_hotspots = []
        for k, v in trip_info.items():
            if k == "trip-name":
                t_name = v
            elif k == "trip-period":
                t_period = int(period_dict[v])
            else:
                t_hotspots.append(k)
        new_trip = analysis.Analysis(t_hotspots, t_period, t_name)
        with Session() as write_session:
            analysis.write_analysis(write_session, username, new_trip)
        return redirect(url_for("trip_page", username=username, tripid=new_trip.analysis_id))
        
    with Session() as sesh:
        hotspots = sesh.query(Hotspot)
        known_hotspots = [hs.LocId for hs in hotspots]
            
    return render_template("cheap_trip.html", user=user, locs=known_hotspots, periods=list(period_dict.keys()))

# ---Dormant---

# Login
# Map
# seen birds
# trip details
