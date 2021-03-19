# Dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create app
app = Flask(__name__)

# Create engine and set up database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create Base object 

Base = automap_base()

# Reflect existing database on new model

Base.prepare(engine, reflect = True)

# Save references to both tables

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create routes
@app.route("/")
def home():
    return (
        f'Welcome to the Hawaii API home page!</br>'
        f'</br>'
        f'These are the routes available:</br>'
        f'/api/v1.0/precipitation</br>'
        f'/api/v1.0/stations</br>'
        f'/api/v1.0/tobs'
    )

# Precipitation API
@app.route("/api/v1.0/precipitation")
def precipitation_query():
    
    # Start a session
    session = Session(engine)

    # Query precipitation by date
    results = session.query(Measurement.date, Measurement.prcp).\
        all()
    
    session.close()
    precipitations_list = []

    # For loop to fill the dictionary

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict.update({date: prcp})
        precipitations_list.append(prcp_dict)

    return jsonify(precipitations_list)

# Stations list API
@app.route("/api/v1.0/stations")
def station_query():

    # Start a session
    session = Session(engine)

    # Query stations
    results = session.query(Station.station).all()
    
    # Close session
    session.close()

    # Create a dictionary with all stations
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temperature_list():

    # Open a session
    session = Session(engine)

    # Query temp observations
    tobs_query = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281", Measurement.date >= "2016-08-23").all()

    # Close session
    session.close()

    # Parse TOBS into a list
    tobs_list = []
    for record in tobs_query:
        tobs = record[2]
        tobs_list.append(tobs)

    # Return list
    return jsonify(tobs_list)

# Dynamic API
@app.route("/api/v1.0/<start>") 

def start_temp_summary(start):

     # Open a session
    session = Session(engine)

    # Query temp observations
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).all()

    # Close session
    session.close()

    # Retrieve a list of temperatures
    tobs_list = []
    for record in tobs_query:
        tobs = record[1]
        if tobs == 'null':
            pass
        else:
            tobs_list.append(tobs)

    tobs_summary = {
        'TMIN': min(tobs_list),
        'TAVG': np.average(tobs_list),
        'TMAX': max(tobs_list)
        }

    return jsonify(tobs_summary)
    
@app.route("/api/v1.0/<start>/<end>") 

def start_end_temp_summary(start, end):

     # Open a session
    session = Session(engine)

    # Query temp observations
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    # Close session
    session.close()

    # Retrieve a list of temperatures
    tobs_list = []
    for record in tobs_query:
        tobs = record[1]
        if tobs == 'null':
            pass
        else:
            tobs_list.append(tobs)

    tobs_summary = {
        'TMIN': min(tobs_list),
        'TAVG': np.average(tobs_list),
        'TMAX': max(tobs_list)
        }
        
    return jsonify(tobs_summary)

# Debug mode
if __name__ == "__main__":
    app.run(debug = True)