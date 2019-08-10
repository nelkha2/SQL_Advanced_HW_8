#Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

from flask import Flask, jsonify

#DB setup 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Flask setup 
app = Flask(__name__)

#Flask Routes (home page)
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tempstats<br/>"
        f"/api/v1.0/tobs<br/>"
    )


#Precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    precp_data = session.query(Measurement.date, Measurement.prcp).all()
    precp_data_list = list(np.ravel(precp_data))
    return jsonify(precp_data_list)

#Stations 
@app.route("/api/v1.0/stations")
def stations():
    inspector = inspect(engine)
    columns = inspector.get_columns('station')

    #Reflect DB into ORM class
    Station = Base.classes.station

    #Station identifier
    station_identifier = session.query(Station.station).all()
    station_identifier_list = list(np.ravel(station_identifier))

    return (jsonify(station_identifier_list))

#Last 12 month temp observations
@app.route("/api/v1.0/tobs")
def tobs():
   
    last_date_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    twelve_month_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.tobs , Measurement.date).\
    filter(Measurement.date > twelve_month_date).all()
    tobs_data_list = list(np.ravel(tobs_data))

    return jsonify(tobs_data_list)

#temp stats: min, average, max
@app.route("/api/v1.0/tempstats")
def tempstats():
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()
    temp_stats_clean = list(np.ravel(temp_stats))
    return jsonify(temp_stats_clean)


if __name__ == '__main__':
    app.run(debug=True)