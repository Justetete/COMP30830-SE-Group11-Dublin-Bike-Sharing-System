'''
We will connect to the local database, access its content through flask, and 
then show the content in a specific page in the form of a json file
'''
from flask import Flask, g, render_template, jsonify
import json
from sqlalchemy import create_engine, text

USER = "root"
PASSWORD = "Just1996" 
PORT = "3306"
DB = "local_db_jcdecaux"
URI = "127.0.0.1"


app = Flask(__name__, static_url_path='') # tell Flask where are the static files (html, js, images, css, etc.)


# Connect to the database and create the engine variable
def connect_to_db():
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)
    engine = create_engine(connection_string, echo = True)
    
    return engine

# Create the engine variable and store it in the global Flask variable 'g'
def get_db():
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine


# Let us retrieve information about a specific station
# @app.route("/available/<int:station_id>")
# def get_stations(station_id):
#     engine = get_db()
#     data = []

#     # Pass the `station_id` value as a parameter in the execute method
#     rows = engine.execute("SELECT available_bikes from availability where number = {};".format(station_id))


#     for row in rows:
#         data.append(dict(row))
    
#     return jsonify(available=data)

# @app.route("/available/<int:station_id>")
# def get_stations(station_id):
#     data = []

#     with engine.connect() as connection:
#         query = text("SELECT available_bikes FROM availability WHERE number = :station_id")
#         result = connection.execute(query, {"station_id": station_id})

#         for row in result:
#             data.append(dict(row))

#     return jsonify(available=data)

# Retrieve information about a specific station
@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    
    with engine.connect() as connection:
        query = text("SELECT available_bikes FROM availability WHERE number = :station_id")
        result = connection.execute(query, {"station_id": station_id})
        # result = connection.execute(text("SELECT available_bikes from availability where number = {};".format(station_id)))
        # for row in result:
        #     data.append(dict(row))

        for row in result.mappings():  # using `mappings()` to convert row to dictionary
            data.append(dict(row))

    return jsonify(available=data)

@app.route('/')
def root():
    return 'Navigate http://127.0.0.1:5000/available/<int:station_id>'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)