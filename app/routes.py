from flask import render_template, redirect, flash, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app import analysis

# from app.analysis import Analysis

engine = create_engine("sqlite:///data/vagrant_db.db")
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
    return "New Bird City helps you get ready to see birds."


@app.route("/user/<username>")
def user_page(username: str):
    with Session() as user_session:
        user = dict()
        user["username"] = "Demo_User_001"
        user["trips"] = analysis.get_user_analyses(user_session, user["username"])
    return render_template("user_page.html", user=user)


@app.route("/user/<username>/<tripid>")
def trip_page(username: str, tripid: str):
    user = {"username": username}
    with session as trip_session:
        trip = analysis.build_analysis(trip_session, tripid)
    return render_template("analysis.html", user=user, trip=trip)


@app.route("/user/<username>/<tripname>/<hsbv>")
def trip_details_page(username: str, tripname: str, hsbv: str):
    pass


# ---Dormant---

# Login
# Map
# seen birds
