import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).filter(Measurement.date >= dt.date(2016,8,23)).all()

    # Convert list of tuples into normal list
    all_date = list(np.ravel(results))

    return jsonify(all_date)

@app.route("/api/v1.0/stations")
def stations():
    
    # Query all passengers
    results = session.query(Station.station).all()
    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= dt.date(2016,8,23)).all()
    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)


if __name__ == '__main__':
    app.run(debug=True)
