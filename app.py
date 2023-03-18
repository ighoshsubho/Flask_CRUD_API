from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request, Flask
from werkzeug.security import generate_password_hash,check_password_hash
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
# app.secret_key = "thisissecret"
 
app.config['MONGO_URI'] = f"mongodb+srv://{os.getenv('MONGO_URI_USER')}:{os.getenv('MONGO_URI_USER_PASSWORD')}@cluster1.v5rmdlf.mongodb.net/?retryWrites=true&w=majority"
 
mongo = PyMongo(app)

print(mongo.cx.db)

@app.route('/add',methods=['POST'])
def add_user():
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
    
@app.route('/users')
def users():
    users = mongo.cx.db.user.find({})
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.cx.db.user.find({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.cx.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code = 200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
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

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp

if __name__ == "__main__":
    app.run(debug=True)