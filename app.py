from flask_pymongo import PyMongo
from flask import jsonify,request, Flask
from flask import Flask
import logging as logger
import os
from dotenv import load_dotenv, find_dotenv
logger.basicConfig(level="DEBUG")

load_dotenv(find_dotenv())

app = Flask(__name__)
 
app.config['MONGO_URI'] = f"mongodb+srv://{os.getenv('MONGO_URI_USER')}:{os.getenv('MONGO_URI_USER_PASSWORD')}@cluster1.v5rmdlf.mongodb.net/?retryWrites=true&w=majority"
 
mongo = PyMongo(app)

def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp

if __name__ == "__main__":
    logger.debug("Starting Flask Server")
    from api import *
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)