# 1. Import Flask
import pandas as pd
import numpy as np
import os
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

os.chdir(os.path.dirname(os.path.abspath(__file__)))

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)

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
    def precipitation():        
        session = Session(engine)
        results = session.query(Measurement.station).all()

        session(close)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)