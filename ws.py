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

def get_db_client():
    if not hasattr(g, 'mongodb_client'):
        g.mongodb_client = get_MongoDB()
    return g.mongodb_client


def get_MongoDB():
    client = MongoClient(os.environ['OPENSHIFT_NOSQL_DB_URL'])

@app.route("/")
def base():
    return "<strong>hello from Flask and IDEA </strong>"

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"

if __name__ == "__main__":
    app.run()

