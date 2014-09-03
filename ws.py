from flask import Flask
from flask import g
import os
from pymongo.mongo_client import MongoClient

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
    return client

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
if hasattr(g, 'mongodb_client'):
    g.mongodb_client.close()


@app.route("/")
def base():
    client = get_db()
    db = client.db[os.environ['OPENSHIFT_APP_NAME']]


    result = db['placenames'].find_one()

    result = str(result) + " " + str(placenames.collection_names)

    return result

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"

if __name__ == "__main__":
    app.run()

