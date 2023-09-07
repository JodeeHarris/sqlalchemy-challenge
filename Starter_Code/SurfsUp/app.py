# Import the dependencies.
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
Base.prepare(autoload_with=engine)

# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"

        f"/api/v1.0/stations<br/>"

        f"/api/v1.0/tobs<br/>"

        f"/api/v1.0/:start<br/>"

        f"/api/v1.0/:start/:end"
    )

@app.route("/api/v1.0/precipitation")
def precipetation():
    time_before = dt.datetime(2017,8,23-dt.timedelta(days = 365))
    rain = session.query(measure.date,measure.prcp).filter(measure.date >= time_before).all()
    
    rain_frame = []
    
    for date, prcp in rain:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        rain_frame.append(rain_dict)

    return jsonify(rain_frame)
    
@app.route("/api/v1.0/stations")
def Stations():
    station_query = session.query(measure.station,func.count(measure.station)).group_by(measure.station).order_by(func.count(measure.station).desc()).all()
    
    station_frame = []
    
    for station, count in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        station_frame.append(station_dict)

    return jsonify(station_frame)
    
@app.route("/api/v1.0/tobs")
def func2():
    time_before = dt.datetime(2017,8,23)- dt.timedelta(days = 365)
    station_query = session.query(measure.station, measure.date, measure.tobs).filter(measure.date >= time_before).filter(measure.station =='USC00519281').all()
    
    station_frame = []
    
    for station, date, tobs in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["date"] = date
        station_dict["tobs"] = tobs
        station_frame.append(station_dict)

    return jsonify(station_frame)
@app.route("/api/v1.0/<start>")
def TOBS_Search(start):
    
    tobs_query = session.query(func.min(measure.tobs),func.max(measure.tobs),func.avg(measure.tobs)).filter(measure.date >= start).all()
    
    tobs_frame = []
    
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        tobs_frame.append(tobs_dict)

    return jsonify(tobs_frame)
    
@app.route("/api/v1.0/<start>/<end>")
def active_station(start,end):
    
    tobs_query = session.query(func.min(measure.tobs),func.max(measure.tobs),func.avg(measure.tobs)).filter(measure.date >= start, measure.date < end).all()
    
    tobs_frame = []
    
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        tobs_frame.append(tobs_dict)

    return jsonify(tobs_frame)

if __name__ == '__main__':
    app.run(debug=True)