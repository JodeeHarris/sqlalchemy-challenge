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

#Beginning webpage for the server
@app.route("/")
def welcome():
    
    #List all available api routes
    return (
        f"Available Routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"

        f"/api/v1.0/stations<br/>"

        f"/api/v1.0/tobs<br/>"

        f"/api/v1.0/:start<br/>"

        f"/api/v1.0/:start/:end"
    )



#Creating a route
@app.route("/api/v1.0/precipitation")

#Creating a definition
def precipetation():
    
    #Creating a time date variable to search fopr the past year's relevant data
    time_before = dt.datetime(2017,8,23-dt.timedelta(days = 365))
    
    #Creating a query
    rain = session.query(measure.date,measure.prcp
                                ).filter(measure.date >= time_before
                                                            ).all()
   
    #creating an empty dictionary
    rain_frame = []
    
    #Creating a for loop to run through the query into a list
    for date, prcp in rain:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        
        #Appending the list into a dictionary
        rain_frame.append(rain_dict)

    #Jsonifying the dictionary
    return jsonify(rain_frame)



#Creating a route
@app.route("/api/v1.0/stations")

#Creating a definition
def Stations():
    
    #Creating a query
    station_query = session.query(measure.station,func.count(measure.station
                                                             )).group_by(measure.station
                                                                         ).order_by(func.count(measure.station
                                                                                               ).desc(
                                                                                                   )).all()
    
    #creating an empty dictionary
    station_frame = []
    
    #Creating a for loop to run through the query into a list
    for station, count in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        
        #Appending the list into a dictionary
        station_frame.append(station_dict)

    #Jsonifying the dictionary
    return jsonify(station_frame)



#Creating a route
@app.route("/api/v1.0/tobs")

#Creating a definition
def specific_station():
    
    #Creating a time date variable to search fopr the past year's relevant data
    time_before = dt.datetime(2017,8,23)- dt.timedelta(days = 365)
    
    #Creating a query
    station_query = session.query(measure.station, measure.date, measure.tobs
                                  ).filter(measure.date >= time_before
                                           ).filter(measure.station =='USC00519281'
                                                                               ).all()
    
    #creating an empty dictionary
    station_frame = []
    
    #Creating a for loop to run through the query into a list
    for station, date, tobs in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["date"] = date
        station_dict["tobs"] = tobs
        
        #Appending the list into a dictionary
        station_frame.append(station_dict)

    #Jsonifying the dictionary
    return jsonify(station_frame)



#Creating a route
@app.route("/api/v1.0/<start>")

#Creating a definition with a user start date search
def TOBS_Search(start):
    
    #Creating a query
    tobs_query = session.query(func.min(measure.tobs
                                        ),func.max(measure.tobs
                                                   ),func.avg(measure.tobs
                                                              )).filter(measure.date >= start
                                                                                        ).all()
   
   #creating an empty dictionary 
    tobs_frame = []
    
    #Creating a for loop to run through the query into a list 
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        
        #Appending the list into a dictionary
        tobs_frame.append(tobs_dict)

    #Jsonifying the dictionary
    return jsonify(tobs_frame)
    
    
    
#Creating a route
@app.route("/api/v1.0/<start>/<end>")

#Creating a definition with a user start date and end date search
def active_station(start,end):
    
    #Creating a query
    tobs_query = session.query(func.min(measure.tobs
                                        ),func.max(measure.tobs
                                                   ),func.avg(measure.tobs
                                                              )).filter(measure.date >= start, measure.date < end
                                                                                                                ).all()
    
    #creating an empty dictionary
    tobs_frame = []
    
    #Creating a for loop to run through the query into a list
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        
        #Appending the list into a dictionary
        tobs_frame.append(tobs_dict)

    #Jsonifying the dictionary
    return jsonify(tobs_frame)

if __name__ == '__main__':
    app.run(debug=True)