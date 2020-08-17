# 1. Import Flask

import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import datetime as dt

from flask import Flask, jsonify

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# 3. Define static routes
@app.route("/")
def home():
    return("Climate App - based on Hawaii <br/>"
    "List of Available API routes are: <br/>"
    "/api/v1.0/precipitation <br/>"
    "/api/v1.0/stations <br/>"
    "/api/v1.0/tobs <br/>"
    "/api/v1.0/<start> <br/>"
    "/api/v1.0/<start>/<end> <br/>")


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Re-run query
    prcp_results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
    group_by(Measurement.date).all()

    session.close()

    #convert list of tuples into normal list
    prcp_dates = list(prcp_results)

    return jsonify(prcp_dates)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Re-run query
    station_results = session.query(Station.name, func.count(Measurement.station)).\
                    filter(Station.station == Measurement.station).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

    session.close()
    all_stations = list(station_results)
    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Re-run query
    tobs_results = session.query(Measurement.date, func.avg(Measurement.tobs)).\
                filter(Measurement.date.between('2016-08-23','2017-08-23')).\
                group_by(Measurement.date).filter(Measurement.station == "USC00519281").all()

    session.close()

#Create a dictionary from the row data and append to a list of tobs_results for last 12 months
    last_12_mo_tobs = []
    for date, temp in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = temp
        last_12_mo_tobs.append(tobs_dict)

    return jsonify(last_12_mo_tobs)

@app.route("/api/v1.0/<start_date>")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Re-run query
    start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    start_date_only = []
    for min, max, avg in start_date_results:
        min_max_avg_dict: {}
        min_max_avg_dict["Minimum Temperature"] = min
        min_max_avg_dict["Maximum Temperature"] = max
        min_max_avg_dict["Average Temperature"] = avg
        start_date_only.append(min_max_avg_dict)

    return jsonify(start_date_only)

# 4. Define main behavior
if __name__ == '__main__':
    app.run(debug=True)