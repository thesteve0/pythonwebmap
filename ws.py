from flask import Flask
from flask import g
from flask import Response
from flask import request
import os
from pymongo.mongo_client import MongoClient
import json
from bson import json_util
from bson import objectid

#TODO import data (maybe new data)
#todo build 2d spehere index
#todo try a simple spatial query
#todo do a call that maps to /ws/parks and returns all

app = Flask(__name__)
#add this so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True

def get_db():
    if not hasattr(g, 'mongodb_client'):
        g.mongodb_client = get_MongoDB()
    return g.mongodb_client


def get_MongoDB():
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],  int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    client[os.environ['OPENSHIFT_APP_NAME']].authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'], os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'], source='admin')
    db = client[os.environ['OPENSHIFT_APP_NAME']]
    return db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
if hasattr(g, 'mongodb_client'):
    g.mongodb_client.close()



#find parks near a lat and long passed in as query parameters (near?lat=45.5&lon=-82)
@app.route("/ws/parks/near")
def near():
    #setup the connection
    db = get_db()
    #get the request parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    #use the request parameters in the query
    result = db.placenames.find({"pos" : { "$near" : {"$geometry" : { type : "Point" , "coordinates": [ lon , lat ] }}}})
    #turn the results into valid JSON
    return Response(response=json.dumps({'results':list(result)},default=json_util.default), status=200, mimetype="application/json" )

@app.route("/ws/parks")
def AllParks():
    db = get_db()
    #only return the first 100 docs
    result = db.placenames.find().limit(100)
    return Response(response=str(json.dumps({'results':list(result)},default=json_util.default)), status=200, mimetype="application/json" )

    #return str(json.dumps({'results':list(result)},default=json_util.default))

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"

@app.route("/")
def base():
    return "<h1>How very strange</h1>"

if __name__ == "__main__":
    app.run()

