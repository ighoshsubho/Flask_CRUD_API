from flask_restful import Resource
import logging as logger
from bson.json_util import dumps
from flask import jsonify,request
from werkzeug.security import generate_password_hash
from app import mongo, not_found


class User(Resource):

    def post(self):
        logger.debug("Inside the post method of User")
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['password']
 
        if _name and _email and _password and request.method == "POST":
 
            _hashed_password = generate_password_hash(_password)
 
            id = mongo.cx.db.user.insert_one({'name':_name,'email':_email,'password':_hashed_password})
 
            resp = jsonify("User Added successfully")
 
            resp.status_code = 200
 
            return resp
 
        else:
 
            return not_found()


    def get(self):
        logger.debug("Inisde the get method of User")
        users = mongo.cx.db.user.find({})
        resp = dumps(users)
        return resp