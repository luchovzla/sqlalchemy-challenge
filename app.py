# Dependencies
import numpy as np

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


# Debug mode
if __name__ == "__main__":
    app.run(debug = True)