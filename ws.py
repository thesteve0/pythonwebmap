from flask import Flask
from flask import g
from flask import Response
from flask import request
from flask import render_template
import os
from pymongo.mongo_client import MongoClient
import json
from bson import json_util
from bson import objectid

#todo add a piece to server static content
#todo see what the new json looks like client side
#todo modify the JS that makes the pins


#need to define the location of static content
app = Flask(__name__, static_url_path='' )
#add this so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/')
def index():
    return app.send_static_file("index.html")

##############################################
## Database setup
#############################################

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

#############################################
## Real Queries
##############################################

#find points within a bounding box
@app.route("/ws/parks/within")
def within():
    db = get_db()

    #Get the box - production code would trap for invalid values
    lat1 = float(request.args.get('lat1'))
    lon1 = float(request.args.get('lon1'))
    lat2 = float(request.args.get('lat2'))
    lon2 = float(request.args.get('lon2'))

    # make a geoJSON box
    geometry = { "type" : "Polygon", "coordinates" : [[[lon1, lat1], [lon2, lat1], [lon2, lat2], [lon1, lat2], [lon1, lat1]]]}
    #again impose a limit as the results may be large for larger map extents
    result = db.placenames.find({"pos" : { "$geoWithin" : { "$geometry" : geometry} } }).limit(800)
    return Response(response=str(json.dumps({'results':list(result)},default=json_util.default)), status=200, mimetype="application/json" )


#find parks near a lat and long passed in as query parameters (near?lat=45.5&lon=-82)
@app.route("/ws/parks/near")
def near():
    #setup the connection
    db = get_db()
    #get the request parameters - production code would trap for invalid values
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    #use the request parameters in the query
    #again limiting results here due to data size
    result = db.placenames.find({"pos" : { "$near" : {"$geometry" : { "type" : "Point" , "coordinates": [ lon , lat ] }}}}).limit(200)

    #turn the results into valid JSON
    return Response(response=str(json.dumps({'results':list(result)},default=json_util.default)), status=200, mimetype="application/json" )


@app.route("/ws/parks")
def all_parks():
    db = get_db()
    #only return the first 100 docs
    result = db.placenames.find().limit(200)
    return Response(response=str(json.dumps({'results':list(result)},default=json_util.default)), status=200, mimetype="application/json" )

#########################################
## Just Testing basics
########################################

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"




if __name__ == "__main__":
    app.run()

