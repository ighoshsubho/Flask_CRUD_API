from flask_restful import Resource
import logging as logger
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash
from app import mongo, not_found

class UserAPIbyID(Resource):

    def get(self,id):
        logger.debug("Inisde the get method of UserAPIbyID. UserID = {}".format(id))
        user = mongo.cx.db.user.find({'_id':ObjectId(id)})
        resp = dumps(user)
        return resp


    def put(self,id):
        logger.debug("Inisde the put method of UserAPIbyID. UserID = {}".format(id))
        _id = id
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['password']
 
        if _name and _email and _password and _id and request.method == "PUT":
 
            _hashed_password = generate_password_hash(_password)
 
            mongo.cx.db.user.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'password:':_hashed_password}})
 
            resp = jsonify("User updated successfully")
 
            resp.status_code = 200
 
            return resp
 
        else:
 
            return not_found()


    def delete(self,id):
        logger.debug("Inisde the delete method of UserAPIbyID. UserID = {}".format(id))
        mongo.cx.db.user.delete_one({'_id':ObjectId(id)})
        resp = jsonify("User deleted successfully")
        resp.status_code = 200
        return resp